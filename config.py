#!/usr/bin/env python3
"""
Configuration file for LinkedIn Job Scraper
Customize your scraping settings and search parameters here.
"""

import os
from typing import Dict, List, Any

# Browser Configuration
BROWSER_CONFIG = {
    "headless": False,  # Set to True for headless mode (faster, no GUI)
    "use_undetected": True,  # Use undetected-chromedriver for better anti-detection
    "window_size": "1920,1080",  # Browser window size
    "timeout": 30,  # Page load timeout in seconds
}

# Rate Limiting Configuration (to avoid getting blocked)
RATE_LIMITING = {
    "min_delay": 2,  # Minimum delay between actions (seconds)
    "max_delay": 5,  # Maximum delay between actions (seconds)
    "scroll_delay_min": 1,  # Minimum delay between page scrolls
    "scroll_delay_max": 2,  # Maximum delay between page scrolls
    "page_change_delay_min": 3,  # Minimum delay when changing pages
    "page_change_delay_max": 6,  # Maximum delay when changing pages
}

# Search Configuration
DEFAULT_SEARCH_PARAMS = {
    "keywords": "python developer",
    "location": "San Francisco, CA",
    "experience_level": "mid",  # Options: internship, entry, associate, mid, senior, director, executive
    "job_type": "full-time",  # Options: full-time, part-time, contract, temporary, internship, volunteer
    "max_pages": 5,  # Maximum number of pages to scrape
}

# Multiple Search Queries (for batch processing)
SEARCH_QUERIES = [
    {
        "keywords": "python developer",
        "location": "San Francisco, CA",
        "experience_level": "mid",
        "job_type": "full-time",
        "max_pages": 3
    },
    {
        "keywords": "data scientist",
        "location": "New York, NY",
        "experience_level": "senior",
        "job_type": "full-time",
        "max_pages": 3
    },
    {
        "keywords": "machine learning engineer",
        "location": "Seattle, WA",
        "experience_level": "mid",
        "job_type": "full-time",
        "max_pages": 2
    },
    {
        "keywords": "full stack developer",
        "location": "Austin, TX",
        "experience_level": "entry",
        "job_type": "full-time",
        "max_pages": 2
    }
]

# Output Configuration
OUTPUT_CONFIG = {
    "save_csv": True,
    "save_json": True,
    "save_excel": True,
    "output_directory": "./results",
    "filename_timestamp": True,  # Add timestamp to filenames
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",  # Options: DEBUG, INFO, WARNING, ERROR
    "log_to_file": True,
    "log_to_console": True,
    "log_filename": "linkedin_scraper.log",
}

# CSS Selectors (in case LinkedIn changes their structure)
CSS_SELECTORS = {
    "job_cards": ".job-search-card",
    "job_title": ".sr-only",
    "company_name": "h4 a",
    "location": ".job-search-card__location",
    "job_link": "h3 a",
    "posted_date": ".job-search-card__listdate",
    "next_button": 'button[data-test-pagination-page-btn][data-test-pagination-page-btn-next]',
    "job_description": ".jobs-description-content__text",
    "company_insights": ".jobs-company__box dd",
}

# Alternative CSS selectors (fallbacks)
ALTERNATIVE_SELECTORS = {
    "job_cards": [".job-search-card", ".jobs-search-results__list-item"],
    "job_title": [".sr-only", "h3 a", ".job-search-card__title a"],
    "company_name": ["h4 a", ".job-search-card__subtitle a"],
    "location": [".job-search-card__location", "[data-test-job-location]"],
    "job_link": ["h3 a", ".job-search-card__title a"],
    "posted_date": [".job-search-card__listdate", "time"],
}

# User Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
]

# Proxy Configuration (optional)
PROXY_CONFIG = {
    "use_proxy": False,
    "proxy_list": [
        # Add your proxy servers here
        # "http://proxy1:port",
        # "http://proxy2:port",
    ],
    "rotate_proxy": True,
}

# Email Configuration (for notifications)
EMAIL_CONFIG = {
    "send_notifications": False,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": os.getenv("SCRAPER_EMAIL", ""),
    "password": os.getenv("SCRAPER_EMAIL_PASSWORD", ""),
    "recipient": os.getenv("NOTIFICATION_EMAIL", ""),
}

# Job Filtering Configuration
JOB_FILTERS = {
    "exclude_keywords": [
        "unpaid",
        "volunteer",
        "commission only",
    ],
    "required_keywords": [
        # Add keywords that must be present in job title/description
    ],
    "exclude_companies": [
        # Add company names to exclude
    ],
    "min_salary": None,  # Minimum salary (if available)
    "max_salary": None,  # Maximum salary (if available)
}

# Advanced Configuration
ADVANCED_CONFIG = {
    "extract_job_details": False,  # Whether to get detailed job descriptions (slower)
    "extract_company_info": False,  # Whether to get company information (slower)
    "deduplicate_jobs": True,  # Remove duplicate job listings
    "save_screenshots": False,  # Save screenshots for debugging
    "retry_failed_pages": True,  # Retry failed page loads
    "max_retries": 3,  # Maximum number of retries for failed operations
}

def get_config() -> Dict[str, Any]:
    """Return complete configuration dictionary."""
    return {
        "browser": BROWSER_CONFIG,
        "rate_limiting": RATE_LIMITING,
        "default_search": DEFAULT_SEARCH_PARAMS,
        "search_queries": SEARCH_QUERIES,
        "output": OUTPUT_CONFIG,
        "logging": LOGGING_CONFIG,
        "selectors": CSS_SELECTORS,
        "alternative_selectors": ALTERNATIVE_SELECTORS,
        "user_agents": USER_AGENTS,
        "proxy": PROXY_CONFIG,
        "email": EMAIL_CONFIG,
        "filters": JOB_FILTERS,
        "advanced": ADVANCED_CONFIG,
    }

def validate_config() -> bool:
    """Validate configuration settings."""
    config = get_config()
    
    # Validate required fields
    if not config["default_search"]["keywords"]:
        print("❌ Error: Keywords are required in DEFAULT_SEARCH_PARAMS")
        return False
    
    # Validate experience level
    valid_experience = ["internship", "entry", "associate", "mid", "senior", "director", "executive"]
    if config["default_search"]["experience_level"] not in valid_experience + [""]:
        print(f"❌ Error: Invalid experience level. Must be one of: {valid_experience}")
        return False
    
    # Validate job type
    valid_job_types = ["full-time", "part-time", "contract", "temporary", "internship", "volunteer"]
    if config["default_search"]["job_type"] not in valid_job_types + [""]:
        print(f"❌ Error: Invalid job type. Must be one of: {valid_job_types}")
        return False
    
    # Validate output directory
    output_dir = config["output"]["output_directory"]
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"✅ Created output directory: {output_dir}")
        except Exception as e:
            print(f"❌ Error: Cannot create output directory {output_dir}: {e}")
            return False
    
    print("✅ Configuration validation passed")
    return True

if __name__ == "__main__":
    print("🔧 LinkedIn Job Scraper Configuration")
    print("=" * 40)
    
    config = get_config()
    print(f"Default search keywords: {config['default_search']['keywords']}")
    print(f"Default location: {config['default_search']['location']}")
    print(f"Experience level: {config['default_search']['experience_level']}")
    print(f"Job type: {config['default_search']['job_type']}")
    print(f"Max pages: {config['default_search']['max_pages']}")
    print(f"Headless mode: {config['browser']['headless']}")
    print(f"Output directory: {config['output']['output_directory']}")
    
    print("\n🔍 Validating configuration...")
    validate_config()