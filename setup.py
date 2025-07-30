#!/usr/bin/env python3
"""
Setup script for LinkedIn Job Scraper
Installs dependencies and configures the environment.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed."""
    print("📦 Checking Node.js version...")
    try:
        result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} is installed")
            return True
        else:
            print("❌ Node.js is not installed")
            return False
    except Exception:
        print("❌ Node.js is not installed")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    print("📥 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python packages"):
        return False
    
    return True

def install_node_dependencies():
    """Install Node.js dependencies."""
    print("📥 Installing Node.js dependencies...")
    
    # Copy package.json for scraper
    if os.path.exists("package-scraper.json"):
        import shutil
        shutil.copy("package-scraper.json", "package.json")
        print("✅ Package.json copied for scraper")
    
    if not run_command("npm install", "Installing Node.js packages"):
        return False
    
    return True

def setup_chrome_driver():
    """Setup Chrome driver for Selenium."""
    print("🌐 Setting up Chrome driver...")
    
    # Check if Chrome is installed
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("⚠️  Chrome not found. Please install Google Chrome manually.")
        print("   Download from: https://www.google.com/chrome/")
    
    # The webdriver-manager will handle driver installation automatically
    print("✅ Chrome driver will be managed automatically by webdriver-manager")
    return True

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    
    directories = ["results", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def create_env_file():
    """Create .env file for environment variables."""
    print("⚙️  Creating .env file...")
    
    env_content = """# LinkedIn Job Scraper Environment Variables

# Email configuration (optional)
SCRAPER_EMAIL=""
SCRAPER_EMAIL_PASSWORD=""
NOTIFICATION_EMAIL=""

# Proxy configuration (optional)
HTTP_PROXY=""
HTTPS_PROXY=""

# API keys (if needed)
# LINKEDIN_API_KEY=""

# Advanced settings
DEBUG=false
LOG_LEVEL=INFO
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("ℹ️  .env file already exists")
    
    return True

def run_test():
    """Run a simple test to verify installation."""
    print("🧪 Running installation test...")
    
    try:
        # Test Python imports
        import selenium
        import pandas
        import requests
        print("✅ Python dependencies import successfully")
        
        # Test configuration
        from config import validate_config
        if validate_config():
            print("✅ Configuration validation passed")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def display_usage_instructions():
    """Display usage instructions."""
    print("\n" + "="*60)
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 USAGE INSTRUCTIONS:")
    print("\n🐍 Python Scraper:")
    print("   python linkedin_job_scraper.py")
    print("   python batch_scraper.py")
    print("   python config.py  # View configuration")
    
    print("\n📦 Node.js Scraper:")
    print("   node linkedin_scraper_node.js")
    print("   npm start")
    
    print("\n⚙️  Configuration:")
    print("   • Edit config.py to customize search parameters")
    print("   • Edit .env file for environment variables")
    print("   • Results will be saved in ./results/ directory")
    
    print("\n📚 Key Features:")
    print("   • Anti-detection measures with stealth plugins")
    print("   • Multiple output formats (CSV, JSON, Excel)")
    print("   • Batch processing for multiple searches")
    print("   • Rate limiting to avoid getting blocked")
    print("   • Comprehensive logging and error handling")
    
    print("\n⚠️  Important Notes:")
    print("   • Use responsibly and respect LinkedIn's terms of service")
    print("   • Don't scrape too aggressively to avoid IP blocking")
    print("   • Consider using delays between requests")
    print("   • Monitor logs for any issues")
    
    print("\n🔧 Troubleshooting:")
    print("   • Check linkedin_scraper.log for detailed logs")
    print("   • Ensure Chrome browser is installed")
    print("   • Try running with headless=False for debugging")
    print("   • Update CSS selectors if LinkedIn changes structure")

def main():
    """Main setup function."""
    print("🚀 LinkedIn Job Scraper Setup")
    print("="*50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check Node.js (optional)
    node_available = check_node_version()
    
    # Create directories
    if not create_directories():
        success = False
    
    # Create environment file
    if not create_env_file():
        success = False
    
    # Install Python dependencies
    if not install_python_dependencies():
        success = False
    
    # Install Node.js dependencies (if Node.js is available)
    if node_available:
        if not install_node_dependencies():
            print("⚠️  Node.js dependencies installation failed, but Python scraper will still work")
    else:
        print("ℹ️  Skipping Node.js setup (Node.js not available)")
    
    # Setup Chrome driver
    if not setup_chrome_driver():
        print("⚠️  Chrome driver setup had issues, but may still work")
    
    # Run test
    if success and not run_test():
        success = False
    
    if success:
        display_usage_instructions()
    else:
        print("\n❌ Setup completed with errors. Please check the messages above.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed with exception: {e}")
        sys.exit(1)