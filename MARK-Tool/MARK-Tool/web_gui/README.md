# MARK Analysis Tool - Flask Backend API

This directory contains the Flask-based backend API for the MARK Analysis Tool, which replaces the desktop GUI with a modern web-based interface.

## 📁 Project Structure

```
web_gui/
├── app.py                          # Main Flask application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── routes/
│   ├── __init__.py
│   ├── analysis_routes.py          # Analysis execution endpoints
│   ├── file_routes.py              # File upload/download endpoints
│   └── results_routes.py           # Results viewing endpoints
├── services/
│   ├── __init__.py
│   ├── analysis_service.py         # Analysis job management
│   └── file_service.py             # File operations
├── static/
│   └── uploads/                    # Temporary file uploads
├── templates/                      # HTML templates (for future frontend)
├── utils/                          # Utility functions
└── logs/                           # Application logs (auto-created)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

Navigate to the `web_gui` directory and install the required packages:

```powershell
cd MARK-Tool\MARK-Tool\web_gui
pip install -r requirements.txt
```

## ⚙️ Configuration

The application supports three environments:
- **development** (default): Debug mode enabled, verbose logging
- **production**: Debug disabled, requires SECRET_KEY env variable
- **testing**: For running tests

### Environment Variables

You can set the following environment variables:

```powershell
# Set environment (development, production, testing)
$env:FLASK_ENV = "development"

# Set secret key (required for production)
$env:SECRET_KEY = "your-secret-key-here"

# Set host (default: 127.0.0.1)
$env:FLASK_HOST = "0.0.0.0"

# Set port (default: 5000)
$env:FLASK_PORT = "5000"
```

### Configuration Files

Edit `config.py` to customize:
- Upload folder location
- Max file size
- Allowed file extensions
- Default input/output paths
- Session settings
- CORS origins

## 🏃 Running the Application

### Method 1: Direct Python Execution

```powershell
python app.py
```

### Method 2: Using Flask CLI

```powershell
$env:FLASK_APP = "app.py"
flask run
```

### Method 3: Custom Host/Port

```powershell
$env:FLASK_HOST = "0.0.0.0"
$env:FLASK_PORT = "8080"
python app.py
```

The API will be available at `http://127.0.0.1:5000` (or your configured host/port).

## 📡 API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "MARK Analysis Tool API",
  "version": "1.0.0"
}
```

---

### Analysis Endpoints

#### Start Analysis

```
POST /api/analysis/start
```

Start a new analysis job.

**Request Body:**
```json
{
  "input_path": "/path/to/repos",
  "output_path": "/path/to/results",
  "github_csv": "/path/to/github.csv",  // Optional
  "run_cloner": false                    // Optional, default: false
}
```

**Response:**
```json
{
  "success": true,
  "message": "Analysis job started successfully",
  "job_id": "uuid-here",
  "job": {
    "job_id": "uuid-here",
    "status": "running",
    "progress": 0,
    "message": "Job started",
    ...
  }
}
```

#### Get Job Status

```
GET /api/analysis/status/<job_id>
```

Get the current status of an analysis job.

**Response:**
```json
{
  "success": true,
  "message": "Job found",
  "job": {
    "job_id": "uuid-here",
    "status": "running",
    "progress": 45,
    "message": "Processing...",
    "started_at": "2025-10-16T10:30:00",
    "completed_at": null,
    "error": null
  }
}
```

#### List All Jobs

```
GET /api/analysis/jobs
```

List all analysis jobs.

**Response:**
```json
{
  "success": true,
  "message": "Found 5 jobs",
  "jobs": [...]
}
```

#### Cancel Job

```
POST /api/analysis/cancel/<job_id>
```

Cancel a running analysis job.

**Response:**
```json
{
  "success": true,
  "message": "Job cancelled successfully"
}
```

#### Get Job Logs

```
GET /api/analysis/logs/<job_id>?limit=50
```

Get the execution logs for a job.

**Response:**
```json
{
  "success": true,
  "message": "Retrieved 50 log entries",
  "logs": [
    {
      "timestamp": "2025-10-16T10:30:15",
      "message": "Processing repository..."
    },
    ...
  ]
}
```

---

### File Endpoints

#### Upload File

```
POST /api/file/upload
```

Upload a CSV file (multipart/form-data).

**Form Data:**
- `file`: The CSV file

**Response:**
```json
{
  "success": true,
  "message": "File 'github.csv' uploaded successfully",
  "filepath": "/path/to/uploaded/file.csv"
}
```

#### Validate Input Folder

```
POST /api/file/validate/input
```

Validate an input folder path.

**Request Body:**
```json
{
  "path": "/path/to/repos"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Valid input folder: /absolute/path/to/repos",
  "path": "/absolute/path/to/repos"
}
```

#### Validate Output Folder

```
POST /api/file/validate/output
```

Validate an output folder path (creates if doesn't exist).

**Request Body:**
```json
{
  "path": "/path/to/results"
}
```

#### Validate CSV

```
POST /api/file/validate/csv
```

Validate a CSV file format.

**Request Body:**
```json
{
  "filepath": "/path/to/file.csv"
}
```

#### Download File

```
GET /api/file/download?filepath=/path/to/file.csv
```

Download a file.

#### List Files

```
GET /api/file/list?directory=/path/to/results
```

List all CSV files in a directory.

**Response:**
```json
{
  "success": true,
  "message": "Found 10 CSV files",
  "files": [
    {
      "filename": "consumer.csv",
      "filepath": "/path/to/consumer.csv",
      "size": 12345,
      "modified": 1697452800.0
    },
    ...
  ]
}
```

---

### Analytics Endpoints

#### Get Summary

```
GET /api/analytics/summary?output_path=/path/to/results
```

Get a summary of analysis results including total counts, projects, and libraries.

**Response:**
```json
{
  "success": true,
  "total_models": 120,
  "consumer_count": 70,
  "producer_count": 50,
  "total_projects": 25,
  "total_libraries": 8,
  "last_analysis_id": "2025-11-24T10:32:01",
  "output_path": "/path/to/results"
}
```

#### Get Consumer/Producer Distribution

```
GET /api/analytics/consumer-producer-distribution?output_path=/path/to/results
```

Get the distribution of consumer and producer models for charts.

**Response:**
```json
{
  "success": true,
  "labels": ["Consumer", "Producer"],
  "counts": [70, 50],
  "percentages": [58.33, 41.67]
}
```

#### Get Top Keywords

```
GET /api/analytics/keywords?output_path=/path/to/results&limit=10
```

Get the top N keywords used in classification.

**Query Parameters:**
- `output_path` (required): Path to results folder
- `limit` (optional, default=10): Maximum keywords to return (1-100)

**Response:**
```json
{
  "success": true,
  "labels": [".predict(", ".fit(", ".no_grad(", ".train("],
  "counts": [30, 25, 18, 12],
  "total_unique_keywords": 45
}
```

#### Get Library Distribution

```
GET /api/analytics/libraries?output_path=/path/to/results&limit=10
```

Get the distribution of ML libraries used.

**Query Parameters:**
- `output_path` (required): Path to results folder
- `limit` (optional, default=10): Maximum libraries to return (1-100)

**Response:**
```json
{
  "success": true,
  "labels": ["tensorflow", "torch", "keras", "sklearn"],
  "counts": [45, 38, 25, 12],
  "total_unique_libraries": 15
}
```

#### Filter Results

```
GET /api/analytics/filter?output_path=/path/to/results&type=consumer&keyword=.predict(&limit=100
```

Get filtered results based on various criteria.

**Query Parameters:**
- `output_path` (required): Path to results folder
- `type` (optional): Filter by 'consumer' or 'producer'
- `keyword` (optional): Filter by specific keyword
- `library` (optional): Filter by specific library
- `project` (optional): Filter by project name (partial match)
- `limit` (optional, default=100): Maximum results to return (1-1000)

**Response:**
```json
{
  "success": true,
  "count": 15,
  "results": [
    {
      "type": "consumer",
      "ProjectName": "TestProject",
      "where": "path/to/file.py",
      "line_number": "42",
      "libraries": "tensorflow",
      "keywords": ".predict("
    },
    ...
  ],
  "filters_applied": {
    "type": "consumer",
    "keyword": ".predict(",
    "library": null,
    "project": null
  }
}
```

#### Analytics Health Check

```
GET /api/analytics/health
```

Health check endpoint for analytics service.

**Response:**
```json
{
  "status": "healthy",
  "service": "Analytics API"
}
```

---

### Results Endpoints

#### List Results

```
GET /api/results/list?output_path=/path/to/results
```

List all result files (consumers and producers).

**Response:**
```json
{
  "success": true,
  "message": "Found 5 consumer and 5 producer files",
  "consumers": [...],
  "producers": [...],
  "all_files": [...]
}
```

#### View CSV

```
GET /api/results/view?filepath=/path/to/file.csv&limit=100&offset=0
```

View the contents of a CSV file with pagination.

**Response:**
```json
{
  "success": true,
  "message": "Retrieved 100 rows",
  "data": {
    "headers": ["col1", "col2", ...],
    "rows": [[...], [...], ...],
    "row_count": 100,
    "column_count": 5,
    "total_rows": 500,
    "has_more": true,
    "offset": 0,
    "limit": 100
  }
}
```

#### Get Statistics

```
GET /api/results/stats?output_path=/path/to/results
```

Get statistics about the results.

**Response:**
```json
{
  "success": true,
  "message": "Statistics retrieved successfully",
  "stats": {
    "total_files": 10,
    "consumer_files": 5,
    "producer_files": 5,
    "total_size": 12345678,
    "total_size_mb": 11.77,
    "latest_file": {...}
  }
}
```

#### Search Results

```
POST /api/results/search
```

Search within CSV results.

**Request Body:**
```json
{
  "filepath": "/path/to/file.csv",
  "query": "search term",
  "column": "column_name"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Found 10 matches",
  "results": {
    "headers": [...],
    "matches": [
      {
        "row_index": 5,
        "row_data": [...]
      },
      ...
    ],
    "match_count": 10,
    "query": "search term",
    "column": "column_name"
  }
}
```

## 🧪 Testing the API

### Using cURL (PowerShell)

```powershell
# Health check
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health" -Method Get

# Start analysis
$body = @{
    input_path = "C:\path\to\repos"
    output_path = "C:\path\to\results"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analysis/start" -Method Post -Body $body -ContentType "application/json"

# Get job status
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/analysis/status/<job_id>" -Method Get
```

### Using Postman

1. Import the API endpoints into Postman
2. Set the base URL to `http://127.0.0.1:5000`
3. Test each endpoint with appropriate request bodies

## 📝 Logging

Logs are automatically created in the `logs/` directory:

- `logs/app.log`: Application logs with timestamps

Log levels can be configured in `config.py` (INFO, DEBUG, WARNING, ERROR).

## 🔒 Security Considerations

### For Production Deployment:

1. **Set a strong SECRET_KEY**:
   ```powershell
   $env:SECRET_KEY = "your-very-secure-random-key"
   ```

2. **Validate file paths**: The API validates all file paths to prevent path traversal attacks

3. **File upload limits**: Max file size is configured in `config.py` (default: 100 MB)

4. **CORS**: Configure allowed origins in `config.py`

5. **HTTPS**: Use a reverse proxy (nginx, Apache) with SSL/TLS in production

## 🐛 Troubleshooting

### Port Already in Use

```powershell
# Use a different port
$env:FLASK_PORT = "8080"
python app.py
```

### Module Not Found

```powershell
# Ensure you're in the correct directory
cd MARK-Tool\MARK-Tool\web_gui

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Errors

- Ensure the application has read/write permissions for:
  - Upload folder (`static/uploads/`)
  - Output folder (specified in analysis)
  - Logs folder (`logs/`)

### Analysis Not Running

1. Check that `exec_analysis.py` exists at the configured path
2. Verify input/output paths are valid
3. Check logs for detailed error messages

## 🔄 Integration with Existing Code

The backend integrates seamlessly with the existing MARK Tool:

- **exec_analysis.py**: Called via subprocess for analysis
- **cloner.py**: Optionally called to clone repositories
- **Results**: Stored in the same CSV format as the desktop GUI

## 📚 Next Steps

### Frontend Development

Once the backend is running, you can:

1. Build a frontend using HTML/CSS/JavaScript
2. Use a framework like React, Vue, or Angular
3. Create templates in the `templates/` directory

### Additional Features

Consider adding:

- User authentication and authorization
- Database for persistent job storage
- WebSocket support for real-time progress updates
- Email notifications on job completion
- Batch analysis support

## 📄 License

This project follows the same license as the MARK-IGES project.

## 👤 Author

Turco Luigi

## 📞 Support

For issues or questions, please refer to the main MARK-IGES repository documentation.
