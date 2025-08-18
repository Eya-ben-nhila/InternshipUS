#!/usr/bin/env python3
"""
Debug Parsing - Test the parsing logic with real job data
"""
import requests
import re

def extract_company_from_title(title):
    """Extract company name from job title"""
    patterns = [
        r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s*$|\s*-|\s*\(|\s*Remote)',
        r'-\s*([A-Z][a-zA-Z\s&]+?)(?:\s*$|\s*Remote)',
        r'([A-Z][a-zA-Z\s&]+?)\s*is\s+hiring',
        r'([A-Z][a-zA-Z\s&]+?)\s*seeks',
        r'([A-Z][a-zA-Z\s&]+?)\s*\(Remote\)',
        r'([A-Z][a-zA-Z\s&]+?)\s*Remote',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            if len(company) > 2 and len(company) < 50:
                return company
    
    return 'Remote Company'

def extract_company_from_description(description):
    """Extract company name from job description"""
    if not description:
        return 'Remote Company'
        
    # Clean the description first
    clean_desc = clean_html(description)
    
    # Company patterns commonly found in descriptions
    patterns = [
        r'([A-Z][a-zA-Z\s&]+?)\s+is\s+(?:a|an)\s+(?:fintech|digital|tech|software|company)',
        r'([A-Z][a-zA-Z\s&]+?)\s+Global',
        r'([A-Z][a-zA-Z\s&]+?)\s+Pro',
        r'([A-Z][a-zA-Z\s&]+?)\s+is\s+hiring',
        r'([A-Z][a-zA-Z\s&]+?)\s+company',
        r'([A-Z][a-zA-Z\s&]+?)\s+team',
        r'About\s+([A-Z][a-zA-Z\s&]+?)(?:\s|\.|,|$)',
        r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s|\.|,|$)',
        r'([A-Z][a-zA-Z\s&]+?)\s+seeks',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_desc, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            if len(company) > 2 and len(company) < 50:
                return company
    
    return 'Remote Company'

def clean_html(html_text):
    """Clean HTML tags from text"""
    if not html_text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', html_text)
    # Remove extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text)
    # Remove special characters
    clean_text = clean_text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    
    # Remove common unwanted text patterns
    unwanted_patterns = [
        r'TO BE CONSIDERED FOR THIS ROLE.*?TRANSLATE',
        r'CLICK HERE TO APPLY.*',
        r'APPLY NOW.*',
        r'Original job post link:.*?Original Job Post Link',
        r'D TO ENGLISH.*?Who is',
        r'ð About.*?We are',
        r'Â Â',
        r'ð',
    ]
    
    for pattern in unwanted_patterns:
        clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE | re.DOTALL)
    
    # Clean up any remaining artifacts
    clean_text = re.sub(r'\s+', ' ', clean_text)  # Remove extra spaces again
    clean_text = clean_text.strip()
    
    return clean_text

def extract_job_title(title):
    """Extract job title from full title"""
    if ' at ' in title:
        return title.split(' at ')[0].strip()
    elif ' - ' in title:
        return title.split(' - ')[0].strip()
    elif ' (' in title:
        return title.split(' (')[0].strip()
    return title

def debug_parsing():
    """Debug the parsing logic with real job data"""
    print("🔍 Debugging Job Parsing Logic")
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
            
            print(f"✅ Found {len(jobs)} jobs to analyze")
            print()
            
            for i, job in enumerate(jobs, 1):
                print(f"JOB {i}:")
                print(f"Original Title: '{job.get('title', 'N/A')}'")
                print(f"Company: '{job.get('company', 'N/A')}'")
                print(f"Description Length: {len(job.get('description', ''))} chars")
                print(f"Description Preview: {job.get('description', '')[:100]}...")
                print()
                
                # Test our parsing logic
                original_title = job.get('title', '')
                original_description = job.get('description', '')
                
                # Test new parsing logic
                extracted_company_from_desc = extract_company_from_description(original_description)
                extracted_company_from_title = extract_company_from_title(original_title)
                extracted_job_title = extract_job_title(original_title)
                
                # Use description first, then title
                final_company = extracted_company_from_desc if extracted_company_from_desc != 'Remote Company' else extracted_company_from_title
                
                print(f"Parsing Results:")
                print(f"  Company from Description: '{extracted_company_from_desc}'")
                print(f"  Company from Title: '{extracted_company_from_title}'")
                print(f"  Final Company: '{final_company}'")
                print(f"  Extracted Job Title: '{extracted_job_title}'")
                print()
                
                # Show what patterns would match
                print("Pattern Analysis:")
                patterns = [
                    r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s*$|\s*-|\s*\(|\s*Remote)',
                    r'-\s*([A-Z][a-zA-Z\s&]+?)(?:\s*$|\s*Remote)',
                    r'([A-Z][a-zA-Z\s&]+?)\s*is\s+hiring',
                    r'([A-Z][a-zA-Z\s&]+?)\s*seeks',
                    r'([A-Z][a-zA-Z\s&]+?)\s*\(Remote\)',
                    r'([A-Z][a-zA-Z\s&]+?)\s*Remote',
                ]
                
                for j, pattern in enumerate(patterns, 1):
                    match = re.search(pattern, original_title, re.IGNORECASE)
                    if match:
                        print(f"  Pattern {j} MATCHED: '{match.group(1).strip()}'")
                    else:
                        print(f"  Pattern {j}: No match")
                print("-" * 60)
                print()
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_parsing()
