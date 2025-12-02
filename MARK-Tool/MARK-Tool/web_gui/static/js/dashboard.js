/**
 * Dashboard Module - Analytics and Charts
 * Handles Chart.js integration and analytics data visualization
 */

class AnalyticsDashboard {
    constructor() {
        this.outputPath = null;
        this.charts = {
            pie: null,
            bar: null,
            keywords: null,
            libraries: null
        };
        
        // Chart colors
        this.colors = {
            consumer: 'rgba(54, 162, 235, 0.8)',
            producer: 'rgba(255, 99, 132, 0.8)',
            other: 'rgba(201, 203, 207, 0.8)',
            consumerBorder: 'rgba(54, 162, 235, 1)',
            producerBorder: 'rgba(255, 99, 132, 1)',
            otherBorder: 'rgba(201, 203, 207, 1)',
            keywords: [
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(201, 203, 207, 0.8)'
            ]
        };
    }

    /**
     * Initialize the dashboard with output path
     */
    init(outputPath) {
        if (!outputPath) {
            this.showError('No output path specified. Please run an analysis or specify an output path.');
            return;
        }
        
        this.outputPath = outputPath;
        // Clear any previous alerts
        this.clearAlerts();
        this.loadAllAnalytics();
    }

    /**
     * Load all analytics data
     */
    async loadAllAnalytics() {
        try {
            await Promise.all([
                this.loadSummary(),
                this.loadDistribution(),
                this.loadKeywords(),
                this.loadLibraries()
            ]);
        } catch (error) {
            console.error('Error loading analytics:', error);
            // Check if it's a CSV not found error
            if (error.message && (error.message.includes('No consumer') || error.message.includes('CSV files'))) {
                this.showError('No analysis results found in the specified output path or its subdirectories. Please run an analysis first.');
            } else {
                this.showError('Failed to load analytics data: ' + error.message);
            }
        }
    }

    /**
     * Load summary statistics
     */
    async loadSummary() {
        try {
            const response = await fetch(`/api/analytics/summary?output_path=${encodeURIComponent(this.outputPath)}`);
            const data = await response.json();

            if (data.success) {
                this.updateSummaryCards(data);
            } else {
                throw new Error(data.message || 'Failed to load summary');
            }
        } catch (error) {
            // Only log to console once, not throw to avoid duplicate error messages
            console.error('Error loading summary:', error);
            throw error;
        }
    }

    /**
     * Update summary cards with data
     */
    updateSummaryCards(data) {
        // Update total models
        const totalEl = document.getElementById('total-models');
        if (totalEl) totalEl.textContent = data.total_models || 0;

        // Update consumer count
        const consumerEl = document.getElementById('consumer-count');
        if (consumerEl) consumerEl.textContent = data.consumer_count || 0;

        // Update producer count
        const producerEl = document.getElementById('producer-count');
        if (producerEl) producerEl.textContent = data.producer_count || 0;

        // Update projects count
        const projectsEl = document.getElementById('total-projects');
        if (projectsEl) projectsEl.textContent = data.total_projects || 0;

        // Update libraries count
        const librariesEl = document.getElementById('total-libraries');
        if (librariesEl) librariesEl.textContent = data.total_libraries || 0;

        // Update last analysis timestamp
        const timestampEl = document.getElementById('last-analysis');
        if (timestampEl && data.last_analysis_id) {
            timestampEl.textContent = new Date(data.last_analysis_id).toLocaleString();
        }
    }

    /**
     * Load consumer/producer distribution
     */
    async loadDistribution() {
        try {
            const response = await fetch(`/api/analytics/consumer-producer-distribution?output_path=${encodeURIComponent(this.outputPath)}`);
            const data = await response.json();

            if (data.success) {
                this.createPieChart(data);
                this.createBarChart(data);
            } else {
                throw new Error(data.message || 'Failed to load distribution');
            }
        } catch (error) {
            // Silently fail for individual chart loading, main error handler will show message
            throw error;
        }
    }

    /**
     * Create pie chart for consumer/producer distribution
     */
    createPieChart(data) {
        const ctx = document.getElementById('pieChart');
        if (!ctx) return;

        // Destroy existing chart
        if (this.charts.pie) {
            this.charts.pie.destroy();
        }

        // Prepare colors
        const backgroundColors = data.labels.map(label => {
            if (label.toLowerCase().includes('consumer')) return this.colors.consumer;
            if (label.toLowerCase().includes('producer')) return this.colors.producer;
            return this.colors.other;
        });

        const borderColors = data.labels.map(label => {
            if (label.toLowerCase().includes('consumer')) return this.colors.consumerBorder;
            if (label.toLowerCase().includes('producer')) return this.colors.producerBorder;
            return this.colors.otherBorder;
        });

        // Create chart
        this.charts.pie = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.percentages,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: { size: 12 }
                        }
                    },
                    title: {
                        display: true,
                        text: 'Consumer vs Producer Distribution (%)',
                        font: { size: 16, weight: 'bold' },
                        padding: { bottom: 20 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value.toFixed(2)}%`;
                            }
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const label = data.labels[index];
                        this.filterByType(label.toLowerCase());
                    }
                }
            }
        });
    }

    /**
     * Create bar chart for consumer/producer counts
     */
    createBarChart(data) {
        const ctx = document.getElementById('barChart');
        if (!ctx) return;

        // Destroy existing chart
        if (this.charts.bar) {
            this.charts.bar.destroy();
        }

        // Prepare colors
        const backgroundColors = data.labels.map(label => {
            if (label.toLowerCase().includes('consumer')) return this.colors.consumer;
            if (label.toLowerCase().includes('producer')) return this.colors.producer;
            return this.colors.other;
        });

        const borderColors = data.labels.map(label => {
            if (label.toLowerCase().includes('consumer')) return this.colors.consumerBorder;
            if (label.toLowerCase().includes('producer')) return this.colors.producerBorder;
            return this.colors.otherBorder;
        });

        // Create chart
        this.charts.bar = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Count',
                    data: data.counts,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Consumer vs Producer Counts',
                        font: { size: 16, weight: 'bold' },
                        padding: { bottom: 20 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Count: ${context.parsed.y}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const label = data.labels[index];
                        this.filterByType(label.toLowerCase());
                    }
                }
            }
        });
    }

    /**
     * Load keywords distribution
     */
    async loadKeywords(limit = 10) {
        try {
            const response = await fetch(`/api/analytics/keywords?output_path=${encodeURIComponent(this.outputPath)}&limit=${limit}`);
            const data = await response.json();

            if (data.success) {
                this.createKeywordsChart(data);
            } else {
                throw new Error(data.message || 'Failed to load keywords');
            }
        } catch (error) {
            // Silently fail for individual chart loading, main error handler will show message
            throw error;
        }
    }

    /**
     * Create horizontal bar chart for keywords
     */
    createKeywordsChart(data) {
        const ctx = document.getElementById('keywordsChart');
        if (!ctx) return;

        // Destroy existing chart
        if (this.charts.keywords) {
            this.charts.keywords.destroy();
        }

        // Create chart
        this.charts.keywords = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Frequency',
                    data: data.counts,
                    backgroundColor: this.colors.keywords,
                    borderColor: this.colors.keywords.map(c => c.replace('0.8', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: `Top ${data.labels.length} Keywords Used in Classification`,
                        font: { size: 16, weight: 'bold' },
                        padding: { bottom: 20 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Frequency: ${context.parsed.x}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const keyword = data.labels[index];
                        this.filterByKeyword(keyword);
                    }
                }
            }
        });
    }

    /**
     * Load libraries distribution
     */
    async loadLibraries(limit = 10) {
        try {
            const response = await fetch(`/api/analytics/libraries?output_path=${encodeURIComponent(this.outputPath)}&limit=${limit}`);
            const data = await response.json();

            if (data.success) {
                this.createLibrariesChart(data);
            } else {
                throw new Error(data.message || 'Failed to load libraries');
            }
        } catch (error) {
            // Silently fail for individual chart loading, main error handler will show message
            throw error;
        }
    }

    /**
     * Create chart for library distribution
     */
    createLibrariesChart(data) {
        const ctx = document.getElementById('librariesChart');
        if (!ctx) return;

        // Destroy existing chart
        if (this.charts.libraries) {
            this.charts.libraries.destroy();
        }

        // Create chart
        this.charts.libraries = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Count',
                    data: data.counts,
                    backgroundColor: this.colors.keywords,
                    borderColor: this.colors.keywords.map(c => c.replace('0.8', '1')),
                    borderWidth: 2
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: `Top ${data.labels.length} ML Libraries Used`,
                        font: { size: 16, weight: 'bold' },
                        padding: { bottom: 20 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Count: ${context.parsed.x}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        }
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const library = data.labels[index];
                        this.filterByLibrary(library);
                    }
                }
            }
        });
    }

    /**
     * Filter results by type (consumer/producer)
     */
    async filterByType(type) {
        try {
            const filterType = type.includes('consumer') ? 'consumer' : 
                              type.includes('producer') ? 'producer' : null;
            
            if (!filterType) return;

            console.log(`Filtering by type: ${filterType}`);
            
            // Call filter endpoint
            const response = await fetch(
                `/api/analytics/filter?output_path=${encodeURIComponent(this.outputPath)}&type=${filterType}`
            );
            const data = await response.json();

            if (data.success) {
                this.displayFilteredResults(data, { type: filterType });
            }
        } catch (error) {
            console.error('Error filtering by type:', error);
            this.showError('Failed to filter results');
        }
    }

    /**
     * Filter results by keyword
     */
    async filterByKeyword(keyword) {
        try {
            console.log(`Filtering by keyword: ${keyword}`);
            
            // Call filter endpoint
            const response = await fetch(
                `/api/analytics/filter?output_path=${encodeURIComponent(this.outputPath)}&keyword=${encodeURIComponent(keyword)}`
            );
            const data = await response.json();

            if (data.success) {
                this.displayFilteredResults(data, { keyword });
            }
        } catch (error) {
            console.error('Error filtering by keyword:', error);
            this.showError('Failed to filter results');
        }
    }

    /**
     * Filter results by library
     */
    async filterByLibrary(library) {
        try {
            console.log(`Filtering by library: ${library}`);
            
            // Call filter endpoint
            const response = await fetch(
                `/api/analytics/filter?output_path=${encodeURIComponent(this.outputPath)}&library=${encodeURIComponent(library)}`
            );
            const data = await response.json();

            if (data.success) {
                this.displayFilteredResults(data, { library });
            }
        } catch (error) {
            console.error('Error filtering by library:', error);
            this.showError('Failed to filter results');
        }
    }

    /**
     * Display filtered results
     */
    displayFilteredResults(data, filters) {
        // Create modal or update results table
        const modalEl = document.getElementById('filteredResultsModal');
        
        if (modalEl) {
            // Update modal content
            const titleEl = modalEl.querySelector('.modal-title');
            const bodyEl = modalEl.querySelector('.modal-body');
            
            // Build filter description
            const filterDesc = Object.entries(filters)
                .map(([key, value]) => `${key}: ${value}`)
                .join(', ');
            
            titleEl.textContent = `Filtered Results (${data.count} items) - ${filterDesc}`;
            
            // Build results table
            let html = `
                <p class="text-muted">Showing ${data.count} results matching filters: ${filterDesc}</p>
                <div class="table-responsive">
                    <table class="table table-sm table-striped">
                        <thead>
                            <tr>
                                <th>Project</th>
                                <th>File</th>
                                <th>Line</th>
                                <th>Libraries</th>
                                <th>Keywords</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.results.forEach(result => {
                html += `
                    <tr>
                        <td>${result.ProjectName || result.project || 'N/A'}</td>
                        <td>${result.where || result.file || 'N/A'}</td>
                        <td>${result.line_number || result.line || 'N/A'}</td>
                        <td>${result.libraries || result.library || 'N/A'}</td>
                        <td>${result.keywords || result.keyword || 'N/A'}</td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                    </table>
                </div>
            `;
            
            bodyEl.innerHTML = html;
            
            // Show modal
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        } else {
            console.warn('Filtered results modal not found');
            // Optionally dispatch event for other components to handle
            window.dispatchEvent(new CustomEvent('filtered-results', { 
                detail: { data, filters } 
            }));
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        const alertEl = document.getElementById('dashboard-alert');
        if (alertEl) {
            alertEl.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Error:</strong> ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        } else {
            console.error(message);
        }
    }

    /**
     * Clear alerts
     */
    clearAlerts() {
        const alertEl = document.getElementById('dashboard-alert');
        if (alertEl) {
            alertEl.innerHTML = '';
        }
    }

    /**
     * Destroy all charts
     */
    destroyCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {
            pie: null,
            bar: null,
            keywords: null,
            libraries: null
        };
    }

    /**
     * Refresh dashboard with new output path
     */
    refresh(outputPath) {
        this.destroyCharts();
        this.init(outputPath);
    }
}

// Export for use in other modules
window.AnalyticsDashboard = AnalyticsDashboard;
