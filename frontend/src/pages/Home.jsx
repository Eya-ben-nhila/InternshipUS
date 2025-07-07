export default function Home() {
  return (
    <div className="js-home">
      {/* Hero Section */}
      <section className="js-hero">
        <div className="js-hero-content">
          <h1>Optimize your resume for the job you want</h1>
          <p>Get past resume screeners and tracking systems with the most advanced resume scanner. Our AI-powered tool analyzes your resume against job descriptions to help you land more interviews.</p>
          <div className="js-cta-buttons">
            <a href="/scan" className="js-primary-button">Scan Your Resume</a>
            <a href="#features" className="js-secondary-button">See How It Works</a>
          </div>
        </div>
        <div className="js-hero-image">
          <div style={{
            width: '100%',
            height: '400px',
            background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(255,255,255,0.2)'
          }}>
            <div style={{ textAlign: 'center', color: 'rgba(255,255,255,0.8)' }}>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📄</div>
              <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>Resume Scanner Demo</div>
              <div style={{ fontSize: '1rem', opacity: 0.8 }}>Upload your resume to see the magic</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="js-features-section">
        <div className="js-features-container">
          <div className="js-features-header">
            <h2>Why Choose ResumeScan?</h2>
            <p>Our advanced technology helps you create resumes that get noticed by both human recruiters and ATS systems.</p>
          </div>
          
          <div className="js-features">
            <div className="js-feature-card">
              <div className="js-feature-icon">🔍</div>
              <h3>ATS Compatibility Check</h3>
              <p>See how your resume performs in applicant tracking systems used by 99% of Fortune 500 companies.</p>
            </div>
            <div className="js-feature-card">
              <div className="js-feature-icon">📊</div>
              <h3>Resume Score</h3>
              <p>Get instant feedback on your resume's effectiveness with our proprietary scoring algorithm.</p>
            </div>
            <div className="js-feature-card">
              <div className="js-feature-icon">✨</div>
              <h3>Tailoring Suggestions</h3>
              <p>Learn how to customize your resume for each job with specific keyword and content recommendations.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}