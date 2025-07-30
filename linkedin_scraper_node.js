#!/usr/bin/env node

/**
 * LinkedIn Job Scraper - Node.js Version
 * A comprehensive tool for scraping job listings from LinkedIn using Puppeteer
 * with anti-detection measures and stealth plugins.
 */

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker');
const UserAgent = require('user-agents');
const fs = require('fs-extra');
const path = require('path');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const XLSX = require('xlsx');
const winston = require('winston');
const delay = require('delay');

// Add stealth plugin and adblocker
puppeteer.use(StealthPlugin());
puppeteer.use(AdblockerPlugin({ blockTrackers: true }));

class LinkedInJobScraperNode {
    constructor(options = {}) {
        this.options = {
            headless: options.headless !== false,
            timeout: options.timeout || 30000,
            minDelay: options.minDelay || 2000,
            maxDelay: options.maxDelay || 5000,
            ...options
        };
        
        this.browser = null;
        this.page = null;
        this.jobs = [];
        this.userAgent = new UserAgent();
        
        // Setup logging
        this.logger = winston.createLogger({
            level: 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.errors({ stack: true }),
                winston.format.printf(({ timestamp, level, message, stack }) => {
                    return `${timestamp} [${level.toUpperCase()}]: ${message}${stack ? '\n' + stack : ''}`;
                })
            ),
            transports: [
                new winston.transports.File({ filename: 'linkedin_scraper_node.log' }),
                new winston.transports.Console()
            ]
        });
    }

    async init() {
        try {
            this.logger.info('Initializing browser...');
            
            this.browser = await puppeteer.launch({
                headless: this.options.headless,
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--disable-features=VizDisplayCompositor',
                    '--window-size=1920,1080'
                ],
                defaultViewport: { width: 1920, height: 1080 }
            });

            this.page = await this.browser.newPage();
            
            // Set random user agent
            await this.page.setUserAgent(this.userAgent.toString());
            
            // Set additional headers
            await this.page.setExtraHTTPHeaders({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            });

            // Enable request interception for additional stealth
            await this.page.setRequestInterception(true);
            this.page.on('request', (req) => {
                if (req.resourceType() === 'image' || req.resourceType() === 'stylesheet') {
                    req.abort();
                } else {
                    req.continue();
                }
            });

            this.logger.info('Browser initialized successfully');
        } catch (error) {
            this.logger.error('Failed to initialize browser:', error);
            throw error;
        }
    }

    async randomDelay(min = null, max = null) {
        const minDelay = min || this.options.minDelay;
        const maxDelay = max || this.options.maxDelay;
        const delayTime = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;
        await delay(delayTime);
    }

    async scrollPage(scrollCount = 3) {
        for (let i = 0; i < scrollCount; i++) {
            await this.page.evaluate(() => {
                window.scrollTo(0, document.body.scrollHeight);
            });
            await this.randomDelay(1000, 2000);
        }
    }

    buildSearchUrl(keywords, location = '', experienceLevel = '', jobType = '') {
        const baseUrl = 'https://www.linkedin.com/jobs/search';
        const params = new URLSearchParams();
        
        if (keywords) params.append('keywords', keywords);
        if (location) params.append('location', location);
        if (experienceLevel) params.append('f_E', this.getExperienceCode(experienceLevel));
        if (jobType) params.append('f_JT', this.getJobTypeCode(jobType));
        params.append('sortBy', 'DD'); // Sort by date posted
        
        return `${baseUrl}?${params.toString()}`;
    }

    getExperienceCode(level) {
        const experienceMap = {
            'internship': '1',
            'entry': '2',
            'associate': '3',
            'mid': '4',
            'senior': '5',
            'director': '6',
            'executive': '7'
        };
        return experienceMap[level?.toLowerCase()] || '';
    }

    getJobTypeCode(jobType) {
        const jobTypeMap = {
            'full-time': 'F',
            'part-time': 'P',
            'contract': 'C',
            'temporary': 'T',
            'internship': 'I',
            'volunteer': 'V'
        };
        return jobTypeMap[jobType?.toLowerCase()] || '';
    }

    async searchJobs(keywords, location = '', experienceLevel = '', jobType = '', maxPages = 5) {
        if (!this.browser) {
            await this.init();
        }

        const jobs = [];
        const searchUrl = this.buildSearchUrl(keywords, location, experienceLevel, jobType);

        try {
            this.logger.info(`Starting job search: ${keywords} in ${location}`);
            this.logger.info(`Search URL: ${searchUrl}`);

            await this.page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: this.options.timeout });
            await this.randomDelay(3000, 5000);

            for (let pageNum = 0; pageNum < maxPages; pageNum++) {
                this.logger.info(`Scraping page ${pageNum + 1}`);

                // Scroll to load more jobs
                await this.scrollPage(3);

                // Extract jobs from current page
                const pageJobs = await this.extractJobCards();
                jobs.push(...pageJobs);

                this.logger.info(`Found ${pageJobs.length} jobs on page ${pageNum + 1}`);

                // Navigate to next page
                if (pageNum < maxPages - 1) {
                    const hasNextPage = await this.goToNextPage();
                    if (!hasNextPage) {
                        this.logger.info('No more pages available');
                        break;
                    }
                }

                await this.randomDelay(3000, 6000);
            }

            this.logger.info(`Total jobs scraped: ${jobs.length}`);
            return jobs;

        } catch (error) {
            this.logger.error('Error during job search:', error);
            return jobs;
        }
    }

    async extractJobCards() {
        try {
            // Wait for job cards to load
            await this.page.waitForSelector('.job-search-card, .jobs-search-results__list-item', 
                { timeout: 10000 });

            return await this.page.evaluate(() => {
                const jobCards = document.querySelectorAll('.job-search-card, .jobs-search-results__list-item');
                const jobs = [];

                jobCards.forEach(card => {
                    try {
                        const job = {};

                        // Job title
                        const titleElement = card.querySelector('h3 a, .job-search-card__title a, [data-test-job-title] a');
                        job.title = titleElement ? titleElement.innerText.trim() : 'N/A';

                        // Company name
                        const companyElement = card.querySelector('h4 a, .job-search-card__subtitle a, [data-test-employer-name]');
                        job.company = companyElement ? companyElement.innerText.trim() : 'N/A';

                        // Location
                        const locationElement = card.querySelector('.job-search-card__location, [data-test-job-location]');
                        job.location = locationElement ? locationElement.innerText.trim() : 'N/A';

                        // Job link
                        const linkElement = card.querySelector('h3 a, .job-search-card__title a, [data-test-job-title] a');
                        job.link = linkElement ? linkElement.href : 'N/A';

                        // Posted date
                        const dateElement = card.querySelector('.job-search-card__listdate, time, [data-test-job-posted-date]');
                        job.posted_date = dateElement ? dateElement.innerText.trim() : 'N/A';

                        // Job ID
                        if (job.link && job.link !== 'N/A') {
                            const urlParts = job.link.split('/');
                            const jobIdMatch = job.link.match(/jobs\/view\/(\d+)/);
                            job.job_id = jobIdMatch ? jobIdMatch[1] : 'N/A';
                        } else {
                            job.job_id = 'N/A';
                        }

                        // Additional metadata
                        job.scraped_at = new Date().toISOString();

                        // Only add if we have essential data
                        if (job.title !== 'N/A' && job.company !== 'N/A') {
                            jobs.push(job);
                        }
                    } catch (error) {
                        console.warn('Error extracting single job:', error);
                    }
                });

                return jobs;
            });

        } catch (error) {
            this.logger.error('Error extracting job cards:', error);
            return [];
        }
    }

    async goToNextPage() {
        try {
            const nextButton = await this.page.$('button[aria-label="Next"], .artdeco-pagination__button--next');
            
            if (nextButton) {
                const isDisabled = await this.page.evaluate(btn => btn.disabled, nextButton);
                if (!isDisabled) {
                    await nextButton.click();
                    await this.page.waitForNavigation({ waitUntil: 'networkidle2', timeout: this.options.timeout });
                    await this.randomDelay(3000, 5000);
                    return true;
                }
            }
            return false;
        } catch (error) {
            this.logger.warn('Error navigating to next page:', error);
            return false;
        }
    }

    async getJobDetails(jobUrl) {
        try {
            await this.page.goto(jobUrl, { waitUntil: 'networkidle2', timeout: this.options.timeout });
            await this.randomDelay(2000, 4000);

            return await this.page.evaluate(() => {
                const details = {};

                // Job description
                const descElement = document.querySelector('.jobs-description-content__text, .jobs-box__html-content');
                details.description = descElement ? descElement.innerText.trim() : 'N/A';

                // Company size and industry
                const companyInsights = document.querySelectorAll('.jobs-company__box dd');
                if (companyInsights.length >= 2) {
                    details.company_size = companyInsights[0].innerText.trim();
                    details.industry = companyInsights[1].innerText.trim();
                } else {
                    details.company_size = 'N/A';
                    details.industry = 'N/A';
                }

                return details;
            });

        } catch (error) {
            this.logger.error('Error getting job details:', error);
            return {};
        }
    }

    async saveToJson(jobs, filename = null) {
        if (!filename) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            filename = `linkedin_jobs_${timestamp}.json`;
        }

        try {
            await fs.writeJson(filename, jobs, { spaces: 2 });
            this.logger.info(`Jobs saved to ${filename}`);
            return filename;
        } catch (error) {
            this.logger.error('Error saving to JSON:', error);
            return '';
        }
    }

    async saveToCsv(jobs, filename = null) {
        if (!filename) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            filename = `linkedin_jobs_${timestamp}.csv`;
        }

        try {
            if (jobs.length === 0) {
                this.logger.warn('No jobs to save to CSV');
                return '';
            }

            const csvWriter = createCsvWriter({
                path: filename,
                header: [
                    { id: 'title', title: 'Title' },
                    { id: 'company', title: 'Company' },
                    { id: 'location', title: 'Location' },
                    { id: 'posted_date', title: 'Posted Date' },
                    { id: 'link', title: 'Link' },
                    { id: 'job_id', title: 'Job ID' },
                    { id: 'scraped_at', title: 'Scraped At' }
                ]
            });

            await csvWriter.writeRecords(jobs);
            this.logger.info(`Jobs saved to ${filename}`);
            return filename;
        } catch (error) {
            this.logger.error('Error saving to CSV:', error);
            return '';
        }
    }

    async saveToExcel(jobs, filename = null) {
        if (!filename) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            filename = `linkedin_jobs_${timestamp}.xlsx`;
        }

        try {
            const worksheet = XLSX.utils.json_to_sheet(jobs);
            const workbook = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(workbook, worksheet, 'Jobs');
            XLSX.writeFile(workbook, filename);
            
            this.logger.info(`Jobs saved to ${filename}`);
            return filename;
        } catch (error) {
            this.logger.error('Error saving to Excel:', error);
            return '';
        }
    }

    async close() {
        if (this.browser) {
            await this.browser.close();
            this.logger.info('Browser closed');
        }
    }
}

// Example usage
async function main() {
    const scraper = new LinkedInJobScraperNode({
        headless: false, // Set to true for headless mode
        timeout: 30000
    });

    try {
        const searchParams = {
            keywords: 'javascript developer',
            location: 'New York, NY',
            experienceLevel: 'mid',
            jobType: 'full-time',
            maxPages: 3
        };

        console.log('🚀 Starting LinkedIn job search...');
        console.log(`Keywords: ${searchParams.keywords}`);
        console.log(`Location: ${searchParams.location}`);
        console.log(`Experience: ${searchParams.experienceLevel}`);
        console.log(`Type: ${searchParams.jobType}`);
        console.log(`Max pages: ${searchParams.maxPages}`);
        console.log('-'.repeat(50));

        const jobs = await scraper.searchJobs(
            searchParams.keywords,
            searchParams.location,
            searchParams.experienceLevel,
            searchParams.jobType,
            searchParams.maxPages
        );

        if (jobs.length > 0) {
            console.log(`✅ Found ${jobs.length} jobs!`);

            // Save to different formats
            const csvFile = await scraper.saveToCsv(jobs);
            const jsonFile = await scraper.saveToJson(jobs);
            const excelFile = await scraper.saveToExcel(jobs);

            console.log('📁 Results saved to:');
            console.log(`  • CSV: ${csvFile}`);
            console.log(`  • JSON: ${jsonFile}`);
            console.log(`  • Excel: ${excelFile}`);

            // Display sample jobs
            console.log('\n📋 Sample jobs:');
            jobs.slice(0, 5).forEach((job, index) => {
                console.log(`${index + 1}. ${job.title} at ${job.company}`);
                console.log(`   📍 ${job.location}`);
                console.log(`   🔗 ${job.link}`);
                console.log(`   📅 ${job.posted_date}`);
                console.log();
            });
        } else {
            console.log('❌ No jobs found. Try adjusting your search parameters.');
        }

    } catch (error) {
        console.error('❌ An error occurred:', error);
    } finally {
        await scraper.close();
    }
}

// Run if this file is executed directly
if (require.main === module) {
    main().catch(console.error);
}

module.exports = LinkedInJobScraperNode;