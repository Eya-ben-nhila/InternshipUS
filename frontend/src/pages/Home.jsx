export default function Home() {
  return (
    <div className="js-home">
      <section className="js-hero">
        <div className="js-hero-content">
          <h1>Optimize your resume for the job you want</h1>
          <p>Get past resume screeners and tracking systems with the best resume scanner</p>
          <div className="js-cta-buttons">
            <a href="/scan" className="js-primary-button">Resume & Job Matcher</a>
          </div>
          <div className="js-partner-logos">
            <img src="/logos/fortune500.png" alt="Fortune 500" />
            <img src="/logos/forbes.png" alt="Forbes" />
            <img src="/logos/wsj.png" alt="Wall Street Journal" />
          </div>
        </div>
        <div className="js-hero-image">
          <img src="/images/resume-scan-example.png" alt="Resume scanning example" />
        </div>
      </section>

      <section className="js-features">
        <div className="js-feature-card">
          <div className="js-feature-icon">🔍</div>
          <h3>ATS Compatibility Check</h3>
          <p>See how your resume performs in applicant tracking systems</p>
        </div>
        <div className="js-feature-card">
          <div className="js-feature-icon">📊</div>
          <h3>Resume Score</h3>
          <p>Get instant feedback on your resume's effectiveness</p>
        </div>
        <div className="js-feature-card">
          <div className="js-feature-icon">✨</div>
          <h3>Tailoring Suggestions</h3>
          <p>Learn how to customize your resume for each job</p>
        </div>
      </section>
    </div>
  );
}