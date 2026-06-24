import requests
from bs4 import BeautifulSoup
import feedparser
import csv
from datetime import datetime

# Initialize a unified list to hold all events
unified_calendar = []

def fetch_rss_events(feed_url, source_name):
    """Extracts events from platforms providing RSS feeds (like DIGIT or blogs)"""
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        unified_calendar.append({
            'Source': source_name,
            'Title': entry.title,
            'Date/Time': entry.get('published', 'Check Link'),
            'Link': entry.link,
            'Location': 'See Link'
        })

def scrape_codebase_events():
    """Scrapes the CodeBase events page"""
    url = "https://thisiscodebase.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust class names based on target site's active CSS hierarchy
        events = soup.find_all('div', class_='event-card') 
        for event in events:
            title = event.find('h3').text.strip() if event.find('h3') else 'Unknown Event'
            date = event.find('time').text.strip() if event.find('time') else 'TBD'
            link = event.find('a')['href'] if event.find('a') else url
            
            unified_calendar.append({
                'Source': 'CodeBase',
                'Title': title,
                'Date/Time': date,
                'Link': link,
                'Location': 'Multi-hub / Hybrid'
            })
    except Exception as e:
        print(f"Error scraping CodeBase: {e}")

# --- EXECUTE THE AGGREGATION ---

# 1. Fetch from structured feeds (Examples - replace with direct platform feed URLs)
fetch_rss_events("https://digit.fyi", "DIGIT.fyi")
fetch_rss_events("https://opentechcalendar.co.uk", "Open Tech Calendar")

# 2. Fetch from standard web pages
scrape_codebase_events()

# --- SAVE TO A UNIFIED MASTER FILE ---
csv_filename = f"scotland_tech_calendar_master.csv"

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Source', 'Title', 'Date/Time', 'Location', 'Link'])
    writer.writeheader()
    for event in unified_calendar:
        writer.writerow(event)

print(f"Success! Compiled {len(unified_calendar)} events into {csv_filename}")
