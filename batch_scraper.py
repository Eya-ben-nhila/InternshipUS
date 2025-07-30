#!/usr/bin/env python3
"""
Batch LinkedIn Job Scraper
Process multiple search queries and aggregate results.
"""

import json
import time
import os
from datetime import datetime
from typing import List, Dict
import pandas as pd

from linkedin_job_scraper import LinkedInJobScraper
from config import get_config, validate_config, SEARCH_QUERIES

class BatchJobScraper:
    """Batch processor for multiple LinkedIn job searches."""
    
    def __init__(self, config_override: Dict = None):
        """Initialize batch scraper with configuration."""
        self.config = get_config()
        if config_override:
            self.config.update(config_override)
        
        self.all_jobs = []
        self.search_results = {}
        self.start_time = datetime.now()
        
        # Validate configuration
        if not validate_config():
            raise ValueError("Invalid configuration")
    
    def run_batch_search(self, search_queries: List[Dict] = None) -> Dict:
        """
        Run multiple search queries in batch.
        
        Args:
            search_queries: List of search parameter dictionaries
            
        Returns:
            Dictionary containing all results and statistics
        """
        if search_queries is None:
            search_queries = SEARCH_QUERIES
        
        print("🚀 Starting batch LinkedIn job search...")
        print(f"📊 Processing {len(search_queries)} search queries")
        print("=" * 60)
        
        scraper = LinkedInJobScraper(
            headless=self.config['browser']['headless'],
            use_undetected=self.config['browser']['use_undetected']
        )
        
        try:
            for i, query in enumerate(search_queries, 1):
                print(f"\n🔍 Search {i}/{len(search_queries)}: {query['keywords']} in {query['location']}")
                print("-" * 40)
                
                # Perform search
                jobs = scraper.search_jobs(**query)
                
                # Store results
                query_key = f"search_{i}_{query['keywords'].replace(' ', '_')}"
                self.search_results[query_key] = {
                    'query': query,
                    'jobs': jobs,
                    'count': len(jobs),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add to master list
                for job in jobs:
                    job['search_query'] = query['keywords']
                    job['search_location'] = query['location']
                    job['batch_id'] = query_key
                    self.all_jobs.append(job)
                
                print(f"✅ Found {len(jobs)} jobs for this query")
                
                # Add delay between searches to avoid rate limiting
                if i < len(search_queries):
                    delay_time = self.config['rate_limiting']['page_change_delay_max']
                    print(f"⏳ Waiting {delay_time} seconds before next search...")
                    time.sleep(delay_time)
        
        finally:
            scraper.close()
        
        # Process and save results
        return self._process_results()
    
    def _process_results(self) -> Dict:
        """Process and aggregate all search results."""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Remove duplicates
        if self.config['advanced']['deduplicate_jobs']:
            original_count = len(self.all_jobs)
            self.all_jobs = self._remove_duplicates(self.all_jobs)
            dedup_count = len(self.all_jobs)
            print(f"🧹 Removed {original_count - dedup_count} duplicate jobs")
        
        # Apply filters
        if self.config['filters']['exclude_keywords'] or self.config['filters']['required_keywords']:
            original_count = len(self.all_jobs)
            self.all_jobs = self._apply_filters(self.all_jobs)
            filtered_count = len(self.all_jobs)
            print(f"🔍 Filtered out {original_count - filtered_count} jobs")
        
        # Create summary statistics
        stats = self._generate_statistics()
        
        # Save results
        output_files = self._save_results()
        
        # Print summary
        self._print_summary(stats, duration, output_files)
        
        return {
            'jobs': self.all_jobs,
            'search_results': self.search_results,
            'statistics': stats,
            'duration': duration.total_seconds(),
            'output_files': output_files
        }
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on job URL or title+company."""
        seen_urls = set()
        seen_jobs = set()
        unique_jobs = []
        
        for job in jobs:
            # Primary deduplication by URL
            if job.get('link') and job['link'] != 'N/A':
                if job['link'] not in seen_urls:
                    seen_urls.add(job['link'])
                    unique_jobs.append(job)
                continue
            
            # Secondary deduplication by title + company
            job_signature = f"{job.get('title', '').lower()}_{job.get('company', '').lower()}"
            if job_signature not in seen_jobs:
                seen_jobs.add(job_signature)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _apply_filters(self, jobs: List[Dict]) -> List[Dict]:
        """Apply filtering based on configuration."""
        filtered_jobs = []
        
        for job in jobs:
            title = job.get('title', '').lower()
            company = job.get('company', '').lower()
            
            # Check exclude keywords
            if any(keyword.lower() in title for keyword in self.config['filters']['exclude_keywords']):
                continue
            
            # Check required keywords
            if self.config['filters']['required_keywords']:
                if not any(keyword.lower() in title for keyword in self.config['filters']['required_keywords']):
                    continue
            
            # Check exclude companies
            if any(comp.lower() in company for comp in self.config['filters']['exclude_companies']):
                continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _generate_statistics(self) -> Dict:
        """Generate statistics about the scraped jobs."""
        if not self.all_jobs:
            return {}
        
        df = pd.DataFrame(self.all_jobs)
        
        stats = {
            'total_jobs': len(self.all_jobs),
            'unique_companies': df['company'].nunique(),
            'unique_locations': df['location'].nunique(),
            'jobs_per_search': {},
            'top_companies': df['company'].value_counts().head(10).to_dict(),
            'top_locations': df['location'].value_counts().head(10).to_dict(),
            'jobs_by_search_query': df['search_query'].value_counts().to_dict()
        }
        
        # Jobs per search query
        for key, result in self.search_results.items():
            stats['jobs_per_search'][key] = result['count']
        
        return stats
    
    def _save_results(self) -> Dict[str, str]:
        """Save results to various formats."""
        output_dir = self.config['output']['output_directory']
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_files = {}
        
        # Save aggregated results
        if self.config['output']['save_json']:
            json_file = os.path.join(output_dir, f"batch_jobs_{timestamp}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'jobs': self.all_jobs,
                    'search_results': self.search_results,
                    'statistics': self._generate_statistics(),
                    'metadata': {
                        'total_jobs': len(self.all_jobs),
                        'searches_performed': len(self.search_results),
                        'scraped_at': datetime.now().isoformat()
                    }
                }, f, indent=2, ensure_ascii=False)
            output_files['json'] = json_file
        
        if self.config['output']['save_csv']:
            csv_file = os.path.join(output_dir, f"batch_jobs_{timestamp}.csv")
            df = pd.DataFrame(self.all_jobs)
            df.to_csv(csv_file, index=False, encoding='utf-8')
            output_files['csv'] = csv_file
        
        if self.config['output']['save_excel']:
            excel_file = os.path.join(output_dir, f"batch_jobs_{timestamp}.xlsx")
            
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                # All jobs sheet
                df_all = pd.DataFrame(self.all_jobs)
                df_all.to_excel(writer, sheet_name='All Jobs', index=False)
                
                # Individual search results
                for key, result in self.search_results.items():
                    if result['jobs']:
                        df_search = pd.DataFrame(result['jobs'])
                        sheet_name = key.replace('search_', '').replace('_', ' ')[:31]  # Excel sheet name limit
                        df_search.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Statistics sheet
                stats_data = []
                stats = self._generate_statistics()
                for category, data in stats.items():
                    if isinstance(data, dict):
                        for item, count in data.items():
                            stats_data.append({'Category': category, 'Item': item, 'Count': count})
                    else:
                        stats_data.append({'Category': category, 'Item': 'Total', 'Count': data})
                
                if stats_data:
                    df_stats = pd.DataFrame(stats_data)
                    df_stats.to_excel(writer, sheet_name='Statistics', index=False)
            
            output_files['excel'] = excel_file
        
        return output_files
    
    def _print_summary(self, stats: Dict, duration, output_files: Dict) -> None:
        """Print summary of the batch scraping results."""
        print("\n" + "=" * 60)
        print("📊 BATCH SCRAPING SUMMARY")
        print("=" * 60)
        
        print(f"⏱️  Duration: {duration}")
        print(f"🔍 Total searches: {len(self.search_results)}")
        print(f"📋 Total jobs found: {stats.get('total_jobs', 0)}")
        print(f"🏢 Unique companies: {stats.get('unique_companies', 0)}")
        print(f"📍 Unique locations: {stats.get('unique_locations', 0)}")
        
        print("\n📈 Jobs per search query:")
        for query, count in stats.get('jobs_by_search_query', {}).items():
            print(f"  • {query}: {count} jobs")
        
        print("\n🏆 Top companies:")
        for company, count in list(stats.get('top_companies', {}).items())[:5]:
            print(f"  • {company}: {count} jobs")
        
        print("\n📍 Top locations:")
        for location, count in list(stats.get('top_locations', {}).items())[:5]:
            print(f"  • {location}: {count} jobs")
        
        print(f"\n📁 Results saved to:")
        for format_type, filepath in output_files.items():
            print(f"  • {format_type.upper()}: {filepath}")
        
        print("\n✅ Batch scraping completed successfully!")

def main():
    """Main function for batch processing."""
    try:
        # Initialize batch scraper
        batch_scraper = BatchJobScraper()
        
        # Run batch search with default queries
        results = batch_scraper.run_batch_search()
        
        # Optional: Run custom searches
        custom_queries = [
            {
                "keywords": "react developer",
                "location": "Remote",
                "experience_level": "mid",
                "job_type": "full-time",
                "max_pages": 2
            },
            {
                "keywords": "devops engineer",
                "location": "Boston, MA",
                "experience_level": "senior",
                "job_type": "full-time",
                "max_pages": 2
            }
        ]
        
        # Uncomment to run additional custom searches
        # print("\n🔄 Running additional custom searches...")
        # additional_results = batch_scraper.run_batch_search(custom_queries)
        
    except KeyboardInterrupt:
        print("\n⏹️  Batch scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during batch scraping: {str(e)}")

if __name__ == "__main__":
    main()