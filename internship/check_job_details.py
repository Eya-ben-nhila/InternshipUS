#!/usr/bin/env python3
"""
Check Job Details
Examines the job details to see what's wrong with parsing
"""

import requests
import json

def check_job_details():
    """Check the job details to see parsing issues"""
    print("🔍 Checking Job Details...")
    print("=" * 60)
    
    try:
        response = requests.get(
            "http://localhost:5000/api/jobs",
            params={'query': 'software engineer', 'limit': 3},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('data', [])
            
            print(f"✅ Found {len(jobs)} jobs")
            print(f"📊 Sources: {data.get('meta', {}).get('sources', [])}")
            
            # Examine each job in detail
            for i, job in enumerate(jobs, 1):
                print(f"\n{'='*50}")
                print(f"JOB {i}:")
                print(f"{'='*50}")
                
                print(f"Title: {job.get('title', 'N/A')}")
                print(f"Company: {job.get('company', 'N/A')}")
                print(f"Location: {job.get('location', 'N/A')}")
                print(f"Salary: {job.get('salary', 'N/A')}")
                print(f"Source: {job.get('source', 'N/A')}")
                print(f"URL: {job.get('url', 'N/A')}")
                print(f"Date Posted: {job.get('date_posted', 'N/A')}")
                print(f"Job Type: {job.get('job_type', 'N/A')}")
                print(f"Remote: {job.get('remote', 'N/A')}")
                print(f"Relevance Score: {job.get('relevance_score', 'N/A')}")
                
                # Check description length and content
                description = job.get('description', '')
                print(f"\nDescription Length: {len(description)} characters")
                print(f"Description Preview: {description[:200]}...")
                
                # Check if description is empty or just placeholder
                if not description or description.strip() == '':
                    print("❌ ISSUE: Description is empty!")
                elif len(description) < 50:
                    print("⚠️  WARNING: Description seems too short")
                elif 'Remote Company' in job.get('company', ''):
                    print("⚠️  WARNING: Company name is generic 'Remote Company'")
                else:
                    print("✅ Description looks good")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_job_details()
