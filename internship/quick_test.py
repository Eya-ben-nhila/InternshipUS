#!/usr/bin/env python3
"""
Quick Test for Job Details Improvements
"""

import requests

r = requests.get('http://localhost:5000/api/jobs', params={'query': 'developer', 'limit': 10}, timeout=60)
data = r.json()
sources = set(job.get('source') for job in data.get('data', []))
print(f'Found jobs from sources: {sources}')
print(f'Total jobs: {len(data.get("data", []))}')
