#!/usr/bin/env python3
"""
Quick Start Script for LinkedIn Job Scraper
Interactive setup and configuration for easy job scraping.
"""

import sys
import os
from linkedin_job_scraper import LinkedInJobScraper

def welcome_message():
    """Display welcome message and features."""
    print("🚀 Welcome to LinkedIn Job Scraper!")
    print("=" * 50)
    print("✨ Features:")
    print("  • Anti-detection measures")
    print("  • Multiple output formats (CSV, JSON, Excel)")
    print("  • Batch processing capabilities")
    print("  • Rate limiting to avoid blocks")
    print("  • Comprehensive logging")
    print("\n⚠️  Important: Use responsibly and respect LinkedIn's ToS")
    print("-" * 50)

def get_user_input():
    """Get search parameters from user."""
    print("\n📝 Let's configure your job search:")
    
    # Job keywords
    keywords = input("\n🔍 Enter job keywords (e.g., 'python developer'): ").strip()
    if not keywords:
        keywords = "software engineer"
        print(f"   Using default: {keywords}")
    
    # Location
    location = input("📍 Enter location (e.g., 'San Francisco, CA' or 'Remote'): ").strip()
    if not location:
        location = "United States"
        print(f"   Using default: {location}")
    
    # Experience level
    print("\n🎯 Experience levels:")
    print("  1. Internship")
    print("  2. Entry level")
    print("  3. Associate")
    print("  4. Mid-level")
    print("  5. Senior level")
    print("  6. Director")
    print("  7. Executive")
    
    exp_choice = input("\nSelect experience level (1-7, or press Enter for mid-level): ").strip()
    exp_map = {
        '1': 'internship',
        '2': 'entry',
        '3': 'associate',
        '4': 'mid',
        '5': 'senior',
        '6': 'director',
        '7': 'executive'
    }
    experience_level = exp_map.get(exp_choice, 'mid')
    print(f"   Selected: {experience_level}")
    
    # Job type
    print("\n💼 Job types:")
    print("  1. Full-time")
    print("  2. Part-time")
    print("  3. Contract")
    print("  4. Temporary")
    print("  5. Internship")
    print("  6. Volunteer")
    
    job_choice = input("\nSelect job type (1-6, or press Enter for full-time): ").strip()
    job_map = {
        '1': 'full-time',
        '2': 'part-time',
        '3': 'contract',
        '4': 'temporary',
        '5': 'internship',
        '6': 'volunteer'
    }
    job_type = job_map.get(job_choice, 'full-time')
    print(f"   Selected: {job_type}")
    
    # Number of pages
    while True:
        try:
            max_pages = input("\n📄 Number of pages to scrape (1-10, recommended: 3): ").strip()
            if not max_pages:
                max_pages = 3
            else:
                max_pages = int(max_pages)
            
            if 1 <= max_pages <= 10:
                break
            else:
                print("   Please enter a number between 1 and 10")
        except ValueError:
            print("   Please enter a valid number")
    
    # Browser mode
    headless_choice = input("\n🖥️  Run in headless mode? (faster, no browser window) [y/N]: ").strip().lower()
    headless = headless_choice in ['y', 'yes']
    
    return {
        'keywords': keywords,
        'location': location,
        'experience_level': experience_level,
        'job_type': job_type,
        'max_pages': max_pages,
        'headless': headless
    }

def confirm_search(params):
    """Display search parameters and confirm."""
    print("\n📋 Search Configuration:")
    print("-" * 30)
    print(f"Keywords: {params['keywords']}")
    print(f"Location: {params['location']}")
    print(f"Experience: {params['experience_level']}")
    print(f"Job Type: {params['job_type']}")
    print(f"Pages: {params['max_pages']}")
    print(f"Headless: {'Yes' if params['headless'] else 'No'}")
    
    confirm = input("\n✅ Proceed with this search? [Y/n]: ").strip().lower()
    return confirm not in ['n', 'no']

def run_search(params):
    """Execute the job search."""
    print("\n🚀 Starting LinkedIn job search...")
    print("🔄 Initializing browser...")
    
    scraper = LinkedInJobScraper(
        headless=params['headless'],
        use_undetected=True
    )
    
    try:
        # Perform search
        jobs = scraper.search_jobs(
            keywords=params['keywords'],
            location=params['location'],
            experience_level=params['experience_level'],
            job_type=params['job_type'],
            max_pages=params['max_pages']
        )
        
        if jobs:
            print(f"\n✅ Successfully found {len(jobs)} jobs!")
            
            # Save results
            print("\n💾 Saving results...")
            csv_file = scraper.save_to_csv(jobs)
            json_file = scraper.save_to_json(jobs)
            excel_file = scraper.save_to_excel(jobs)
            
            print(f"\n📁 Results saved to:")
            print(f"  • CSV: {csv_file}")
            print(f"  • JSON: {json_file}")
            print(f"  • Excel: {excel_file}")
            
            # Display sample results
            print(f"\n📋 Sample jobs (showing first 5 of {len(jobs)}):")
            print("-" * 80)
            
            for i, job in enumerate(jobs[:5], 1):
                print(f"\n{i}. {job.get('title', 'N/A')}")
                print(f"   🏢 Company: {job.get('company', 'N/A')}")
                print(f"   📍 Location: {job.get('location', 'N/A')}")
                print(f"   📅 Posted: {job.get('posted_date', 'N/A')}")
                if job.get('link') != 'N/A':
                    print(f"   🔗 Link: {job.get('link')}")
            
            if len(jobs) > 5:
                print(f"\n... and {len(jobs) - 5} more jobs in the saved files!")
        
        else:
            print("\n❌ No jobs found. Try adjusting your search parameters:")
            print("  • Use different keywords")
            print("  • Try a broader location")
            print("  • Adjust experience level or job type")
    
    except KeyboardInterrupt:
        print("\n⏹️  Search interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("💡 Try running with headless=False to see what's happening")
    
    finally:
        scraper.close()
        print("\n🔒 Browser closed")

def offer_batch_mode():
    """Offer to run in batch mode."""
    print("\n🔄 Would you like to run additional searches?")
    print("You can:")
    print("  • Run this search again with different parameters")
    print("  • Use batch_scraper.py for multiple automated searches")
    print("  • Edit config.py to customize default settings")
    
    again = input("\nRun another search? [y/N]: ").strip().lower()
    return again in ['y', 'yes']

def display_tips():
    """Display helpful tips."""
    print("\n💡 Tips for better results:")
    print("  • Use specific job titles (e.g., 'Python Developer' vs 'Developer')")
    print("  • Try both city names and 'Remote' for location")
    print("  • Start with fewer pages (2-3) to test your search")
    print("  • Check the logs if you encounter issues")
    print("  • Respect LinkedIn's servers - don't scrape too aggressively")
    
    print("\n🔧 Advanced usage:")
    print("  • Edit config.py for custom settings")
    print("  • Use batch_scraper.py for multiple searches")
    print("  • Run 'python linkedin_job_scraper.py' for programmatic use")

def main():
    """Main function for quick start."""
    try:
        welcome_message()
        
        while True:
            # Get search parameters
            params = get_user_input()
            
            # Confirm search
            if not confirm_search(params):
                print("🔄 Let's reconfigure...")
                continue
            
            # Run search
            run_search(params)
            
            # Check if user wants to run again
            if not offer_batch_mode():
                break
        
        display_tips()
        print("\n🎉 Thank you for using LinkedIn Job Scraper!")
        print("📚 Check README.md for more advanced features")
    
    except KeyboardInterrupt:
        print("\n⏹️  Quick start interrupted by user")
    except Exception as e:
        print(f"\n❌ Quick start failed: {str(e)}")

if __name__ == "__main__":
    main()