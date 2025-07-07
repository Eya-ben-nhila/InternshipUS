import { useState } from 'react';

export default function Scanner() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Processing logic here
    console.log('Scanning resume...', { resumeFile, jobDesc });
  };

  return (
    <div className="js-scanner">
      <div className="js-scanner-container">
        <div className="js-scanner-header">
          <h2>Resume & Job Description Scanner</h2>
          <p>Upload your resume and paste the job description to get instant feedback on how well they match.</p>
        </div>
        
        <form onSubmit={handleSubmit} className="js-scanner-form">
          <div className="js-upload-section">
            <h3>Upload Your Resume</h3>
            <div className="js-upload-box">
              <input 
                type="file" 
                id="resume-upload" 
                accept=".pdf,.doc,.docx" 
                onChange={handleFileChange}
              />
              <label htmlFor="resume-upload">
                {resumeFile ? resumeFile.name : 'Choose File'}
              </label>
              <span>PDF, DOC, or DOCX (max 5MB)</span>
            </div>
          </div>

          <div className="js-job-desc-section">
            <h3>Paste Job Description</h3>
            <textarea
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
              placeholder="Copy and paste the job description here to analyze how well your resume matches the requirements..."
            />
          </div>

          <button type="submit" className="js-scan-button">
            Scan Resume
          </button>
        </form>
      </div>
    </div>
  );
}