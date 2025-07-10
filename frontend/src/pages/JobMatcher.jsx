import { useState } from 'react';

// Helper: extract keywords from text (simple split, remove stopwords, dedupe)
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

// Curated list of common work-related keywords (expand as needed)
const WORK_KEYWORDS = [
  'react', 'node.js', 'python', 'aws', 'typescript', 'agile', 'analytics', 'sql', 'machine learning', 'product', 'user research', 'statistics', 'project management', 'leadership', 'javascript', 'java', 'c++', 'docker', 'kubernetes', 'cloud', 'data', 'api', 'design', 'testing', 'scrum', 'jira', 'git', 'html', 'css', 'devops', 'linux'
];

// Extract up to 20 work-related keywords from job description
function extractWorkKeywords(description, max = 20) {
  if (!description) return [];
  // Split description into words, remove punctuation, lowercase
  const words = description
    .toLowerCase()
    .replace(/[^a-z0-9\s\+\#\.\-]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
  // Only include words that are in the WORK_KEYWORDS list
  const found = WORK_KEYWORDS.filter(keyword =>
    words.includes(keyword.toLowerCase())
  );
  // Remove duplicates and limit to max
  const unique = Array.from(new Set(found)).slice(0, max);
  console.log('Extracted work keywords:', unique); // Debugging
  return unique;
}

// Extract up to 20 keywords from job description only
function extractTopKeywords(text, max = 20) {
  if (!text) return [];
  const words = extractKeywords(text);
  return words.slice(0, max);
}

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

  // Improved matching logic: percentage of job tags found in resume keywords
  const getMatchScore = (job, resume) => {
    if (!resume) return 0;
    const resumeKeywords = resume.keywords || [];
    const jobKeywords = job.tags || [];
    if (jobKeywords.length === 0) return 0;
    const found = jobKeywords.filter(k => resumeKeywords.includes(k));
    const percent = Math.round((found.length / jobKeywords.length) * 100);
    return Math.max(0, Math.min(100, percent));
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
            // Extract up to 20 work-related keywords from job description
            const jobKeywords = extractWorkKeywords(job.description, 20);
            const bestResume = getBestResume({ ...job, tags: jobKeywords });
            const matchScore = bestResume ? getMatchScore({ ...job, tags: jobKeywords }, bestResume) : 0;
            const { pros, cons } = bestResume ? getProsCons(bestResume, { ...job, tags: jobKeywords }) : { pros: [], cons: [] };
            return (
              <div key={job.id} className="js-job-card">
                <div className="js-job-title">{job.title}</div>
                <div className="js-job-company">{job.company}</div>
                <div className="js-job-location">{job.location} • {job.type}</div>
                <div className="js-job-tags">
                  <b>Required Keywords:</b> {jobKeywords.map((tag, index) => (
                    <span key={index} className="js-job-tag">{tag}</span>
                  ))}
                </div>
                <div className="js-job-match-score">
                  <span className="js-match-percentage">{matchScore}% Match</span>
                </div>
                {/* Remove any display or extraction of keywords from job.description */}
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
                {bestResume ? (
                  <button className="js-apply-button" onClick={() => handleEnhance(bestResume, job)}>
                    Enhance Resume for this Job
                  </button>
                ) : (
                  <button className="js-apply-button" disabled title="No resume available">
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
