# LinkedIn Job Scraper 🚀

A comprehensive LinkedIn job scraping solution with anti-detection measures, supporting both Python (Selenium) and Node.js (Puppeteer) implementations.

## ✨ Features

- **Anti-Detection**: Uses undetected-chromedriver and Puppeteer stealth plugins
- **Multiple Formats**: Export to CSV, JSON, and Excel
- **Batch Processing**: Run multiple search queries automatically
- **Rate Limiting**: Built-in delays to avoid getting blocked
- **Flexible Filtering**: Filter jobs by keywords, companies, etc.
- **Comprehensive Logging**: Detailed logs for debugging
- **Dual Implementation**: Both Python and Node.js versions
- **Easy Configuration**: Customizable settings via config files

## 📋 Requirements

### Python Version
- Python 3.7 or higher
- Google Chrome browser

### Node.js Version (Optional)
- Node.js 14 or higher
- Google Chrome browser

## 🛠️ Quick Setup

### 1. Clone/Download the Files
Make sure you have all the scraper files in your project directory.

### 2. Run Setup Script
```bash
python setup.py
```

This will:
- Install all Python dependencies
- Install Node.js dependencies (if Node.js is available)
- Create necessary directories
- Set up environment files
- Validate the installation

### 3. Manual Setup (Alternative)

#### Python Setup:
```bash
pip install -r requirements.txt
```

#### Node.js Setup:
```bash
cp package-scraper.json package.json
npm install
```

## 🎯 Usage

### Python Scraper

#### Basic Usage:
```python
from linkedin_job_scraper import LinkedInJobScraper

# Initialize scraper
scraper = LinkedInJobScraper(headless=False)

# Search for jobs
jobs = scraper.search_jobs(
    keywords="python developer",
    location="San Francisco, CA",
    experience_level="mid",
    job_type="full-time",
    max_pages=3
)

# Save results
scraper.save_to_csv(jobs)
scraper.save_to_json(jobs)
scraper.save_to_excel(jobs)

# Clean up
scraper.close()
```

#### Command Line:
```bash
python linkedin_job_scraper.py
```

#### Batch Processing:
```bash
python batch_scraper.py
```

### Node.js Scraper

#### Command Line:
```bash
node linkedin_scraper_node.js
# or
npm start
```

#### Programmatic Usage:
```javascript
const LinkedInJobScraperNode = require('./linkedin_scraper_node');

const scraper = new LinkedInJobScraperNode({
    headless: false,
    timeout: 30000
});

const jobs = await scraper.searchJobs(
    'javascript developer',
    'New York, NY',
    'mid',
    'full-time',
    3
);

await scraper.saveToCsv(jobs);
await scraper.close();
```

## ⚙️ Configuration

### Edit `config.py` for Python:

```python
# Search Configuration
DEFAULT_SEARCH_PARAMS = {
    "keywords": "your job keywords",
    "location": "Your City, State",
    "experience_level": "mid",  # internship, entry, associate, mid, senior, director, executive
    "job_type": "full-time",    # full-time, part-time, contract, temporary, internship, volunteer
    "max_pages": 5,
}

# Browser Configuration
BROWSER_CONFIG = {
    "headless": False,  # Set to True for headless mode
    "use_undetected": True,
    "timeout": 30,
}
```

### Available Experience Levels:
- `internship`
- `entry`
- `associate`
- `mid`
- `senior`
- `director`
- `executive`

### Available Job Types:
- `full-time`
- `part-time`
- `contract`
- `temporary`
- `internship`
- `volunteer`

## 📊 Output Formats

The scraper saves results in multiple formats:

### CSV Format:
```csv
title,company,location,posted_date,link,job_id,scraped_at
Software Engineer,Google,Mountain View CA,1 day ago,https://linkedin.com/jobs/view/123,123,2024-01-01T12:00:00
```

### JSON Format:
```json
[
  {
    "title": "Software Engineer",
    "company": "Google",
    "location": "Mountain View, CA",
    "posted_date": "1 day ago",
    "link": "https://linkedin.com/jobs/view/123",
    "job_id": "123",
    "scraped_at": "2024-01-01T12:00:00"
  }
]
```

### Excel Format:
- Multiple sheets with organized data
- Statistics and summary information
- Individual search results

## 🔄 Batch Processing

Create multiple search queries in `config.py`:

```python
SEARCH_QUERIES = [
    {
        "keywords": "python developer",
        "location": "San Francisco, CA",
        "experience_level": "mid",
        "job_type": "full-time",
        "max_pages": 3
    },
    {
        "keywords": "data scientist",
        "location": "New York, NY",
        "experience_level": "senior",
        "job_type": "full-time",
        "max_pages": 3
    }
]
```

Run batch processing:
```bash
python batch_scraper.py
```

## 🛡️ Anti-Detection Features

- **Undetected Chrome Driver**: Bypasses basic bot detection
- **Random User Agents**: Rotates browser user agents
- **Random Delays**: Mimics human browsing behavior
- **Stealth Plugins**: Advanced anti-detection for Puppeteer
- **Request Filtering**: Blocks unnecessary resources
- **Human-like Scrolling**: Gradual page scrolling

## 📝 Logging

All activities are logged to:
- `linkedin_scraper.log` (Python)
- `linkedin_scraper_node.log` (Node.js)
- Console output with colored messages

Log levels: DEBUG, INFO, WARNING, ERROR

## 🔧 Troubleshooting

### Common Issues:

#### 1. Chrome Driver Issues:
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager
```

#### 2. Selenium Issues:
```bash
# Reinstall selenium
pip uninstall selenium
pip install selenium==4.15.2
```

#### 3. No Jobs Found:
- Check if LinkedIn changed their HTML structure
- Update CSS selectors in `config.py`
- Try different search parameters
- Check internet connection

#### 4. Getting Blocked:
- Increase delays in rate limiting settings
- Use different IP/VPN
- Reduce the number of pages scraped
- Add more random delays

#### 5. Memory Issues:
- Enable headless mode
- Reduce `max_pages`
- Close browser between searches

### Debug Mode:
Run with debug settings:

```python
scraper = LinkedInJobScraper(headless=False, use_undetected=True)
```

Set logging to DEBUG in `config.py`:
```python
LOGGING_CONFIG = {
    "level": "DEBUG",
}
```

## ⚠️ Important Notes

### Legal and Ethical Considerations:
- **Respect robots.txt**: Check LinkedIn's robots.txt file
- **Terms of Service**: Review LinkedIn's ToS before scraping
- **Rate Limiting**: Don't overwhelm LinkedIn's servers
- **Personal Use**: Use for personal job searching, not commercial purposes
- **Data Privacy**: Handle scraped data responsibly

### Best Practices:
- Start with small searches (1-2 pages)
- Use appropriate delays between requests
- Monitor logs for any errors or warnings
- Don't run continuously for long periods
- Respect LinkedIn's infrastructure

## 📈 Performance Tips

1. **Use Headless Mode** for faster processing:
   ```python
   scraper = LinkedInJobScraper(headless=True)
   ```

2. **Optimize Page Count**:
   ```python
   max_pages=3  # Instead of 10+
   ```

3. **Batch Processing**:
   ```bash
   python batch_scraper.py  # More efficient than individual runs
   ```

4. **Filter Early**:
   ```python
   JOB_FILTERS = {
       "exclude_keywords": ["unpaid", "volunteer"],
       "required_keywords": ["python", "remote"]
   }
   ```

## 🆘 Support

If you encounter issues:

1. Check the logs for detailed error messages
2. Verify your configuration in `config.py`
3. Ensure Chrome browser is installed and updated
4. Try running with `headless=False` to see what's happening
5. Update CSS selectors if LinkedIn has changed

## 🔄 Updates

To update the scraper:

1. Check for LinkedIn HTML structure changes
2. Update CSS selectors in `config.py`
3. Update dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   npm update
   ```

## 📄 License

This project is for educational and personal use only. Please respect LinkedIn's terms of service and use responsibly.

---

**Happy Job Hunting! 🎯**