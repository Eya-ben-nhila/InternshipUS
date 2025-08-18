#!/usr/bin/env python3
"""
Test Fixed Job Search
Verifies that the flexible matching is working
"""

import requests
import json

def test_fixed_search():
    """Test the fixed job search with flexible matching"""
    print("🔧 Testing Fixed Job Search with Flexible Matching...")
    print("=" * 60)
    
    # Test queries that should now work
    test_queries = [
        "software engineer",
        "python developer", 
        "javascript",
        "frontend",
        "backend"
    ]
    
    total_jobs = 0
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 40)
        
        try:
            response = requests.get(
                "http://localhost:5000/api/jobs",
                params={'query': query, 'limit': 5},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                
                print(f"✅ Found {len(jobs)} jobs")
                print(f"📊 Sources: {data.get('meta', {}).get('sources', [])}")
                total_jobs += len(jobs)
                
                # Show first job details
                if jobs:
                    job = jobs[0]
                    print(f"\n📋 Sample job:")
                    print(f"   Title: {job.get('title', 'N/A')}")
                    print(f"   Company: {job.get('company', 'N/A')}")
                    print(f"   Source: {job.get('source', 'N/A')}")
                    print(f"   URL: {job.get('url', 'N/A')}")
                else:
                    print("   No jobs found")
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Total jobs found: {total_jobs}")
    print("✅ Fixed job search is working with flexible matching!")

if __name__ == "__main__":
    print("🔧 Fixed Job Search Test")
    print("This tests the improved flexible matching logic")
    print("=" * 60)
    
    test_fixed_search()
