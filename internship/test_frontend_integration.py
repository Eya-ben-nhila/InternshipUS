#!/usr/bin/env python3
"""
Test Frontend Integration
Simulates the frontend request to verify integration
"""

import requests
import json

def test_frontend_integration():
    """Test the frontend integration by simulating the exact request"""
    print("🌐 Testing Frontend Integration...")
    print("=" * 60)
    
    # Simulate the exact frontend request
    print("🔍 Simulating frontend search for: 'software engineer'")
    print("-" * 50)
    
    try:
        # This is the exact request the frontend makes
        url = "http://localhost:5000/api/jobs"
        params = {
            'query': 'software engineer',
            'limit': '100'  # Frontend requests 100 jobs
        }
        
        print(f"📡 Making request to: {url}")
        print(f"📋 Parameters: {params}")
        
        response = requests.get(url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('data', [])
            
            print(f"✅ Success! Found {len(jobs)} jobs")
            print(f"📊 Sources: {data.get('meta', {}).get('sources', [])}")
            print(f"🔍 Query: {data.get('meta', {}).get('query', 'N/A')}")
            
            # Show sample jobs
            if jobs:
                print(f"\n📋 Sample jobs:")
                for i, job in enumerate(jobs[:3], 1):
                    print(f"\n{i}. {job.get('title', 'N/A')}")
                    print(f"   🏢 Company: {job.get('company', 'N/A')}")
                    print(f"   📍 Location: {job.get('location', 'N/A')}")
                    print(f"   💰 Salary: {job.get('salary', 'N/A')}")
                    print(f"   🌐 Source: {job.get('source', 'N/A')}")
                    print(f"   🔗 URL: {job.get('url', 'N/A')}")
                
                if len(jobs) > 3:
                    print(f"\n   ... and {len(jobs) - 3} more jobs")
                
                print(f"\n🎉 Frontend integration is working!")
                print(f"✅ The frontend should now show {len(jobs)} jobs for 'software engineer'")
            else:
                print("⚠️  No jobs found - this might indicate an issue")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Make sure the API server is running!")
        print("💡 Run: python reliable_job_search.py")
    except requests.exceptions.Timeout:
        print("❌ Request timeout - The service might be slow")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🌐 Frontend Integration Test")
    print("This simulates the exact frontend request")
    print("=" * 60)
    
    test_frontend_integration()
