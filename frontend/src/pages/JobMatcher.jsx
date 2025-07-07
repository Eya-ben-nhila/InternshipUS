import { useState } from 'react';

// Simulate fetching user profile (in real app, use context or props)
const getUserProfile = () => {
  return JSON.parse(localStorage.getItem('userProfile')) || {
    dreamJobs: [],
    activeDreamJobId: null,
    resumes: [
      { id: 1, name: 'Software Engineer Resume', score: 87, keywords: ['React', 'Node.js', 'Python'] },
      { id: 2, name: 'Product Manager Resume', score: 92, keywords: ['Product', 'Agile', 'Analytics'] },
      { id: 3, name: 'Data Scientist Resume', score: 78, keywords: ['Python', 'ML', 'SQL'] }
    ]
  };
};

export default function JobMatcher() {
  // Simulate user profile state
  const [userProfile, setUserProfile] = useState(getUserProfile());
  const activeDreamJob = userProfile.dreamJobs?.find(j => j.id === userProfile.activeDreamJobId);

  // Simulated jobs
  const [jobs] = useState([
    {
      id: 1,
      title: 'Senior Software Engineer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      type: 'Full-time',
      salary: '$120,000 - $150,000',
      tags: ['React', 'Node.js', 'AWS', 'TypeScript'],
      description: 'We are looking for a Senior Software Engineer to join our growing team building scalable web applications using React and Node.js. Experience with AWS and TypeScript is a plus.'
    },
    {
      id: 2,
      title: 'Product Manager',
      company: 'InnovateTech',
      location: 'New York, NY',
      type: 'Full-time',
      salary: '$100,000 - $130,000',
      tags: ['Product Strategy', 'Agile', 'User Research', 'Analytics'],
      description: 'Join our product team to drive innovation and user experience. Must have experience in Agile and analytics.'
    },
    {
      id: 3,
      title: 'Data Scientist',
      company: 'DataFlow Solutions',
      location: 'Austin, TX',
      type: 'Full-time',
      salary: '$110,000 - $140,000',
      tags: ['Python', 'Machine Learning', 'SQL', 'Statistics'],
      description: 'Help us build predictive models and data-driven solutions. Strong Python and ML background required.'
    }
  ]);

  // State for enhance modal
  const [showEnhance, setShowEnhance] = useState(false);
  const [enhanceData, setEnhanceData] = useState(null);

  // Simulate matching logic
  const getMatchScore = (job, dreamJob) => {
    if (!dreamJob) return 0;
    // Simple keyword overlap for demo
    const dreamWords = dreamJob.description.toLowerCase().split(/\W+/);
    const jobWords = job.description.toLowerCase().split(/\W+/);
    const overlap = dreamWords.filter(w => jobWords.includes(w)).length;
    return Math.min(100, 60 + overlap * 5);
  };

  // Find best resume for a job (by keyword overlap)
  const getBestResume = (job) => {
    if (!userProfile.resumes) return null;
    let best = null, bestScore = -1;
    for (const resume of userProfile.resumes) {
      const overlap = resume.keywords.filter(k => job.tags.includes(k)).length;
      if (overlap > bestScore) {
        best = resume;
        bestScore = overlap;
      }
    }
    return best;
  };

  // Simulate pros/cons and suggestions
  const getProsCons = (resume, job) => {
    const pros = resume.keywords.filter(k => job.tags.includes(k));
    const cons = job.tags.filter(k => !resume.keywords.includes(k));
    return {
      pros: pros.length ? pros : ['Relevant experience'],
      cons: cons.length ? cons : ['No major gaps']
    };
  };

  // Handle enhance resume
  const handleEnhance = (resume, job) => {
    const { cons } = getProsCons(resume, job);
    setEnhanceData({
      resume,
      job,
      suggestions: cons.map(c => `Add or highlight experience with "${c}" in your resume.`)
    });
    setShowEnhance(true);
  };

  return (
    <div className="js-job-match">
      <div className="js-job-match-container">
        <div className="js-job-match-header">
          <h2>Find Your Perfect Job Match</h2>
          <p>
            {activeDreamJob
              ? <>Matching jobs based on your dream job: <b>{activeDreamJob.title}</b></>
              : <>Please add and activate a dream job in your profile to get personalized matches.</>}
          </p>
        </div>
        {!activeDreamJob ? (
          <div style={{ color: '#dc2626', background: '#fef2f2', padding: 16, borderRadius: 8, marginBottom: 24 }}>
            No active dream job set. Go to your profile and add/activate a dream job to use this feature.
          </div>
        ) : null}
        <div className="js-jobs-grid">
          {jobs.map(job => {
            const matchScore = activeDreamJob ? getMatchScore(job, activeDreamJob) : 0;
            const bestResume = getBestResume(job);
            const { pros, cons } = bestResume ? getProsCons(bestResume, job) : { pros: [], cons: [] };
            return (
              <div key={job.id} className="js-job-card">
                <div className="js-job-title">{job.title}</div>
                <div className="js-job-company">{job.company}</div>
                <div className="js-job-location">{job.location} • {job.type}</div>
                <div className="js-job-tags">
                  {job.tags.map((tag, index) => (
                    <span key={index} className="js-job-tag">{tag}</span>
                  ))}
                </div>
                <div className="js-job-match-score">
                  <span className="js-match-percentage">{matchScore}% Match</span>
                </div>
                <p style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '1rem' }}>{job.description}</p>
                <div style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '1rem' }}>💰 {job.salary}</div>
                {bestResume && (
                  <div style={{ marginBottom: 8 }}>
                    <b>Best Resume:</b> {bestResume.name}
                  </div>
                )}
                <div style={{ marginBottom: 8 }}>
                  <b>Pros:</b> {pros.join(', ')}
                </div>
                <div style={{ marginBottom: 8 }}>
                  <b>Cons:</b> {cons.join(', ')}
                </div>
                {bestResume && (
                  <button className="js-apply-button" onClick={() => handleEnhance(bestResume, job)}>
                    Enhance Resume for this Job
                  </button>
                )}
              </div>
            );
          })}
        </div>
        {/* Enhance Resume Modal */}
        {showEnhance && enhanceData && (
          <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: '#0008', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
            <div style={{ background: '#fff', borderRadius: 12, padding: 32, minWidth: 320, maxWidth: 400, boxShadow: '0 8px 32px #0004' }}>
              <h3 style={{ color: '#2563eb', marginBottom: 12 }}>Enhance Resume</h3>
              <div style={{ marginBottom: 12 }}><b>Resume:</b> {enhanceData.resume.name}</div>
              <div style={{ marginBottom: 12 }}><b>Job:</b> {enhanceData.job.title}</div>
              <div style={{ marginBottom: 12 }}><b>Suggestions:</b>
                <ul style={{ margin: 0, paddingLeft: 20 }}>
                  {enhanceData.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              <button className="js-action-button primary" onClick={() => setShowEnhance(false)}>Close</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
