from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_cors import CORS
import requests
from datetime import datetime, timedelta, timezone
import os
import re
import logging
from bs4 import BeautifulSoup
import json
from searchapi_client import SearchAPIClient
from urllib.parse import quote_plus
import time
import uuid

app = Flask(__name__, template_folder='templates')

# Configure CORS to allow all origins and headers
cors = CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/static/*": {"origins": "*"}
})

# Enable CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Theirstack API configuration
# In production, use environment variables for sensitive data
# Example: os.environ.get('THEIRSTACK_API_KEY')
THEIRSTACK_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJleWFiZW5oaWxhQGdtYWlsLmNvbSIsInBlcm1pc3Npb25zIjoidXNlciIsImNyZWF0ZWRfYXQiOiIyMDI1LTA3LTI5VDEyOjI3OjA5LjE0MTcxNiswMDowMCJ9.4ZCd9jMzAX_6IHGwcX1NDFMLSO0rqnOwx1vRxSiTYpI'
THEIRSTACK_API_URL = 'https://api.theirstack.com/v1'  # Update with actual API URL if different

# Theirstack API Client
def theirstack_search_jobs(query, location='', page=1, per_page=10):
    """Search for jobs using Theirstack API"""
    try:
        headers = {
            'Authorization': f'Bearer {THEIRSTACK_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        params = {
            'query': query,
            'page': page,
            'per_page': per_page
        }
        
        if location:
            params['location'] = location
        
        logging.info(f"Making request to Theirstack API with params: {params}")
        
        response = requests.get(
            f"{THEIRSTACK_API_URL}/jobs",
            headers=headers,
            params=params,
            timeout=10
        )
        
        logging.info(f"Theirstack API response status: {response.status_code}")
        logging.info(f"Response headers: {dict(response.headers)}")
        
        # Log the first 500 chars of the response for debugging
        response_text = response.text
        logging.info(f"Response text (first 500 chars): {response_text[:500]}")
        
        response.raise_for_status()
        
        result = response.json()
        logging.info(f"Successfully parsed response. Data keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Theirstack API: {str(e)}", exc_info=True)
        if 'response' in locals():
            try:
                error_response = response.json()
                logging.error(f"Error response: {error_response}")
            except:
                logging.error(f"Could not parse error response. Status: {response.status_code}, Text: {response.text}")
        return None

# SearchAPI.io client (keeping as fallback)
SEARCHAPI_KEY = 'eo5c5me2HM9P6BFAuSmdpvZb'
searchapi_client = SearchAPIClient(SEARCHAPI_KEY)


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

@app.route('/')
def index():
    return redirect(url_for('job_search'))

@app.route('/search')
def job_search():
    return render_template('job_search.html')

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify frontend-backend connection"""
    print("\n=== Test endpoint called ===")
    print("Request headers:", dict(request.headers))
    print("Request args:", request.args)
    print("Request data:", request.get_data())
    print("Request form:", request.form)
    print("Request json:", request.json)
    print("Request method:", request.method)
    print("Request url:", request.url)
    print("Request remote_addr:", request.remote_addr)
    print("Request user_agent:", request.user_agent)
    print("Request referrer:", request.referrer)
    print("Request cookies:", request.cookies)
    print("=== End test endpoint ===\n")
    
    return jsonify({
        'status': 'success',
        'message': 'Test endpoint is working',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'request_headers': dict(request.headers),
        'request_args': dict(request.args)
    })

# Theirstack-like API endpoints

@app.route('/location', methods=['GET'])
def location_lookup():
    """Simple location lookup endpoint"""
    zip_code = request.args.get('zip', '')
    return jsonify({
        'city': zip_code if zip_code else 'Unknown',
        'country': 'United Kingdom',
        'postal_code': zip_code,
        'status': 'success'
    })

@app.route('/api/geolocate', methods=['GET'])
def geolocate():
    """Mimic Theirstack's geolocation endpoint"""
    return jsonify({
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5074,
        'longitude': -0.1278,
        'ip': request.remote_addr
    })

@app.route('/api/statistics', methods=['GET'])
def statistics():
    """Mimic Theirstack's statistics endpoint"""
    return jsonify({
        'total_jobs': 1500000,
        'total_companies': 50000,
        'last_updated': datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/saved_searches', methods=['GET'])
def saved_searches():
    """Mimic Theirstack's saved searches endpoint"""
    return jsonify({
        'data': [],
        'meta': {
            'total': 0,
            'per_page': 10,
            'current_page': 1,
            'total_pages': 0
        }
    })

@app.route('/api/search', methods=['GET'])
def theirstack_search():
    """Mimic Theirstack's main search endpoint"""
    try:
        # Get query parameters
        query = request.args.get('q', '')
        location = request.args.get('location', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Call SearchAPI
        result = searchapi_client.search_jobs(
            query=query,
            location=location,
            num_results=per_page
        )
        
        # Format jobs in Theirstack format
        jobs = []
        if result and 'jobs_results' in result:
            for job in result['jobs_results']:
                jobs.append({
                    'id': job.get('job_id', str(uuid.uuid4())),
                    'title': job.get('title', 'No title'),
                    'company': job.get('company_name', 'No company'),
                    'location': job.get('location', 'Location not specified'),
                    'description': clean_html(' '.join(job.get('description', [])) if isinstance(job.get('description'), list) 
                                          else job.get('description', '')),
                    'job_type': job.get('job_type', 'Full-time'),
                    'url': job.get('related_links', [{}])[0].get('link', '#') if job.get('related_links') else '#',
                    'company_logo': job.get('thumbnail', 'https://via.placeholder.com/100'),
                    'date_posted': job.get('detected_extensions', {}).get('posted_at', datetime.now(timezone.utc).isoformat()),
                    'is_remote': 'remote' in (job.get('location', '') + ' ' + job.get('title', '')).lower()
                })
        
        # Create Theirstack-like response
        response_data = {
            'data': jobs,
            'meta': {
                'current_page': page,
                'per_page': per_page,
                'total': len(jobs) * 10,  # Estimate total
                'total_pages': 10,  # Estimate pages
                'query': query,
                'location': location
            },
            'status': 'success'
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logging.error(f"Error in theirstack_search: {str(e)}", exc_info=True)
        return jsonify({
            'data': [],
            'meta': {
                'current_page': 1,
                'per_page': 10,
                'total': 0,
                'total_pages': 0,
                'query': '',
                'location': ''
            },
            'status': 'error',
            'message': str(e)
        }), 500

# Keep the old endpoint for backward compatibility
@app.route('/api/jobs', methods=['GET', 'OPTIONS'])
def search_jobs():
    # CORS headers
    response_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return ('', 204, response_headers)
    
    try:
        # Log the incoming request
        logging.info("=== New Search Request ===")
        logging.info(f"URL: {request.url}")
        logging.info(f"Headers: {dict(request.headers)}")
        logging.info(f"Args: {dict(request.args)}")
        
        # Get query parameters with fallbacks
        query = request.args.get('query', request.args.get('search', request.args.get('q', '')))
        location = request.args.get('location', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        logging.info(f"Processing search - query: '{query}', location: '{location}', page: {page}, per_page: {per_page}")
        
        # Call Theirstack API
        try:
            logging.info("Calling Theirstack API...")
            result = theirstack_search_jobs(
                query=query,
                location=location,
                page=page,
                per_page=per_page
            )
            
            if not result:
                logging.warning("No results from Theirstack API")
                return jsonify({
                    'data': [],
                    'meta': {
                        'current_page': page,
                        'per_page': per_page,
                        'total': 0,
                        'total_pages': 0,
                        'query': query,
                        'location': location
                    },
                    'status': 'success'
                }), 200, response_headers
                
            logging.info(f"Received {len(result.get('data', []))} jobs from Theirstack API")
            
            # Format response to match frontend expectations
            response_data = {
                'data': result.get('data', []),
                'meta': result.get('meta', {
                    'current_page': page,
                    'per_page': per_page,
                    'total': 0,
                    'total_pages': 0,
                    'query': query,
                    'location': location
                }),
                'status': 'success'
            }
            
            return jsonify(response_data), 200, response_headers
            
        except Exception as api_error:
            logging.error(f"Error in search_jobs: {str(api_error)}", exc_info=True)
            
            # Return a proper error response
            error_response = {
                'data': [],
                'meta': {
                    'current_page': page,
                    'per_page': per_page,
                    'total': 0,
                    'total_pages': 0,
                    'query': query,
                    'location': location
                },
                'status': 'error',
                'message': str(api_error)
            }
            
            return jsonify(error_response), 500, response_headers
        
        # Format the response
        formatted_jobs = []
        for job in result['jobs_results']:
            # Extract job details
            job_id = job.get('job_id', '')
            title = job.get('title', 'No title')
            company = job.get('company_name', 'No company')
            job_location = job.get('location', 'Location not specified')
            
            # Handle job type (can be string or list)
            job_type = job.get('job_type', [])
            if isinstance(job_type, list):
                job_type = ', '.join(job_type) if job_type else 'Not specified'
            
            # Get description (handle both string and list formats)
            description = job.get('description', '')
            if isinstance(description, list):
                description = ' '.join(description)
            
            # Get apply link
            related_links = job.get('related_links', [])
            apply_url = related_links[0].get('link', '#') if related_links else '#'
            
            formatted_jobs.append({
                'id': job_id or str(hash(f"{title}{company}")),
                'title': title,
                'company': company,
                'location': job_location,
                'type': job_type,
                'description': clean_html(description),
                'how_to_apply': f"Apply at {apply_url}" if apply_url != '#' else "",
                'company_logo': job.get('thumbnail', 'https://via.placeholder.com/100'),
                'created_at': datetime.utcnow().isoformat(),
                'url': apply_url
            })
        
        return jsonify(formatted_jobs)
        
    except Exception as e:
        print(f"Error in search_jobs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch jobs', 'jobs': []}), 500

@app.route('/api/job/<job_id>', methods=['GET'])
def get_job(job_id):
    try:
        # For now, we'll just return the first job from the search results
        # since the SearchAPI doesn't have a direct job detail endpoint
        search = request.args.get('search', '')
        location = request.args.get('location', '')
        
        # Search for jobs to find the matching one
        result = searchapi_client.search_jobs(
            query=search,
            location=location,
            num_results=50  # Search more to find the specific job
        )
        
        if not result or 'jobs_results' not in result:
            return jsonify({'error': 'Job not found'}), 404
        
        # Try to find the job with matching ID
        matching_job = None
        for job in result['jobs_results']:
            if str(job.get('job_id', '')) == job_id or \
               str(hash(f"{job.get('title', '')}{job.get('company_name', '')}")) == job_id:
                matching_job = job
                break
        
        if not matching_job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Format the job details
        job = matching_job
        related_links = job.get('related_links', [])
        apply_url = related_links[0].get('link', '#') if related_links else '#'
        
        # Handle job type
        job_type = job.get('job_type', [])
        if isinstance(job_type, list):
            job_type = ', '.join(job_type) if job_type else 'Not specified'
        
        # Handle description
        description = job.get('description', '')
        if isinstance(description, list):
            description = ' '.join(description)
        
        formatted_job = {
            'id': job.get('job_id', job_id),
            'title': job.get('title', 'No title'),
            'company': job.get('company_name', 'No company'),
            'location': job.get('location', 'Location not specified'),
            'type': job_type,
            'description': clean_html(description),
            'how_to_apply': f"Apply at {apply_url}" if apply_url != '#' else "",
            'company_logo': job.get('thumbnail', 'https://via.placeholder.com/100'),
            'created_at': datetime.utcnow().isoformat(),
            'url': apply_url
        }
        
        return jsonify(formatted_job)
        
    except Exception as e:
        print(f"Error in get_job: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Create basic HTML template if it doesn't exist
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Search</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
    <style>
        body {
            padding: 20px;
            background-color: #f5f5f5;
        }
        .search-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .job-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .company-logo {
            max-width: 100px;
            max-height: 50px;
            margin-right: 15px;
        }
        .job-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #2185d0;
            margin-bottom: 5px;
        }
        .company-name {
            font-weight: bold;
            color: #333;
        }
        .job-meta {
            color: #666;
            font-size: 0.9em;
            margin: 5px 0;
        }
        .job-description {
            margin: 15px 0;
            color: #444;
            line-height: 1.5;
        }
        .view-job-btn {
            margin-top: 10px;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="ui container">
        <h1 class="ui header">Job Search</h1>
        
        <div class="search-container">
            <form id="searchForm" class="ui form">
                <div class="field">
                    <label>Job Title or Keywords</label>
                    <input type="text" name="query" placeholder="e.g. software engineer">
                </div>
                <div class="two fields">
                    <div class="field">
                        <label>Location</label>
                        <input type="text" name="location" placeholder="City, State, or Remote">
                    </div>
                    <div class="field">
                        <div class="ui checkbox">
                            <input type="checkbox" name="full_time" value="true">
                            <label>Full-time only</label>
                        </div>
                    </div>
                </div>
                <button class="ui primary button" type="submit">Search Jobs</button>
            </form>
        </div>
        
        <div id="loading" class="ui active inverted dimmer">
            <div class="ui text loader">Searching for jobs...</div>
        </div>
        
        <div id="results">
            <!-- Results will be inserted here -->
        </div>
        
        <div id="no-results" class="no-results" style="display: none;">
            <h3>No jobs found</h3>
            <p>Try adjusting your search criteria</p>
        </div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
    <script>
        // Global state
        const AppState = {
            currentPage: 1,
            perPage: 10,
            totalResults: 0,
            totalPages: 1,
            isLoading: false,
            currentSearch: {
                query: '',
                location: ''
            }
        };
        
        // Initialize the application
        $(document).ready(function() {
            console.log('Initializing Theirstack-like job search...');
            
            // Initialize UI components
            $('.ui.dropdown').dropdown();
            $('.ui.checkbox').checkbox();
            
            // Load user's location
            detectLocation();
            
            // Set up event listeners
            $('#searchForm').on('submit', handleSearch);
            $('#loadMore').on('click', loadMoreJobs);
            
            // Load stats
            loadStats();
        });
        
        // Detect user's location
        function detectLocation() {
            $.get('/api/geolocate')
                .done(function(data) {
                    if (data && data.city) {
                        $('input[name="location"]').val(data.city);
                    }
                })
                .fail(console.error);
        }
        
        // Load statistics
        function loadStats() {
            $.get('/api/statistics')
                .done(function(data) {
                    if (data) {
                        $('.stats-jobs').text(formatNumber(data.total_jobs));
                        $('.stats-companies').text(formatNumber(data.total_companies));
                    }
                })
                .fail(console.error);
        }
        
        // Handle search form submission
        function handleSearch(e) {
            e.preventDefault();
            
            // Update search state
            AppState.currentPage = 1;
            AppState.currentSearch = {
                query: $('input[name="query"]').val().trim(),
                location: $('input[name="location"]').val().trim()
            };
            
            // Clear previous results
            $('#jobResults').empty();
            $('#noResults').addClass('hidden');
            
            // Show loading state
            setLoading(true);
            
            // Perform search
            searchJobs();
        }
        
        // Load more jobs (pagination)
        function loadMoreJobs() {
            if (AppState.isLoading || AppState.currentPage >= AppState.totalPages) return;
            
            AppState.currentPage++;
            setLoading(true);
            searchJobs();
        }
        
        // Search for jobs
        function searchJobs() {
            const { query, location } = AppState.currentSearch;
            
            // Show loading state
            setLoading(true);
            
            // Make API request
            $.ajax({
                url: '/api/search',
                method: 'GET',
                data: {
                    q: query,
                    location: location,
                    page: AppState.currentPage,
                    per_page: AppState.perPage
                },
                dataType: 'json'
            })
            .done(function(response) {
                if (response.status === 'success') {
                    // Update pagination info
                    AppState.totalResults = response.meta.total;
                    AppState.totalPages = response.meta.total_pages;
                    
                    // Render jobs
                    if (response.data && response.data.length > 0) {
                        renderJobs(response.data);
                        updatePagination();
                    } else {
                        showNoResults();
                    }
                } else {
                    showError('Failed to load jobs. Please try again.');
                }
            })
            .fail(function(xhr, status, error) {
                console.error('Search error:', status, error);
                showError('Error connecting to the server. Please check your connection.');
            })
            .always(function() {
                setLoading(false);
            });
        }
        
        // Render job listings
        function renderJobs(jobs) {
            const $container = $('#jobResults');
            
            jobs.forEach(function(job) {
                const jobHtml = `
                    <div class="job-card">
                        <div class="job-header">
                            <img src="${job.company_logo || 'https://via.placeholder.com/50'}" 
                                 alt="${job.company}" 
                                 class="company-logo">
                            <div class="job-meta">
                                <h3 class="job-title">${job.title}</h3>
                                <div class="company-name">${job.company}</div>
                                <div class="job-location">
                                    <i class="map marker alternate icon"></i>
                                    ${job.location}
                                    ${job.is_remote ? '<span class="remote-tag">Remote</span>' : ''}
                                </div>
                            </div>
                        </div>
                        <div class="job-description">
                            ${job.description.substring(0, 200)}${job.description.length > 200 ? '...' : ''}
                        </div>
                        <div class="job-footer">
                            <span class="job-type">${job.job_type || 'Full-time'}</span>
                            <span class="job-posted">Posted ${formatDate(job.date_posted)}</span>
                            <a href="${job.url}" target="_blank" class="ui primary button">
                                Apply Now
                            </a>
                        </div>
                    </div>
                `;
                
                $container.append(jobHtml);
            });
        }
        
        // Update pagination controls
        function updatePagination() {
            const $loadMore = $('#loadMore');
            
            if (AppState.currentPage < AppState.totalPages) {
                $loadMore.removeClass('hidden');
                $loadMore.find('.text')
                    .text(`Load More (${AppState.currentPage}/${AppState.totalPages})`);
            } else {
                $loadMore.addClass('hidden');
            }
            
            // Update result count
            const showing = Math.min(AppState.currentPage * AppState.perPage, AppState.totalResults);
            $('.results-count').text(`Showing ${showing} of ${AppState.totalResults} jobs`);
        }
        
        // Show no results message
        function showNoResults() {
            $('#noResults').removeClass('hidden');
            $('#loadMore').addClass('hidden');
        }
        
        // Show error message
        function showError(message) {
            const $error = $('.error-message');
            $error.text(message).removeClass('hidden');
            setTimeout(() => $error.addClass('hidden'), 5000);
        }
        
        // Set loading state
        function setLoading(isLoading) {
            AppState.isLoading = isLoading;
            const $button = $('#searchButton');
            const $loadMore = $('#loadMore');
            
            if (isLoading) {
                $button.addClass('loading');
                $loadMore.addClass('loading');
            } else {
                $button.removeClass('loading');
                $loadMore.removeClass('loading');
            }
        }
        
        // Helper: Format date
        function formatDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
        }
        
        // Helper: Format large numbers
        function formatNumber(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        $(document).ready(function() {
            // Initialize checkboxes
            $('.ui.checkbox').checkbox();
            
            // Hide loading indicator initially
            $('#loading').dimmer('hide');
            
            // Handle form submission
            $('#searchForm').on('submit', function(e) {
                e.preventDefault();
                
                // Get form data
                const formData = $(this).serialize();
                const query = $('input[name="query"]').val();
                const location = $('input[name="location"]').val();
                
                console.log('Form submitted with data:', { query, location });
                
                // Show loading indicator
                $('#loading').dimmer({
                    onShow: function() {
                        console.log('Showing loading indicator');
                    },
                    onHide: function() {
                        console.log('Hiding loading indicator');
                    }
                }).dimmer('show');
                
                // Clear previous results
                $('#results').empty();
                $('#no-results').hide();
                
                console.log('Making API request to /api/jobs with params:', formData);
                
                // Make API request with timeout
                const request = $.ajax({
                    url: '/api/jobs',
                    method: 'GET',
                    data: formData,
                    dataType: 'json',
                    timeout: 30000, // 30 second timeout
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                request.done(function(data, status, xhr) {
                    console.log('API request successful');
                    console.log('Status:', status);
                    console.log('Response data:', data);
                    
                    if (data && Array.isArray(data) && data.length > 0) {
                        console.log(`Rendering ${data.length} jobs`);
                        renderJobs(data);
                    } else {
                        console.log('No jobs found, showing no-results message');
                        $('#no-results').show();
                    }
                });
                
                request.fail(function(xhr, status, error) {
                    console.error('API request failed');
                    console.error('Status:', status);
                    console.error('Error:', error);
                    console.error('Response text:', xhr.responseText);
                    
                    let errorMessage = 'Error searching for jobs. ';
                    
                    if (status === 'timeout') {
                        errorMessage += 'The request timed out. Please try again.';
                    } else if (xhr.responseText) {
                        try {
                            const errorData = JSON.parse(xhr.responseText);
                            errorMessage += errorData.message || errorData.error || 'Unknown error';
                        } catch (e) {
                            errorMessage += xhr.responseText;
                        }
                    } else {
                        errorMessage += 'Please check your connection and try again.';
                    }
                    
                    console.error('Error details:', errorMessage);
                    alert(errorMessage);
                });
                
                request.always(function() {
                    console.log('API request completed, hiding loading indicator');
                    $('#loading').dimmer('hide');
                });
            });
            
            // Render job listings
            function renderJobs(jobs) {
                const $results = $('#results');
                $results.empty();
                
                jobs.forEach(function(job) {
                    const jobHtml = `
                        <div class="job-card">
                            <div class="ui grid">
                                <div class="two wide column">
                                    <img src="${job.company_logo}" alt="${job.company}" class="company-logo">
                                </div>
                                <div class="fourteen wide column">
                                    <h3 class="job-title">${job.title}</h3>
                                    <div class="company-name">${job.company}</div>
                                    <div class="job-meta">
                                        <i class="map marker alternate icon"></i> ${job.location} • 
                                        <i class="briefcase icon"></i> ${job.type}
                                    </div>
                                    <div class="job-description">
                                        ${job.description.substring(0, 250)}${job.description.length > 250 ? '...' : ''}
                                    </div>
                                    <div class="view-job-btn">
                                        <a href="${job.url}" target="_blank" class="ui primary button">
                                            View Job
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    $results.append(jobHtml);
                });
            }
            
            // Trigger search on page load if there are search parameters
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('search') || urlParams.has('location')) {
                $('#searchForm').submit();
            }
        });
    </script>
</body>
</html>
""")
    
    # Run the application
    try:
        app.run(debug=True, port=5000, use_reloader=False)
    except OSError as e:
        if e.winerror == 10038:  # Handle Windows socket error
            print("\nServer restarting...")
            app.run(debug=True, port=5000, use_reloader=False)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
