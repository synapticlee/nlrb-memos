#!/usr/bin/env python3
"""
Simple NLRB General Counsel Memo Scraper
Saves the current state of memos to a file - any changes will trigger a commit
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import sys

def scrape_nlrb_memos():
    """Scrape the NLRB memos page and return structured data"""
    url = "https://www.nlrb.gov/guidance/memos-research/general-counsel-memos"
    
    try:
        print(f"Fetching {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract memo information
        memos = []
        memo_links = soup.find_all('a', href=True)
        
        for link in memo_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Filter for memo links (adjust pattern as needed)
            if ('memo' in href.lower() or 'gc-' in href.lower()) and text and len(text) > 5:
                # Create full URL if relative
                if href.startswith('/'):
                    href = f"https://www.nlrb.gov{href}"
                
                memos.append({
                    'title': text,
                    'url': href,
                    'found_date': datetime.now().isoformat()
                })
        
        # Sort by title for consistency
        memos.sort(key=lambda x: x['title'])
        
        print(f"Found {len(memos)} memos")
        return {
            'last_updated': datetime.now().isoformat(),
            'memo_count': len(memos),
            'memos': memos
        }
        
    except Exception as e:
        print(f"Error scraping memos: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print(f"Starting NLRB memo scrape at {datetime.now()}")
    
    # Scrape current memos
    memo_data = scrape_nlrb_memos()
    
    # Save to JSON file
    with open('nlrb_memos.json', 'w') as f:
        json.dump(memo_data, f, indent=2)
    
    print(f"Saved {memo_data['memo_count']} memos to nlrb_memos.json")
    print("Scrape completed successfully")

if __name__ == "__main__":
    main()
