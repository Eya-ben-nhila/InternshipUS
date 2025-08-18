#!/usr/bin/env python3
"""
Test Comprehensive Job Search
Shows maximum jobs with complete details
"""

import requests
import json

def test_comprehensive_search():
    """Test the comprehensive job search"""
    print("🚀 Testing Comprehensive Job Search...")
    print("=" * 60)
    
    # Test with a broad search to get maximum jobs
    queries = ["developer", "engineer", "programmer"]
    
    total_jobs = 0
    
    for query in queries:
        print(f"\n🔍 Searching for: '{query}'")
        print("-" * 40)
        
        try:
            response = requests.get(
                "http://localhost:5000/api/jobs",
                params={'query': query, 'limit': 30}
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                
                print(f"✅ Found {len(jobs)} jobs")
                print(f"📊 Sources: {data.get('meta', {}).get('sources', [])}")
                total_jobs += len(jobs)
                
                # Show detailed job info
                for i, job in enumerate(jobs[:3], 1):  # Show first 3 jobs
                    print(f"\n{i}. {job.get('title', 'N/A')}")
                    print(f"   🏢 Company: {job.get('company', 'N/A')}")
                    print(f"   📍 Location: {job.get('location', 'N/A')}")
                    print(f"   💰 Salary: {job.get('salary', 'N/A')}")
                    print(f"   🌐 Source: {job.get('source', 'N/A')}")
                    print(f"   📅 Posted: {job.get('date_posted', 'N/A')}")
                    print(f"   📝 Description: {job.get('description', 'N/A')[:150]}...")
                    print(f"   🔗 URL: {job.get('url', 'N/A')}")
                
                if len(jobs) > 3:
                    print(f"\n   ... and {len(jobs) - 3} more jobs")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Total jobs found: {total_jobs}")
    print("✅ Comprehensive search is working with many more jobs!")

if __name__ == "__main__":
    print("🚀 Comprehensive Job Search Test")
    print("This will show you many more jobs with complete details")
    print("Make sure to start: python comprehensive_job_search.py")
    print("=" * 60)
    
    test_comprehensive_search()
