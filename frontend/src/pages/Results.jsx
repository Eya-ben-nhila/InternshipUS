export default function Results() {
  // Mock data - replace with real API results
  const results = {
    score: 78,
    matches: [
      { keyword: 'Project Management', found: true, count: 5 },
      { keyword: 'Agile Methodology', found: true, count: 3 },
      { keyword: 'Stakeholder Engagement', found: false },
      { keyword: 'Data Analysis', found: true, count: 2 },
      { keyword: 'Team Leadership', found: true, count: 4 },
      { keyword: 'Strategic Planning', found: false },
      { keyword: 'Budget Management', found: true, count: 1 },
      { keyword: 'Cross-functional Collaboration', found: false },
    ],
    suggestions: [
      'Add more metrics to quantify your achievements',
      'Include the term "Agile Methodology" 2-3 more times',
      'Reorder experience to highlight relevant positions first',
      'Add specific examples of stakeholder engagement',
      'Include more strategic planning experience'
    ]
  };

  return (
    <div className="js-results">
      <div className="js-results-container">
        <div className="js-results-header">
          <h2>Your Resume Analysis Results</h2>
          <p>Here's how well your resume matches the job description</p>
        </div>

        {/* Score Section */}
        <div className="js-score-section">
          <div className="js-score-circle">
            {results.score}
          </div>
          <div className="js-score-text">Match Score</div>
          <div className="js-score-value">{results.score}/100</div>
          <p>Your resume has a {results.score}% match with the job requirements</p>
        </div>

        {/* Keywords Section */}
        <div className="js-keywords-section">
          <h3>Keyword Analysis</h3>
          <div className="js-keywords-list">
            {results.matches.map((match, index) => (
              <div key={index} className={`js-keyword ${match.found ? 'found' : 'missing'}`}>
                {match.keyword}
                {match.found && <span> ({match.count}x)</span>}
              </div>
            ))}
          </div>
        </div>

        {/* Suggestions Section */}
        <div className="js-keywords-section">
          <h3>Optimization Suggestions</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {results.suggestions.map((suggestion, index) => (
              <li key={index} style={{ 
                padding: '0.75rem 0', 
                borderBottom: index < results.suggestions.length - 1 ? '1px solid #e2e8f0' : 'none',
                color: '#64748b'
              }}>
                • {suggestion}
              </li>
            ))}
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="js-results-actions">
          <button className="js-primary-button">Download PDF Report</button>
          <button className="js-secondary-button">Scan Another Resume</button>
        </div>
      </div>
    </div>
  );
}
