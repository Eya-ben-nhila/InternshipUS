#!/usr/bin/env python3
"""
LinkedIn Job Scraper
A comprehensive tool for scraping job listings from LinkedIn with anti-detection measures.
"""

import os
import time
import random
import json
import csv
import logging
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import undetected_chromedriver as uc
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests

class LinkedInJobScraper:
    """Enhanced LinkedIn job scraper with anti-detection capabilities."""
    
    def __init__(self, headless: bool = False, use_undetected: bool = True):
        """
        Initialize the scraper with configuration options.
        
        Args:
            headless: Run browser in headless mode
            use_undetected: Use undetected-chromedriver for better anti-detection
        """
        self.driver = None
        self.headless = headless
        self.use_undetected = use_undetected
        self.jobs_data = []
        self.ua = UserAgent()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('linkedin_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Rate limiting settings
        self.min_delay = 2
        self.max_delay = 5
        
    def setup_driver(self) -> None:
        """Setup Chrome driver with anti-detection measures."""
        try:
            if self.use_undetected:
                options = uc.ChromeOptions()
            else:
                options = Options()
            
            # Common options for stealth
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--disable-javascript')
            
            # Randomize window size
            window_sizes = ['1920,1080', '1366,768', '1440,900', '1280,720']
            options.add_argument(f'--window-size={random.choice(window_sizes)}')
            
            # Random user agent
            options.add_argument(f'--user-agent={self.ua.random}')
            
            if self.headless:
                options.add_argument('--headless')
            
            if self.use_undetected:
                self.driver = uc.Chrome(options=options)
            else:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            # Execute script to hide webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Driver setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup driver: {str(e)}")
            raise
    
    def random_delay(self, min_delay: float = None, max_delay: float = None) -> None:
        """Add random delay to mimic human behavior."""
        min_d = min_delay or self.min_delay
        max_d = max_delay or self.max_delay
        delay = random.uniform(min_d, max_d)
        time.sleep(delay)
    
    def scroll_page(self, scroll_count: int = 3) -> None:
        """Scroll page to load more content."""
        for i in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(1, 2)
            
    def search_jobs(self, keywords: str, location: str = "", experience_level: str = "", 
                   job_type: str = "", max_pages: int = 5) -> List[Dict]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            keywords: Job search keywords
            location: Job location
            experience_level: Experience level filter
            job_type: Job type filter (full-time, part-time, etc.)
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of job dictionaries
        """
        if not self.driver:
            self.setup_driver()
        
        jobs = []
        
        try:
            # Build search URL
            base_url = "https://www.linkedin.com/jobs/search"
            params = {
                'keywords': keywords,
                'location': location,
                'f_E': self._get_experience_code(experience_level),
                'f_JT': self._get_job_type_code(job_type),
                'sortBy': 'DD'  # Sort by date posted
            }
            
            # Remove empty parameters
            params = {k: v for k, v in params.items() if v}
            
            # Construct URL with parameters
            url = base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
            
            self.logger.info(f"Starting job search: {keywords} in {location}")
            self.driver.get(url)
            self.random_delay(3, 5)
            
            for page in range(max_pages):
                self.logger.info(f"Scraping page {page + 1}")
                
                # Scroll to load more jobs
                self.scroll_page(3)
                
                # Extract job cards
                page_jobs = self._extract_job_cards()
                jobs.extend(page_jobs)
                
                self.logger.info(f"Found {len(page_jobs)} jobs on page {page + 1}")
                
                # Navigate to next page
                if page < max_pages - 1:
                    if not self._go_to_next_page():
                        self.logger.info("No more pages available")
                        break
                
                self.random_delay(3, 6)
            
            self.logger.info(f"Total jobs scraped: {len(jobs)}")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error during job search: {str(e)}")
            return jobs
    
    def _extract_job_cards(self) -> List[Dict]:
        """Extract job information from job cards on current page."""
        jobs = []
        
        try:
            # Wait for job cards to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.job-search-card'))
            )
            
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, '.job-search-card')
            
            for card in job_cards:
                try:
                    job_data = self._extract_single_job(card)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    self.logger.warning(f"Failed to extract job: {str(e)}")
                    continue
                    
        except TimeoutException:
            self.logger.warning("Timeout waiting for job cards to load")
        except Exception as e:
            self.logger.error(f"Error extracting job cards: {str(e)}")
        
        return jobs
    
    def _extract_single_job(self, card) -> Optional[Dict]:
        """Extract data from a single job card."""
        try:
            job_data = {}
            
            # Job title
            title_elem = card.find_element(By.CSS_SELECTOR, '.sr-only')
            job_data['title'] = title_elem.get_attribute('innerText').strip() if title_elem else 'N/A'
            
            # Company name
            try:
                company_elem = card.find_element(By.CSS_SELECTOR, 'h4 a')
                job_data['company'] = company_elem.text.strip()
            except NoSuchElementException:
                job_data['company'] = 'N/A'
            
            # Location
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, '.job-search-card__location')
                job_data['location'] = location_elem.text.strip()
            except NoSuchElementException:
                job_data['location'] = 'N/A'
            
            # Job link
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, 'h3 a')
                job_data['link'] = link_elem.get_attribute('href')
            except NoSuchElementException:
                job_data['link'] = 'N/A'
            
            # Posted date
            try:
                date_elem = card.find_element(By.CSS_SELECTOR, '.job-search-card__listdate')
                job_data['posted_date'] = date_elem.text.strip()
            except NoSuchElementException:
                job_data['posted_date'] = 'N/A'
            
            # Additional metadata
            job_data['scraped_at'] = datetime.now().isoformat()
            job_data['job_id'] = self._extract_job_id(job_data.get('link', ''))
            
            return job_data
            
        except Exception as e:
            self.logger.warning(f"Error extracting single job: {str(e)}")
            return None
    
    def _extract_job_id(self, url: str) -> str:
        """Extract job ID from LinkedIn job URL."""
        try:
            if 'currentJobId=' in url:
                return url.split('currentJobId=')[1].split('&')[0]
            elif '/view/' in url:
                return url.split('/view/')[1].split('/')[0]
            else:
                return 'N/A'
        except:
            return 'N/A'
    
    def _go_to_next_page(self) -> bool:
        """Navigate to next page of results."""
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, 
                'button[data-test-pagination-page-btn][data-test-pagination-page-btn-next]'
            )
            
            if next_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", next_button)
                self.random_delay(3, 5)
                return True
            else:
                return False
                
        except NoSuchElementException:
            return False
    
    def _get_experience_code(self, level: str) -> str:
        """Map experience level to LinkedIn filter code."""
        experience_map = {
            'internship': '1',
            'entry': '2',
            'associate': '3',
            'mid': '4',
            'senior': '5',
            'director': '6',
            'executive': '7'
        }
        return experience_map.get(level.lower(), '')
    
    def _get_job_type_code(self, job_type: str) -> str:
        """Map job type to LinkedIn filter code."""
        job_type_map = {
            'full-time': 'F',
            'part-time': 'P',
            'contract': 'C',
            'temporary': 'T',
            'internship': 'I',
            'volunteer': 'V'
        }
        return job_type_map.get(job_type.lower(), '')
    
    def get_job_details(self, job_url: str) -> Dict:
        """Get detailed information for a specific job."""
        try:
            self.driver.get(job_url)
            self.random_delay(2, 4)
            
            # Wait for job details to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.jobs-description-content'))
            )
            
            details = {}
            
            # Job description
            try:
                desc_elem = self.driver.find_element(By.CSS_SELECTOR, '.jobs-description-content__text')
                details['description'] = desc_elem.get_attribute('innerText')
            except NoSuchElementException:
                details['description'] = 'N/A'
            
            # Company size, industry, etc.
            try:
                company_insights = self.driver.find_elements(By.CSS_SELECTOR, '.jobs-company__box dd')
                if len(company_insights) >= 2:
                    details['company_size'] = company_insights[0].text
                    details['industry'] = company_insights[1].text
            except:
                details['company_size'] = 'N/A'
                details['industry'] = 'N/A'
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error getting job details: {str(e)}")
            return {}
    
    def save_to_csv(self, jobs: List[Dict], filename: str = None) -> str:
        """Save jobs data to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.csv"
        
        try:
            df = pd.DataFrame(jobs)
            df.to_csv(filename, index=False, encoding='utf-8')
            self.logger.info(f"Jobs saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {str(e)}")
            return ""
    
    def save_to_json(self, jobs: List[Dict], filename: str = None) -> str:
        """Save jobs data to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Jobs saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {str(e)}")
            return ""
    
    def save_to_excel(self, jobs: List[Dict], filename: str = None) -> str:
        """Save jobs data to Excel file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_jobs_{timestamp}.xlsx"
        
        try:
            df = pd.DataFrame(jobs)
            df.to_excel(filename, index=False, engine='openpyxl')
            self.logger.info(f"Jobs saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error saving to Excel: {str(e)}")
            return ""
    
    def close(self) -> None:
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser driver closed")


def main():
    """Example usage of the LinkedIn Job Scraper."""
    
    # Initialize scraper
    scraper = LinkedInJobScraper(headless=False, use_undetected=True)
    
    try:
        # Search configuration
        search_params = {
            'keywords': 'python developer',
            'location': 'San Francisco, CA',
            'experience_level': 'mid',
            'job_type': 'full-time',
            'max_pages': 3
        }
        
        print("🚀 Starting LinkedIn job search...")
        print(f"Keywords: {search_params['keywords']}")
        print(f"Location: {search_params['location']}")
        print(f"Experience: {search_params['experience_level']}")
        print(f"Type: {search_params['job_type']}")
        print(f"Max pages: {search_params['max_pages']}")
        print("-" * 50)
        
        # Perform search
        jobs = scraper.search_jobs(**search_params)
        
        if jobs:
            print(f"✅ Found {len(jobs)} jobs!")
            
            # Save to different formats
            csv_file = scraper.save_to_csv(jobs)
            json_file = scraper.save_to_json(jobs)
            excel_file = scraper.save_to_excel(jobs)
            
            print(f"📁 Results saved to:")
            print(f"  • CSV: {csv_file}")
            print(f"  • JSON: {json_file}")
            print(f"  • Excel: {excel_file}")
            
            # Display sample jobs
            print("\n📋 Sample jobs:")
            for i, job in enumerate(jobs[:5], 1):
                print(f"{i}. {job['title']} at {job['company']}")
                print(f"   📍 {job['location']}")
                print(f"   🔗 {job['link']}")
                print(f"   📅 {job['posted_date']}")
                print()
        else:
            print("❌ No jobs found. Try adjusting your search parameters.")
    
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    
    finally:
        scraper.close()


if __name__ == "__main__":
    main()