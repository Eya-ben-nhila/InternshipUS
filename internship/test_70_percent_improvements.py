#!/usr/bin/env python3
"""
Test script to verify improvements for 70%+ matches
"""

import requests
import json
import time

def test_70_percent_improvements():
    """Test the improved matching algorithm for 70%+ matches"""
    
    print("🧪 Testing ULTRA-EXPANDED Job Search for 70%+ Matches...")
    print("=" * 60)
    
    # Test queries that should get high matches
    test_queries = [
        "Director of Data and AI Governance",
        "Data Scientist",
        "Machine Learning Engineer", 
        "Data Engineer",
        "AI Engineer",
        "Senior Data Scientist",
        "Lead Machine Learning Engineer"
    ]
    
    total_jobs = 0
    high_match_jobs = 0
    
    for query in test_queries:
        print(f"\n🔍 Testing: {query}")
        
        try:
            # Make API request
            url = "http://localhost:5000/api/jobs"
            params = {
                'query': query,
                'limit': 50
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                
                print(f"   ✅ Found {len(jobs)} jobs")
                
                # Count high relevance jobs (70%+)
                high_relevance = [job for job in jobs if job.get('relevance_score', 0) >= 70]
                medium_relevance = [job for job in jobs if 50 <= job.get('relevance_score', 0) < 70]
                
                print(f"   🎯 High relevance (70%+): {len(high_relevance)} jobs")
                print(f"   📊 Medium relevance (50-69%): {len(medium_relevance)} jobs")
                
                # Show top 3 jobs by relevance
                sorted_jobs = sorted(jobs, key=lambda x: x.get('relevance_score', 0), reverse=True)
                print(f"   🏆 Top 3 jobs by relevance:")
                for i, job in enumerate(sorted_jobs[:3], 1):
                    score = job.get('relevance_score', 0)
                    title = job.get('title', 'Unknown')[:50]
                    source = job.get('source', 'Unknown')
                    print(f"      {i}. {score}% - {title} ({source})")
                
                total_jobs += len(jobs)
                high_match_jobs += len(high_relevance)
                
            else:
                print(f"   ❌ API request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Brief pause between requests
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print(f"Total jobs found: {total_jobs}")
    print(f"High relevance jobs (70%+): {high_match_jobs}")
    
    if total_jobs > 0:
        percentage = (high_match_jobs / total_jobs) * 100
        print(f"Percentage of high relevance jobs: {percentage:.1f}%")
        
        if percentage >= 30:
            print("🎉 EXCELLENT! High percentage of 70%+ matches achieved!")
        elif percentage >= 20:
            print("✅ GOOD! Significant improvement in 70%+ matches!")
        else:
            print("📈 IMPROVEMENT NEEDED: Working on increasing 70%+ matches...")
    else:
        print("❌ No jobs found - check if the API is running")

if __name__ == "__main__":
    test_70_percent_improvements()
