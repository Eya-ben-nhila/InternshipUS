#!/usr/bin/env python3
"""
Test script for Reliable Job Search
Verifies that the job search returns real job postings
"""

import requests
import json
import time

def test_job_search():
    """Test the reliable job search API"""
    print("🧪 Testing Reliable Job Search API...")
    print("=" * 50)
    
    # Test parameters
    test_queries = [
        "software engineer",
        "python developer", 
        "frontend developer",
        "data scientist"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing search for: '{query}'")
        print("-" * 30)
        
        try:
            # Make API request
            url = "http://localhost:5000/api/jobs"
            params = {
                'query': query,
                'limit': 5
            }
            
            print(f"📡 Making request to: {url}")
            print(f"📋 Parameters: {params}")
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                
                print(f"✅ Success! Found {len(jobs)} jobs")
                print(f"📊 Sources: {data.get('meta', {}).get('sources', [])}")
                
                # Display job details
                for i, job in enumerate(jobs, 1):
                    print(f"\n{i}. {job.get('title', 'N/A')}")
                    print(f"   🏢 Company: {job.get('company', 'N/A')}")
                    print(f"   📍 Location: {job.get('location', 'N/A')}")
                    print(f"   🌐 Source: {job.get('source', 'N/A')}")
                    print(f"   🔗 URL: {job.get('url', 'N/A')}")
                    print(f"   📅 Posted: {job.get('date_posted', 'N/A')}")
                    
                    # Verify this is a real job posting
                    if job.get('url') and 'http' in job.get('url', ''):
                        print(f"   ✅ Real job posting (has valid URL)")
                    else:
                        print(f"   ⚠️  Potential mock data (no valid URL)")
                
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
        
        print("\n" + "="*50)
        time.sleep(2)  # Rate limiting between tests

def test_health_check():
    """Test the health check endpoint"""
    print("\n🏥 Testing health check...")
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    print("🚀 Reliable Job Search Test Suite")
    print("This will test if the job search returns real job postings")
    print("Make sure to start the API server first: python reliable_job_search.py")
    print("\n" + "="*60)
    
    # Test health check first
    test_health_check()
    
    # Test job search
    test_job_search()
    
    print("\n🎉 Test completed!")
    print("If you see real job postings with valid URLs, the system is working correctly!")
