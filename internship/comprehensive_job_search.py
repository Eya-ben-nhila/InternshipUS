#!/usr/bin/env python3
"""
Comprehensive Job Search - Maximum Jobs, Complete Details
Uses multiple sources to get the most jobs possible with full details
"""

import requests
import json
import time
import re
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from urllib.parse import urlencode, quote_plus
import os
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveJobSearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.jobs = []
        
    def search_jobs(self, query='', location='', job_type='', experience='', remote='', limit=100):
        """
        Comprehensive job search from multiple sources
        Returns maximum number of real job postings
        """
        logger.info(f"Starting comprehensive job search: query='{query}', location='{location}', limit={limit}")
        
        # Clear previous results
        self.jobs = []
        
        # Multiple sources with high limits
        sources = [
            (self.search_remoteok_comprehensive, 50),
            (self.search_stackoverflow_comprehensive, 40),
            (self.search_indeed_comprehensive, 30),
            (self.search_glassdoor_comprehensive, 30),
            (self.search_weworkremotely_comprehensive, 40),
            (self.search_remotebase_comprehensive, 30),
            (self.search_authentic_jobs_comprehensive, 25),
        ]
        
        for source_func, source_limit in sources:
            try:
                logger.info(f"Searching {source_func.__name__} with limit {source_limit}...")
                source_func(query, location, job_type, experience, remote, source_limit)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error in {source_func.__name__}: {e}")
                continue
        
        # Sort by date and relevance
        self.jobs.sort(key=lambda x: (
            x.get('date_posted', ''), 
            x.get('relevance_score', 0)
        ), reverse=True)
        
        # Return limited results
        return self.jobs[:limit]
    
    def search_remoteok_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=50):
        """Comprehensive RemoteOK search with multiple categories"""
        try:
            # Multiple RemoteOK RSS feeds
            rss_urls = [
                "https://remoteok.io/remote-dev-jobs.rss",
                "https://remoteok.io/remote-software-dev-jobs.rss",
                "https://remoteok.io/remote-programming-jobs.rss",
                "https://remoteok.io/remote-jobs.rss",  # General jobs
            ]
            
            for rss_url in rss_urls:
                try:
                    response = self.session.get(rss_url, timeout=10)
                    
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        items = root.findall('.//item')
                        
                        for item in items[:limit//len(rss_urls)]:
                            try:
                                title = item.find('title').text.strip()
                                link = item.find('link').text.strip()
                                description = item.find('description').text.strip()
                                pub_date = item.find('pubDate').text.strip()
                                
                                # Better company parsing
                                company = self.extract_company_from_title(title)
                                job_title = self.extract_job_title(title)
                                
                                # Check if job matches search criteria
                                if query and query.lower() not in job_title.lower():
                                    continue
                                
                                # Clean description
                                clean_description = self.clean_html(description)
                                
                                job = {
                                    'title': job_title,
                                    'company': company,
                                    'location': 'Remote',
                                    'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                                    'url': link,
                                    'salary': self.extract_salary(clean_description),
                                    'date_posted': pub_date,
                                    'source': 'RemoteOK',
                                    'job_type': 'Full-time',
                                    'remote': 'Yes',
                                    'relevance_score': self.calculate_relevance(query, job_title, clean_description)
                                }
                                
                                self.jobs.append(job)
                                
                            except Exception as e:
                                logger.debug(f"Error parsing RemoteOK item: {e}")
                                continue
                                
                except Exception as e:
                    logger.debug(f"Error with RemoteOK URL {rss_url}: {e}")
                    continue
                        
        except Exception as e:
            logger.error(f"Error fetching from RemoteOK: {e}")
    
    def search_stackoverflow_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=40):
        """Comprehensive Stack Overflow search"""
        try:
            rss_url = "https://stackoverflow.com/jobs/feed"
            response = self.session.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                for item in items[:limit]:
                    try:
                        title = item.find('title').text.strip()
                        link = item.find('link').text.strip()
                        description = item.find('description').text.strip()
                        pub_date = item.find('pubDate').text.strip()
                        
                        # Check if job matches search criteria
                        if query and query.lower() not in title.lower():
                            continue
                        
                        # Clean description
                        clean_description = self.clean_html(description)
                        
                        # Extract company
                        company = self.extract_company_from_description(clean_description)
                        
                        job = {
                            'title': title,
                            'company': company,
                            'location': 'Various',
                            'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                            'url': link,
                            'salary': self.extract_salary(clean_description),
                            'date_posted': pub_date,
                            'source': 'StackOverflow',
                            'job_type': 'Full-time',
                            'remote': 'Maybe',
                            'relevance_score': self.calculate_relevance(query, title, clean_description)
                        }
                        
                        self.jobs.append(job)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing Stack Overflow item: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching from Stack Overflow: {e}")
    
    def search_weworkremotely_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=40):
        """Comprehensive We Work Remotely search"""
        try:
            rss_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
            response = self.session.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                for item in items[:limit]:
                    try:
                        title = item.find('title').text.strip()
                        link = item.find('link').text.strip()
                        description = item.find('description').text.strip()
                        pub_date = item.find('pubDate').text.strip()
                        
                        # Check if job matches search criteria
                        if query and query.lower() not in title.lower():
                            continue
                        
                        # Clean description
                        clean_description = self.clean_html(description)
                        
                        # Extract company
                        company = self.extract_company_from_title(title)
                        
                        job = {
                            'title': title,
                            'company': company,
                            'location': 'Remote',
                            'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                            'url': link,
                            'salary': self.extract_salary(clean_description),
                            'date_posted': pub_date,
                            'source': 'WeWorkRemotely',
                            'job_type': 'Full-time',
                            'remote': 'Yes',
                            'relevance_score': self.calculate_relevance(query, title, clean_description)
                        }
                        
                        self.jobs.append(job)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing WeWorkRemotely item: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching from WeWorkRemotely: {e}")
    
    def search_indeed_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=30):
        """Comprehensive Indeed search"""
        try:
            search_query = quote_plus(query) if query else 'developer'
            rss_url = f"https://www.indeed.com/rss?q={search_query}&l={quote_plus(location) if location else 'remote'}"
            
            response = self.session.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                for item in items[:limit]:
                    try:
                        title = item.find('title').text.strip()
                        link = item.find('link').text.strip()
                        description = item.find('description').text.strip()
                        pub_date = item.find('pubDate').text.strip()
                        
                        # Check if job matches search criteria
                        if query and query.lower() not in title.lower():
                            continue
                        
                        # Clean description
                        clean_description = self.clean_html(description)
                        
                        job = {
                            'title': title,
                            'company': 'Various (Indeed)',
                            'location': location or 'Various',
                            'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                            'url': link,
                            'salary': self.extract_salary(clean_description),
                            'date_posted': pub_date,
                            'source': 'Indeed',
                            'job_type': 'Full-time',
                            'remote': 'Maybe',
                            'relevance_score': self.calculate_relevance(query, title, clean_description)
                        }
                        
                        self.jobs.append(job)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing Indeed item: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching from Indeed: {e}")
    
    def search_glassdoor_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=30):
        """Comprehensive Glassdoor search"""
        try:
            search_query = quote_plus(query) if query else 'developer'
            rss_url = f"https://www.glassdoor.com/Job/rss?sc.keyword={search_query}&locT=N&locId=1&jobType=&fromAge=-1&minSalary=0&includeUnknownSalary=false&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0"
            
            response = self.session.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                for item in items[:limit]:
                    try:
                        title = item.find('title').text.strip()
                        link = item.find('link').text.strip()
                        description = item.find('description').text.strip()
                        pub_date = item.find('pubDate').text.strip()
                        
                        # Check if job matches search criteria
                        if query and query.lower() not in title.lower():
                            continue
                        
                        # Clean description
                        clean_description = self.clean_html(description)
                        
                        job = {
                            'title': title,
                            'company': 'Various (Glassdoor)',
                            'location': location or 'Various',
                            'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                            'url': link,
                            'salary': self.extract_salary(clean_description),
                            'date_posted': pub_date,
                            'source': 'Glassdoor',
                            'job_type': 'Full-time',
                            'remote': 'Maybe',
                            'relevance_score': self.calculate_relevance(query, title, clean_description)
                        }
                        
                        self.jobs.append(job)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing Glassdoor item: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching from Glassdoor: {e}")
    
    def search_remotebase_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=30):
        """Comprehensive RemoteBase search"""
        try:
            rss_url = "https://remotebase.io/remote-jobs.rss"
            response = self.session.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                for item in items[:limit]:
                    try:
                        title = item.find('title').text.strip()
                        link = item.find('link').text.strip()
                        description = item.find('description').text.strip()
                        pub_date = item.find('pubDate').text.strip()
                        
                        # Check if job matches search criteria
                        if query and query.lower() not in title.lower():
                            continue
                        
                        # Clean description
                        clean_description = self.clean_html(description)
                        
                        job = {
                            'title': title,
                            'company': 'Remote Company',
                            'location': 'Remote',
                            'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                            'url': link,
                            'salary': self.extract_salary(clean_description),
                            'date_posted': pub_date,
                            'source': 'RemoteBase',
                            'job_type': 'Full-time',
                            'remote': 'Yes',
                            'relevance_score': self.calculate_relevance(query, title, clean_description)
                        }
                        
                        self.jobs.append(job)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing RemoteBase item: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching from RemoteBase: {e}")
    
    def search_authentic_jobs_comprehensive(self, query='', location='', job_type='', experience='', remote='', limit=25):
        """Comprehensive Authentic Jobs search"""
        try:
            rss_url = "https://authenticjobs.com/rss/"
            response = self.session.get(rss_url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')
                
                for item in items[:limit]:
                    try:
                        title = item.find('title').text.strip()
                        link = item.find('link').text.strip()
                        description = item.find('description').text.strip()
                        pub_date = item.find('pubDate').text.strip()
                        
                        # Check if job matches search criteria
                        if query and query.lower() not in title.lower():
                            continue
                        
                        # Clean description
                        clean_description = self.clean_html(description)
                        
                        job = {
                            'title': title,
                            'company': 'Various (Authentic Jobs)',
                            'location': 'Various',
                            'description': clean_description[:600] + '...' if len(clean_description) > 600 else clean_description,
                            'url': link,
                            'salary': self.extract_salary(clean_description),
                            'date_posted': pub_date,
                            'source': 'AuthenticJobs',
                            'job_type': 'Full-time',
                            'remote': 'Maybe',
                            'relevance_score': self.calculate_relevance(query, title, clean_description)
                        }
                        
                        self.jobs.append(job)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing Authentic Jobs item: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching from Authentic Jobs: {e}")
    
    def extract_company_from_title(self, title):
        """Extract company name from job title"""
        patterns = [
            r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s*$|\s*-|\s*\(|\s*Remote)',
            r'-\s*([A-Z][a-zA-Z\s&]+?)(?:\s*$|\s*Remote)',
            r'([A-Z][a-zA-Z\s&]+?)\s*is\s+hiring',
            r'([A-Z][a-zA-Z\s&]+?)\s*seeks',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) > 2 and len(company) < 50:
                    return company
        
        return 'Various Company'
    
    def extract_job_title(self, title):
        """Extract job title from full title"""
        if ' at ' in title:
            return title.split(' at ')[0].strip()
        elif ' - ' in title:
            return title.split(' - ')[0].strip()
        return title
    
    def extract_company_from_description(self, description):
        """Extract company from description"""
        # Look for company patterns in description
        patterns = [
            r'([A-Z][a-zA-Z\s&]+?)\s+is\s+(?:hiring|seeking|looking)',
            r'join\s+([A-Z][a-zA-Z\s&]+?)',
            r'at\s+([A-Z][a-zA-Z\s&]+?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) > 2 and len(company) < 50:
                    return company
        
        return 'Various Company'
    
    def clean_html(self, html_text):
        """Clean HTML tags from text"""
        if not html_text:
            return ""
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        # Remove special characters
        clean_text = clean_text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        
        return clean_text.strip()
    
    def extract_salary(self, description):
        """Extract salary information from description"""
        salary_patterns = [
            r'\$(\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?)\s*(?:USD|k|K)?',
            r'(\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?)\s*(?:USD|k|K)',
            r'salary[:\s]*\$?(\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?)',
            r'pay[:\s]*\$?(\d{1,3}(?:,\d{3})*(?:-\d{1,3}(?:,\d{3})*)?)',
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return f"${match.group(1)}"
        
        return 'Not specified'
    
    def calculate_relevance(self, query, title, description):
        """Calculate relevance score for job matching"""
        if not query:
            return 0
        
        query_lower = query.lower()
        title_lower = title.lower()
        desc_lower = description.lower()
        
        score = 0
        
        # Title match gets highest score
        if query_lower in title_lower:
            score += 10
        
        # Description match gets medium score
        if query_lower in desc_lower:
            score += 5
        
        # Partial matches
        query_words = query_lower.split()
        for word in query_words:
            if len(word) > 3:  # Only consider words longer than 3 chars
                if word in title_lower:
                    score += 2
                if word in desc_lower:
                    score += 1
        
        return score
    
    def get_jobs(self, limit=100):
        """Get all collected jobs"""
        return self.jobs[:limit]
    
    def save_to_json(self, filename='jobs.json'):
        """Save jobs to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.jobs)} jobs to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return None

# Flask API wrapper
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

job_searcher = ComprehensiveJobSearch()

@app.route('/api/jobs', methods=['GET'])
def search_jobs():
    """API endpoint for job search"""
    try:
        # Get query parameters
        query = request.args.get('query', '')
        location = request.args.get('location', '')
        job_type = request.args.get('jobType', '')
        experience = request.args.get('experience', '')
        remote = request.args.get('remote', '')
        limit = int(request.args.get('limit', 100))  # Much higher default limit
        
        logger.info(f"API request: query='{query}', location='{location}', limit={limit}")
        
        # Perform search
        jobs = job_searcher.search_jobs(
            query=query,
            location=location,
            job_type=job_type,
            experience=experience,
            remote=remote,
            limit=limit
        )
        
        # Format response
        response = {
            'data': jobs,
            'meta': {
                'total': len(jobs),
                'query': query,
                'location': location,
                'sources': list(set(job.get('source', 'Unknown') for job in jobs))
            },
            'status': 'success'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'comprehensive-job-search'})

if __name__ == '__main__':
    print("🚀 Starting Comprehensive Job Search API...")
    print("✅ Maximum jobs, complete details, multiple sources")
    print("✅ NO MOCK DATA - Only real job postings")
    print("✅ Sources: RemoteOK, Stack Overflow, WeWorkRemotely, RemoteBase, Authentic Jobs, Indeed, Glassdoor")
    print("🌐 API available at: http://localhost:5000/api/jobs")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
