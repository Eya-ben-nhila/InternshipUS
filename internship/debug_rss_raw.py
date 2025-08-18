#!/usr/bin/env python3
"""
Debug RSS Raw Data - Examine the raw RSS feed structure
"""
import requests
import xml.etree.ElementTree as ET

def debug_rss_raw():
    """Debug the raw RSS feed data"""
    print("🔍 Debugging Raw RSS Feed Data")
    print("=" * 60)
    
    try:
        # Test RemoteOK RSS feed
        rss_url = "https://remoteok.io/remote-dev-jobs.rss"
        response = requests.get(rss_url, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            print(f"✅ Found {len(items)} items in RSS feed")
            print()
            
            # Examine first 3 items in detail
            for i, item in enumerate(items[:3], 1):
                print(f"ITEM {i}:")
                print("-" * 40)
                
                # Get all elements
                title = item.find('title')
                link = item.find('link')
                description = item.find('description')
                pub_date = item.find('pubDate')
                
                print(f"Title: '{title.text if title is not None else 'N/A'}'")
                print(f"Link: '{link.text if link is not None else 'N/A'}'")
                print(f"Pub Date: '{pub_date.text if pub_date is not None else 'N/A'}'")
                print(f"Description Length: {len(description.text) if description is not None else 0} chars")
                
                if description is not None:
                    desc_text = description.text
                    print(f"Description Preview: {desc_text[:200]}...")
                    
                    # Look for company name patterns in description
                    import re
                    
                    # Common company patterns in descriptions
                    company_patterns = [
                        r'About\s+([A-Z][a-zA-Z\s&]+?)(?:\s|\.|,|$)',
                        r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s|\.|,|$)',
                        r'([A-Z][a-zA-Z\s&]+?)\s+is\s+(?:a|an)',
                        r'([A-Z][a-zA-Z\s&]+?)\s+seeks',
                        r'([A-Z][a-zA-Z\s&]+?)\s+Global',
                        r'([A-Z][a-zA-Z\s&]+?)\s+Pro',
                    ]
                    
                    print("Company Patterns Found:")
                    for pattern in company_patterns:
                        matches = re.findall(pattern, desc_text, re.IGNORECASE)
                        if matches:
                            for match in matches[:3]:  # Show first 3 matches
                                company = match.strip()
                                if len(company) > 2 and len(company) < 50:
                                    print(f"  '{company}'")
                
                print()
                print("=" * 60)
                print()
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_rss_raw()
