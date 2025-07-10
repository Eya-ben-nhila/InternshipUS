import { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist/build/pdf';
import 'pdfjs-dist/build/pdf.worker.entry';
pdfjsLib.GlobalWorkerOptions.workerSrc = '/node_modules/pdfjs-dist/build/pdf.worker.entry.js';

// Simple keyword extraction (same as JobMatcher)
const stopwords = new Set(['the','and','a','an','to','of','in','on','for','with','by','at','is','are','as','be','from','that','this','it','our','we','you','your','us','will','must','have','has','was','were','or','but','if','then','so','not','can','should','may','do','does','did','using','used','into','out','about','over','under','more','less','than','such','these','those','their','which','who','what','when','where','how','why','all','any','each','other','some','most','many','much','very','just','also','too','both','either','neither','own','same','new','now','after','before','again','once']);

function extractKeywords(text) {
  if (!text) return [];
  return Array.from(new Set(
    text
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(/\s+/)
      .filter(w => w && !stopwords.has(w))
  ));
}

async function extractTextFromFile(file) {
  if (!file) return '';
  const ext = file.name.split('.').pop().toLowerCase();
  if (ext === 'txt') {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.readAsText(file);
    });
  } else if (ext === 'pdf') {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const typedarray = new Uint8Array(e.target.result);
          const pdf = await pdfjsLib.getDocument({ data: typedarray }).promise;
          let text = '';
          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            // Join text items in reading order, separated by spaces
            const pageText = content.items.map(item => item.str).join(' ');
            text += pageText + '\n';
          }
          // Clean up excessive whitespace
          text = text.replace(/\s+/g, ' ').replace(/\n+/g, '\n').trim();
          resolve(text);
        } catch (err) {
          reject(err);
        }
      };
      reader.onerror = (err) => reject(err);
      reader.readAsArrayBuffer(file);
    });
  }
  return '';
}

// Extract only the job description section from the text
function extractJobDescriptionSection(text) {
  if (!text) return '';
  // Look for common section headers
  const descStart = text.search(/job description|description/i);
  if (descStart === -1) return text; // fallback: use all text
  // Find where the description ends (next section header)
  const afterDesc = text.slice(descStart);
  const endMatch = afterDesc.search(/requirements|qualifications|responsibilities|skills|benefits|about|who you are|what you will do|compensation|salary|education|experience/i);
  if (endMatch === -1) return afterDesc.trim();
  return afterDesc.slice(0, endMatch).trim();
}

// Large curated list of work-related keywords (expand as needed)
const WORK_KEYWORDS = [
  'react', 'node.js', 'python', 'aws', 'typescript', 'agile', 'analytics', 'sql', 'machine learning', 'product management', 'user research', 'statistics', 'project management', 'leadership', 'javascript', 'java', 'c++', 'docker', 'kubernetes', 'cloud', 'data analysis', 'api', 'ui/ux', 'design', 'testing', 'scrum', 'jira', 'git', 'html', 'css', 'devops', 'linux', 'project manager', 'software engineer', 'data scientist', 'product manager', 'business analyst', 'qa', 'automation', 'frontend', 'backend', 'full stack', 'mobile', 'ios', 'android', 'azure', 'gcp', 'rest', 'graphql', 'php', 'ruby', 'go', 'swift', 'objective-c', 'scala', 'perl', 'r', 'matlab', 'sas', 'tableau', 'power bi', 'excel', 'salesforce', 'sap', 'oracle', 'erp', 'crm', 'networking', 'security', 'penetration testing', 'compliance', 'blockchain', 'ai', 'ml', 'nlp', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'hadoop', 'spark', 'hive', 'pig', 'flink', 'cassandra', 'mongodb', 'postgresql', 'mysql', 'sqlite', 'firebase', 'redux', 'vue', 'angular', 'svelte', 'bootstrap', 'tailwind', 'sass', 'less', 'webpack', 'babel', 'eslint', 'prettier', 'jest', 'mocha', 'chai', 'cypress', 'puppeteer', 'playwright', 'selenium', 'confluence', 'trello', 'asana', 'notion', 'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'invision', 'zeplin'
];

// Extract work-related keywords from job description section
function extractWorkKeywordsFromText(text, max = 20) {
  if (!text) return [];
  const lowerText = text.toLowerCase();
  // Only match whole words/phrases from the curated list
  const found = WORK_KEYWORDS.filter(keyword => {
    // For multi-word keywords, use includes; for single words, use word boundary
    if (keyword.includes(' ')) {
      return lowerText.includes(keyword.toLowerCase());
    } else {
      return new RegExp(`\\b${keyword}\\b`, 'i').test(lowerText);
    }
  });
  return Array.from(new Set(found)).slice(0, max);
}

export default function Scanner() {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobFile, setJobFile] = useState(null);
  const [jobText, setJobText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleResumeFile = async (e) => {
    const file = e.target.files[0];
    setResumeFile(file);
    setLoading(true);
    try {
      const text = await extractTextFromFile(file);
      console.log('Extracted resume text:', text);
      setResumeText(text);
      setLoading(false);
      if (!text.trim()) {
        setError('Could not extract text from the uploaded resume file. Please try another file or paste the text manually.');
      } else {
        setError('');
      }
    } catch (err) {
      setResumeText('');
      setLoading(false);
      setError('Error extracting text from resume: ' + (err.message || err));
    }
  };

  const handleJobFile = async (e) => {
    const file = e.target.files[0];
    setJobFile(file);
    setLoading(true);
    try {
      let text = await extractTextFromFile(file);
      // Only use the job description section
      text = extractJobDescriptionSection(text);
      console.log('Extracted job description section:', text);
      setJobText(text);
      setLoading(false);
      if (!text.trim()) {
        setError('Could not extract the job description section from the uploaded job file. Please try another file or paste the description manually.');
      } else {
        setError('');
      }
    } catch (err) {
      setJobText('');
      setLoading(false);
      setError('Error extracting text from job description: ' + (err.message || err));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!resumeText.trim() || !jobText.trim()) return;
    
    const resumeKeywords = extractKeywords(resumeText);
    const jobKeywords = extractWorkKeywordsFromText(jobText, 20);
    const found = jobKeywords.filter(k => resumeKeywords.includes(k));
    const missing = jobKeywords.filter(k => !resumeKeywords.includes(k));
    const score = jobKeywords.length ? Math.round((found.length / jobKeywords.length) * 100) : 0;
    
    setResults({ 
      score, 
      found, 
      missing, 
      suggestions: missing.map(k => `Add or highlight "${k}" in your resume.`) 
    });
  };

  return (
    <div className="js-scanner">
      <div className="js-scanner-container">
        <div className="js-scanner-header">
          <h2>Resume & Job Description Scanner</h2>
          <p>Upload your resume and job description as TXT files, or paste the text below. Get instant feedback on how well they match.</p>
        </div>
        
        <form onSubmit={handleSubmit} className="js-scanner-form">
          {error && (
            <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>
          )}
          {/* Debug: Show extracted job description section */}
          {jobText && (
            <div style={{ background: '#f3f4f6', color: '#334155', padding: 8, borderRadius: 6, marginBottom: 12, fontSize: '0.95em' }}>
              <b>Extracted Job Description Section:</b>
              <div style={{ whiteSpace: 'pre-wrap', marginTop: 4 }}>{jobText}</div>
            </div>
          )}
          <div className="js-upload-section">
            <h3>Upload Your Resume</h3>
            <div className="js-upload-box">
              <input type="file" id="resume-upload" accept=".txt,.pdf" onChange={handleResumeFile} />
              <label htmlFor="resume-upload">{resumeFile ? resumeFile.name : 'Choose TXT File'}</label>
              <span>TXT or PDF files only (max 5MB)</span>
            </div>
            <textarea
              value={resumeText}
              onChange={e => setResumeText(e.target.value)}
              placeholder="Or paste your resume text here..."
              style={{ width: '100%', minHeight: 100, marginTop: 12 }}
            />
          </div>
          
          <div className="js-job-desc-section">
            <h3>Upload Job Description</h3>
            <div className="js-upload-box">
              <input type="file" id="job-upload" accept=".txt,.pdf" onChange={handleJobFile} />
              <label htmlFor="job-upload">{jobFile ? jobFile.name : 'Choose TXT File'}</label>
              <span>TXT or PDF files only (max 5MB)</span>
            </div>
            <textarea
              value={jobText}
              onChange={e => setJobText(e.target.value)}
              placeholder="Or paste the job description here..."
              style={{ width: '100%', minHeight: 100, marginTop: 12 }}
            />
          </div>
          
          <button type="submit" className="js-scan-button" disabled={loading || !resumeText.trim() || !jobText.trim()}>
            {loading ? 'Extracting...' : 'Scan Resume'}
          </button>
        </form>
        
        {results && (
          <div style={{ marginTop: 32, background: '#fff', borderRadius: 12, padding: 24, boxShadow: '0 4px 16px #2563eb22', border: '1px solid #e2e8f0' }}>
            <h3 style={{ color: '#2563eb', marginBottom: 12 }}>Scan Results</h3>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: '#2563eb', marginBottom: 8 }}>{results.score}% Match</div>
            <div style={{ marginBottom: 16, color: '#64748b' }}>Your resume matches {results.found.length} out of {results.found.length + results.missing.length} keywords from the job description.</div>
            <div style={{ marginBottom: 12 }}>
              <b>Found Keywords:</b> {results.found.length ? results.found.map(k => <span key={k} style={{ background: '#dcfce7', color: '#166534', borderRadius: 20, padding: '4px 12px', marginRight: 6, fontSize: '0.95em' }}>{k}</span>) : <span style={{ color: '#dc2626' }}>None</span>}
            </div>
            <div style={{ marginBottom: 12 }}>
              <b>Missing Keywords:</b> {results.missing.length ? results.missing.map(k => <span key={k} style={{ background: '#fef2f2', color: '#dc2626', borderRadius: 20, padding: '4px 12px', marginRight: 6, fontSize: '0.95em' }}>{k}</span>) : <span style={{ color: '#2563eb' }}>None</span>}
            </div>
            <div style={{ marginBottom: 12 }}>
              <b>Suggestions:</b>
              <ul style={{ margin: 0, paddingLeft: 20 }}>
                {results.suggestions.length ? results.suggestions.map((s, i) => <li key={i}>{s}</li>) : <li>No suggestions. Great match!</li>}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}