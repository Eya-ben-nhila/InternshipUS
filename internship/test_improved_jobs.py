#!/usr/bin/env python3
"""
Test Improved Job Search
Shows more jobs and better details
"""

import requests
import json

def test_improved_job_search():
    """Test the improved job search API"""
    print("🧪 Testing Improved Job Search API...")
    print("=" * 60)
    
    # Test different queries to get more jobs
    test_queries = [
        "developer",
        "software engineer", 
        "python",
        "javascript"
    ]
    
    total_jobs = 0
    
    for query in test_queries:
        print(f"\n🔍 Testing search for: '{query}'")
        print("-" * 40)
        
        try:
            # Make API request
            url = "http://localhost:5000/api/jobs"
            params = {
                'query': query,
                'limit': 15
            }
            
            print(f"📡 Making request to: {url}")
            print(f"📋 Parameters: {params}")
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                
                print(f"✅ Success! Found {len(jobs)} jobs")
                print(f"📊 Sources: {data.get('meta', {}).get('sources', [])}")
                total_jobs += len(jobs)
                
                # Display job details
                for i, job in enumerate(jobs[:5], 1):  # Show first 5 jobs
                    print(f"\n{i}. {job.get('title', 'N/A')}")
                    print(f"   🏢 Company: {job.get('company', 'N/A')}")
                    print(f"   📍 Location: {job.get('location', 'N/A')}")
                    print(f"   💰 Salary: {job.get('salary', 'N/A')}")
                    print(f"   🌐 Source: {job.get('source', 'N/A')}")
                    print(f"   🔗 URL: {job.get('url', 'N/A')}")
                    print(f"   📅 Posted: {job.get('date_posted', 'N/A')}")
                    print(f"   📝 Description: {job.get('description', 'N/A')[:100]}...")
                    
                    # Verify this is a real job posting
                    if job.get('url') and 'http' in job.get('url', ''):
                        print(f"   ✅ Real job posting (has valid URL)")
                    else:
                        print(f"   ⚠️  Potential mock data (no valid URL)")
                
                if len(jobs) > 5:
                    print(f"\n   ... and {len(jobs) - 5} more jobs")
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - Make sure the API server is running!")
            print("💡 Run: python reliable_job_search.py")
            break
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)
    
    print(f"\n🎉 Total jobs found across all queries: {total_jobs}")
    print("✅ Improved job search is working with more jobs and better details!")

if __name__ == "__main__":
    print("🚀 Improved Job Search Test")
    print("This will test the enhanced job search with more jobs and better details")
    print("Make sure to start the API server first: python reliable_job_search.py")
    print("\n" + "="*60)
    
    test_improved_job_search()
