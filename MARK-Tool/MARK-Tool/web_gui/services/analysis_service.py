"""
Analysis Service - Handles interaction with exec_analysis.py and cloner.py
"""
import os
import sys
import subprocess
import threading
import time
import uuid
from typing import Optional, Dict, Tuple
from datetime import datetime


class AnalysisJob:
    """Represents an analysis job"""
    
    def __init__(self, job_id: str, input_path: str, output_path: str, github_csv: Optional[str] = None):
        self.job_id = job_id
        self.input_path = input_path
        self.output_path = output_path
        self.github_csv = github_csv
        self.status = 'pending'  # pending, running, completed, failed
        self.progress = 0
        self.message = 'Job created'
        self.started_at = None
        self.completed_at = None
        self.error = None
        self.process = None
        self.thread = None
        self.output_log = []
    
    def to_dict(self) -> Dict:
        """Convert job to dictionary"""
        return {
            'job_id': self.job_id,
            'input_path': self.input_path,
            'output_path': self.output_path,
            'github_csv': self.github_csv,
            'status': self.status,
            'progress': self.progress,
            'message': self.message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error': self.error,
            'output_log': self.output_log[-50:]  # Last 50 lines
        }


class AnalysisService:
    """Service for managing analysis jobs"""
    
    def __init__(self, exec_analysis_path: str, cloner_path: str):
        """
        Initialize the analysis service
        
        Args:
            exec_analysis_path: Path to exec_analysis.py
            cloner_path: Path to cloner.py
        """
        self.exec_analysis_path = exec_analysis_path
        self.cloner_path = cloner_path
        self.jobs: Dict[str, AnalysisJob] = {}
        self.lock = threading.Lock()
    
    def create_job(self, input_path: str, output_path: str, github_csv: Optional[str] = None) -> str:
        """
        Create a new analysis job
        
        Args:
            input_path: Path to input folder
            output_path: Path to output folder
            github_csv: Optional path to GitHub CSV file
            
        Returns:
            Job ID
        """
        job_id = str(uuid.uuid4())
        
        with self.lock:
            job = AnalysisJob(job_id, input_path, output_path, github_csv)
            self.jobs[job_id] = job
        
        return job_id
    
    def get_job(self, job_id: str) -> Optional[AnalysisJob]:
        """
        Get a job by ID
        
        Args:
            job_id: Job ID
            
        Returns:
            AnalysisJob or None
        """
        with self.lock:
            return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> list:
        """Get all jobs"""
        with self.lock:
            return [job.to_dict() for job in self.jobs.values()]
    
    def start_job(self, job_id: str, run_cloner: bool = False) -> Tuple[bool, str]:
        """
        Start an analysis job
        
        Args:
            job_id: Job ID
            run_cloner: Whether to run the cloner first
            
        Returns:
            Tuple of (success, message)
        """
        job = self.get_job(job_id)
        
        if not job:
            return False, "Job not found"
        
        if job.status == 'running':
            return False, "Job is already running"
        
        # Start the job in a background thread
        thread = threading.Thread(
            target=self._run_job,
            args=(job_id, run_cloner),
            daemon=True
        )
        
        with self.lock:
            job.thread = thread
            job.status = 'running'
            job.started_at = datetime.now()
            job.message = 'Job started'
        
        thread.start()
        
        return True, "Job started successfully"
    
    def _run_job(self, job_id: str, run_cloner: bool):
        """
        Run the analysis job (internal method, runs in thread)
        
        Args:
            job_id: Job ID
            run_cloner: Whether to run the cloner first
        """
        job = self.get_job(job_id)
        
        if not job:
            return
        
        try:
            # Step 1: Run cloner if requested and GitHub CSV provided
            if run_cloner and job.github_csv:
                self._update_job(job_id, status='running', progress=10, 
                               message='Running repository cloner...')
                
                success, message = self._run_cloner(job.input_path, job.github_csv)
                
                if not success:
                    self._update_job(job_id, status='failed', 
                                   error=f"Cloner failed: {message}")
                    return
                
                self._update_job(job_id, progress=30, 
                               message='Cloner completed successfully')
            
            # Step 2: Run analysis
            self._update_job(job_id, progress=40, 
                           message='Running MARK analysis...')
            
            success, message = self._run_analysis(job.input_path, job.output_path, job_id)
            
            if not success:
                self._update_job(job_id, status='failed', 
                               error=f"Analysis failed: {message}")
                return
            
            # Job completed successfully
            self._update_job(job_id, status='completed', progress=100,
                           message='Analysis completed successfully')
            
        except Exception as e:
            self._update_job(job_id, status='failed', 
                           error=f"Unexpected error: {str(e)}")
    
    def _run_cloner(self, input_path: str, github_csv: str) -> Tuple[bool, str]:
        """
        Run the repository cloner
        
        Args:
            input_path: Path to clone repositories to
            github_csv: Path to GitHub CSV file
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Build command
            cmd = [
                sys.executable,
                self.cloner_path,
                '--input', github_csv,
                '--output', input_path,
                '--no_repos2'
            ]
            
            # Run the cloner
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode == 0:
                return True, "Cloner completed successfully"
            else:
                return False, result.stderr or "Cloner failed"
                
        except subprocess.TimeoutExpired:
            return False, "Cloner timed out (exceeded 1 hour)"
        except Exception as e:
            return False, f"Error running cloner: {str(e)}"
    
    def _run_analysis(self, input_path: str, output_path: str, job_id: str) -> Tuple[bool, str]:
        """
        Run the MARK analysis
        
        Args:
            input_path: Path to input folder
            output_path: Path to output folder
            job_id: Job ID for logging
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Build command
            cmd = [
                sys.executable,
                self.exec_analysis_path,
                '--input_path', input_path,
                '--output_path', output_path
            ]
            
            # Run the analysis
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Store process for potential cancellation
            job = self.get_job(job_id)
            if job:
                with self.lock:
                    job.process = process
            
            # Read output in real-time
            progress_step = 50 / 100  # Remaining 50% progress divided by expected steps
            current_progress = 40
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Log output
                    self._add_log(job_id, line)
                    
                    # Update progress based on output
                    current_progress = min(90, current_progress + progress_step)
                    self._update_job(job_id, progress=int(current_progress), 
                                   message=f'Processing: {line[:100]}...')
            
            # Wait for completion
            process.wait()
            
            if process.returncode == 0:
                return True, "Analysis completed successfully"
            else:
                stderr = process.stderr.read()
                return False, stderr or "Analysis failed"
                
        except Exception as e:
            return False, f"Error running analysis: {str(e)}"
    
    def cancel_job(self, job_id: str) -> Tuple[bool, str]:
        """
        Cancel a running job
        
        Args:
            job_id: Job ID
            
        Returns:
            Tuple of (success, message)
        """
        job = self.get_job(job_id)
        
        if not job:
            return False, "Job not found"
        
        if job.status != 'running':
            return False, "Job is not running"
        
        try:
            # Terminate the process if it exists
            if job.process:
                job.process.terminate()
                job.process.wait(timeout=5)
            
            self._update_job(job_id, status='failed', 
                           error='Job cancelled by user')
            
            return True, "Job cancelled successfully"
            
        except Exception as e:
            return False, f"Error cancelling job: {str(e)}"
    
    def _update_job(self, job_id: str, **kwargs):
        """
        Update job properties
        
        Args:
            job_id: Job ID
            **kwargs: Properties to update
        """
        job = self.get_job(job_id)
        
        if job:
            with self.lock:
                for key, value in kwargs.items():
                    if hasattr(job, key):
                        setattr(job, key, value)
                
                if kwargs.get('status') == 'completed':
                    job.completed_at = datetime.now()
                elif kwargs.get('status') == 'failed':
                    job.completed_at = datetime.now()
    
    def _add_log(self, job_id: str, message: str):
        """
        Add a log message to job
        
        Args:
            job_id: Job ID
            message: Log message
        """
        job = self.get_job(job_id)
        
        if job:
            with self.lock:
                job.output_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'message': message
                })
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """
        Clean up old completed/failed jobs
        
        Args:
            max_age_hours: Maximum age of jobs to keep (in hours)
        """
        current_time = datetime.now()
        max_age_seconds = max_age_hours * 3600
        
        with self.lock:
            jobs_to_remove = []
            
            for job_id, job in self.jobs.items():
                if job.status in ['completed', 'failed'] and job.completed_at:
                    age = (current_time - job.completed_at).total_seconds()
                    
                    if age > max_age_seconds:
                        jobs_to_remove.append(job_id)
            
            for job_id in jobs_to_remove:
                del self.jobs[job_id]
                print(f"Removed old job: {job_id}")
    
    def get_last_completed_job(self) -> Optional[AnalysisJob]:
        """
        Get the most recently completed job
        
        Returns:
            AnalysisJob or None if no completed jobs exist
        """
        with self.lock:
            completed_jobs = [
                job for job in self.jobs.values() 
                if job.status == 'completed' and job.completed_at
            ]
            
            if not completed_jobs:
                return None
            
            # Sort by completion time (most recent first)
            completed_jobs.sort(key=lambda j: j.completed_at, reverse=True)
            
            return completed_jobs[0]
    
    def get_output_path_for_job(self, job_id: str) -> Optional[str]:
        """
        Get the output path for a specific job
        
        Args:
            job_id: Job ID
            
        Returns:
            Output path or None if job not found
        """
        job = self.get_job(job_id)
        
        if job:
            return job.output_path
        
        return None
    
    def get_last_analysis_output_path(self) -> Optional[str]:
        """
        Get the output path of the last completed analysis
        
        Returns:
            Output path or None if no completed analysis exists
        """
        last_job = self.get_last_completed_job()
        
        if last_job:
            return last_job.output_path
        
        return None
