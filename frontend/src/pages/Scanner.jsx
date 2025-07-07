import { useState } from 'react';

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
  }
  return '';
}

export default function Scanner() {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobFile, setJobFile] = useState(null);
  const [jobText, setJobText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResumeFile = async (e) => {
    const file = e.target.files[0];
    setResumeFile(file);
    setLoading(true);
    const text = await extractTextFromFile(file);
    setResumeText(text);
    setLoading(false);
  };

  const handleJobFile = async (e) => {
    const file = e.target.files[0];
    setJobFile(file);
    setLoading(true);
    const text = await extractTextFromFile(file);
    setJobText(text);
    setLoading(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!resumeText.trim() || !jobText.trim()) return;
    
    const resumeKeywords = extractKeywords(resumeText);
    const jobKeywords = extractKeywords(jobText);
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
          <div className="js-upload-section">
            <h3>Upload Your Resume</h3>
            <div className="js-upload-box">
              <input type="file" id="resume-upload" accept=".txt" onChange={handleResumeFile} />
              <label htmlFor="resume-upload">{resumeFile ? resumeFile.name : 'Choose TXT File'}</label>
              <span>TXT files only (max 5MB)</span>
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
              <input type="file" id="job-upload" accept=".txt" onChange={handleJobFile} />
              <label htmlFor="job-upload">{jobFile ? jobFile.name : 'Choose TXT File'}</label>
              <span>TXT files only (max 5MB)</span>
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