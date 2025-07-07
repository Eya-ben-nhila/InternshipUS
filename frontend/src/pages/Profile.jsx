import { useState, useEffect } from "react";

export default function Profile() {
  // Load/save profile from localStorage
  const loadProfile = () => {
    return JSON.parse(localStorage.getItem('userProfile')) || {
      name: 'Sarah Johnson',
      title: 'Senior Software Engineer',
      email: 'sarah.johnson@email.com',
      location: 'San Francisco, CA',
      phone: '+1 (555) 123-4567',
      stats: {
        resumesScanned: 24,
        jobsMatched: 156,
        applicationsSubmitted: 12,
        interviewsScheduled: 3
      },
      skills: ['React', 'Node.js', 'Python'],
      values: ['Innovation', 'Teamwork', 'Growth'],
      interests: ['AI', 'Web Development', 'Startups'],
      workExperiences: [
        { role: 'Software Engineer', company: 'TechCorp', years: '2019-2022' },
        { role: 'Frontend Developer', company: 'Webify', years: '2017-2019' }
      ],
      dreamJobs: [
        { id: 1, title: 'Lead AI Engineer', description: 'Work on cutting-edge AI products.' }
      ],
      activeDreamJobId: 1,
      dreamOrgs: ['OpenAI', 'Google', 'Tesla'],
      webSources: ['https://linkedin.com/jobs', 'https://indeed.com', 'https://openai.com/careers'],
      meta: {
        salaryMin: 120000,
        salaryMax: 150000,
        location: 'San Francisco, CA',
        workType: 'Hybrid',
        employerType: 'Private',
        sector: 'Technology'
      },
      resumes: [
        { id: 1, name: 'Software Engineer Resume', lastUpdated: '2024-01-15', score: 87, status: 'Active', keywords: ['React', 'Node.js', 'Python'] },
        { id: 2, name: 'Product Manager Resume', lastUpdated: '2024-01-10', score: 92, status: 'Active', keywords: ['Product', 'Agile', 'Analytics'] },
        { id: 3, name: 'Data Scientist Resume', lastUpdated: '2023-12-20', score: 78, status: 'Draft', keywords: ['Python', 'ML', 'SQL'] }
      ]
    };
  };
  const [userProfile, setUserProfile] = useState(loadProfile());
  useEffect(() => {
    localStorage.setItem('userProfile', JSON.stringify(userProfile));
  }, [userProfile]);

  const [resumes, setResumes] = useState([
    {
      id: 1,
      name: 'Software Engineer Resume',
      lastUpdated: '2024-01-15',
      score: 87,
      status: 'Active'
    },
    {
      id: 2,
      name: 'Product Manager Resume',
      lastUpdated: '2024-01-10',
      score: 92,
      status: 'Active'
    },
    {
      id: 3,
      name: 'Data Scientist Resume',
      lastUpdated: '2023-12-20',
      score: 78,
      status: 'Draft'
    }
  ]);

  const [recentActivity] = useState([
    {
      id: 1,
      action: 'Resume scanned for Senior Developer position',
      company: 'TechCorp Inc.',
      date: '2024-01-15',
      score: 89
    },
    {
      id: 2,
      action: 'Applied to Product Manager role',
      company: 'InnovateTech',
      date: '2024-01-12',
      status: 'Application Submitted'
    },
    {
      id: 3,
      action: 'Resume optimized for Data Scientist position',
      company: 'DataFlow Solutions',
      date: '2024-01-10',
      score: 85
    }
  ]);

  const [newSkill, setNewSkill] = useState('');
  const addSkill = () => {
    if (newSkill.trim()) {
      setUserProfile({ ...userProfile, skills: [...userProfile.skills, newSkill.trim()] });
      setNewSkill('');
    }
  };
  const removeSkill = (skill) => {
    setUserProfile({ ...userProfile, skills: userProfile.skills.filter(s => s !== skill) });
  };

  const handleResumeAction = (action, resumeId) => {
    console.log(`${action} resume ${resumeId}`);
    // In a real app, this would make an API call
  };

  // Dream Job Section State
  const [showDreamJobForm, setShowDreamJobForm] = useState(false);
  const [editingDreamJob, setEditingDreamJob] = useState(null);
  const [dreamJobForm, setDreamJobForm] = useState({ title: '', description: '' });

  // Add/Edit Dream Job
  const handleDreamJobFormChange = (e) => {
    setDreamJobForm({ ...dreamJobForm, [e.target.name]: e.target.value });
  };
  const openAddDreamJob = () => {
    setEditingDreamJob(null);
    setDreamJobForm({ title: '', description: '' });
    setShowDreamJobForm(true);
  };
  const openEditDreamJob = (job) => {
    setEditingDreamJob(job.id);
    setDreamJobForm({ title: job.title, description: job.description });
    setShowDreamJobForm(true);
  };
  const saveDreamJob = () => {
    if (dreamJobForm.title.trim() && dreamJobForm.description.trim()) {
      if (editingDreamJob) {
        setUserProfile({
          ...userProfile,
          dreamJobs: userProfile.dreamJobs.map(j =>
            j.id === editingDreamJob ? { ...j, ...dreamJobForm } : j
          )
        });
      } else {
        const newId = Math.max(0, ...userProfile.dreamJobs.map(j => j.id)) + 1;
        setUserProfile({
          ...userProfile,
          dreamJobs: [...userProfile.dreamJobs, { id: newId, ...dreamJobForm }]
        });
      }
      setShowDreamJobForm(false);
      setEditingDreamJob(null);
      setDreamJobForm({ title: '', description: '' });
    }
  };
  const deleteDreamJob = (id) => {
    setUserProfile({
      ...userProfile,
      dreamJobs: userProfile.dreamJobs.filter(j => j.id !== id),
      activeDreamJobId: userProfile.activeDreamJobId === id ? null : userProfile.activeDreamJobId
    });
  };
  const setActiveDreamJob = (id) => {
    setUserProfile({ ...userProfile, activeDreamJobId: id });
  };

  // Resume Section State
  const [showResumeForm, setShowResumeForm] = useState(false);
  const [editingResume, setEditingResume] = useState(null);
  const [resumeForm, setResumeForm] = useState({ name: '', keywords: '', status: 'Active' });
  const [showScanModal, setShowScanModal] = useState(false);
  const [scanResult, setScanResult] = useState(null);

  // Add/Update Resume
  const openAddResume = () => {
    setEditingResume(null);
    setResumeForm({ name: '', keywords: '', status: 'Active' });
    setShowResumeForm(true);
  };
  const openEditResume = (resume) => {
    setEditingResume(resume.id);
    setResumeForm({ name: resume.name, keywords: resume.keywords.join(', '), status: resume.status });
    setShowResumeForm(true);
  };
  const saveResume = () => {
    const keywordsArr = resumeForm.keywords.split(',').map(k => k.trim()).filter(Boolean);
    if (resumeForm.name.trim() && keywordsArr.length) {
      if (editingResume) {
        setUserProfile({
          ...userProfile,
          resumes: userProfile.resumes.map(r =>
            r.id === editingResume ? { ...r, name: resumeForm.name, keywords: keywordsArr, status: resumeForm.status, lastUpdated: new Date().toISOString().slice(0, 10) } : r
          )
        });
      } else {
        const newId = Math.max(0, ...userProfile.resumes.map(r => r.id)) + 1;
        setUserProfile({
          ...userProfile,
          resumes: [...userProfile.resumes, { id: newId, name: resumeForm.name, keywords: keywordsArr, status: resumeForm.status, lastUpdated: new Date().toISOString().slice(0, 10), score: 0 }]
        });
      }
      setShowResumeForm(false);
      setEditingResume(null);
      setResumeForm({ name: '', keywords: '', status: 'Active' });
    }
  };
  // Scan Resume
  const scanResume = (resume) => {
    // Simulate scan: random score, add a keyword
    const newScore = Math.floor(Math.random() * 21) + 80;
    const newKeywords = [...resume.keywords, 'ScannedSkill' + Math.floor(Math.random() * 100)];
    setUserProfile({
      ...userProfile,
      resumes: userProfile.resumes.map(r =>
        r.id === resume.id ? { ...r, score: newScore, keywords: newKeywords, lastUpdated: new Date().toISOString().slice(0, 10) } : r
      )
    });
    setScanResult({ name: resume.name, score: newScore, keywords: newKeywords });
    setShowScanModal(true);
  };

  return (
    <div className="js-profile">
      <div className="js-profile-container">
        <div className="js-profile-header">
          <h2>Your Profile</h2>
          <p>Manage your personal brand, preferences, and job search data.</p>
        </div>

        <div className="js-profile-content">
          {/* Profile Sidebar */}
          <div className="js-profile-sidebar">
            <div className="js-profile-avatar">
              {userProfile.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div className="js-profile-name">{userProfile.name}</div>
            <div className="js-profile-title">{userProfile.title}</div>
            
            <div className="js-profile-stats">
              <div className="js-stat-item">
                <div className="js-stat-number">{userProfile.stats.resumesScanned}</div>
                <div className="js-stat-label">Resumes Scanned</div>
              </div>
              <div className="js-stat-item">
                <div className="js-stat-number">{userProfile.stats.jobsMatched}</div>
                <div className="js-stat-label">Jobs Matched</div>
              </div>
              <div className="js-stat-item">
                <div className="js-stat-number">{userProfile.stats.applicationsSubmitted}</div>
                <div className="js-stat-label">Applications</div>
              </div>
              <div className="js-stat-item">
                <div className="js-stat-number">{userProfile.stats.interviewsScheduled}</div>
                <div className="js-stat-label">Interviews</div>
              </div>
            </div>

            <div style={{ marginTop: '2rem' }}>
              <h4 style={{ fontSize: '1rem', fontWeight: '600', color: '#1a202c', marginBottom: '1rem' }}>Contact Info</h4>
              <div style={{ fontSize: '0.875rem', color: '#64748b', lineHeight: '1.6' }}>
                <div>📧 {userProfile.email}</div>
                <div>📱 {userProfile.phone}</div>
                <div>📍 {userProfile.location}</div>
              </div>
            </div>
          </div>

          {/* Profile Main Content */}
          <div className="js-profile-main">
            {/* Skills */}
            <div style={{ marginBottom: '2rem' }}>
              <h3 className="js-section-title">Skills</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1rem' }}>
                {userProfile.skills.map(skill => (
                  <span key={skill} className="js-job-tag">
                    {skill} <button onClick={() => removeSkill(skill)} style={{ marginLeft: 4, color: '#dc2626', background: 'none', border: 'none', cursor: 'pointer' }}>×</button>
                  </span>
                ))}
              </div>
              <input value={newSkill} onChange={e => setNewSkill(e.target.value)} placeholder="Add skill" style={{ padding: '0.5rem', borderRadius: 6, border: '1px solid #e2e8f0', marginRight: 8 }} />
              <button className="js-action-button primary" onClick={addSkill}>Add</button>
            </div>

            {/* Resumes Section */}
            <div style={{ marginBottom: '3rem' }}>
              <h3 className="js-section-title">Your Resumes</h3>
              {userProfile.resumes.map(resume => (
                <div key={resume.id} className="js-resume-item">
                  <div className="js-resume-info">
                    <h4>{resume.name}</h4>
                    <p>Last updated: {resume.lastUpdated} • Score: {resume.score}/100 • Status: {resume.status}</p>
                    <div style={{ color: '#64748b', fontSize: '0.85rem', marginTop: 4 }}>Keywords: {resume.keywords.join(', ')}</div>
                  </div>
                  <div className="js-resume-actions">
                    <button 
                      className="js-action-button primary"
                      onClick={() => openEditResume(resume)}
                    >
                      Edit
                    </button>
                    <button 
                      className="js-action-button secondary"
                      onClick={() => scanResume(resume)}
                    >
                      Scan
                    </button>
                    <button 
                      className="js-action-button secondary"
                      onClick={() => alert('Download not implemented in demo')}
                    >
                      Download
                    </button>
                  </div>
                </div>
              ))}
              <button 
                className="js-action-button primary"
                style={{ marginTop: '1rem' }}
                onClick={openAddResume}
              >
                + Add New Resume
              </button>
              {/* Resume Modal/Form */}
              {showResumeForm && (
                <div style={{ background: '#fff', border: '2px solid #2563eb', borderRadius: 12, padding: 24, marginTop: 16, boxShadow: '0 4px 16px #2563eb22' }}>
                  <h4 style={{ color: '#2563eb', marginBottom: 12 }}>{editingResume ? 'Edit Resume' : 'Add Resume'}</h4>
                  <input name="name" value={resumeForm.name} onChange={e => setResumeForm({ ...resumeForm, name: e.target.value })} placeholder="Resume Name" style={{ width: '100%', marginBottom: 12, padding: 8, borderRadius: 6, border: '1px solid #e2e8f0' }} />
                  <input name="keywords" value={resumeForm.keywords} onChange={e => setResumeForm({ ...resumeForm, keywords: e.target.value })} placeholder="Keywords (comma separated)" style={{ width: '100%', marginBottom: 12, padding: 8, borderRadius: 6, border: '1px solid #e2e8f0' }} />
                  <select name="status" value={resumeForm.status} onChange={e => setResumeForm({ ...resumeForm, status: e.target.value })} style={{ width: '100%', marginBottom: 12, padding: 8, borderRadius: 6, border: '1px solid #e2e8f0' }}>
                    <option value="Active">Active</option>
                    <option value="Draft">Draft</option>
                  </select>
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button className="js-action-button primary" onClick={saveResume}>{editingResume ? 'Save' : 'Add'}</button>
                    <button className="js-action-button secondary" onClick={() => { setShowResumeForm(false); setEditingResume(null); }}>Cancel</button>
                  </div>
                </div>
              )}
              {/* Scan Modal */}
              {showScanModal && scanResult && (
                <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: '#0008', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
                  <div style={{ background: '#fff', borderRadius: 12, padding: 32, minWidth: 320, maxWidth: 400, boxShadow: '0 8px 32px #0004' }}>
                    <h3 style={{ color: '#2563eb', marginBottom: 12 }}>Resume Scanned</h3>
                    <div style={{ marginBottom: 12 }}><b>Resume:</b> {scanResult.name}</div>
                    <div style={{ marginBottom: 12 }}><b>New Score:</b> {scanResult.score}/100</div>
                    <div style={{ marginBottom: 12 }}><b>Keywords:</b> {scanResult.keywords.join(', ')}</div>
                    <button className="js-action-button primary" onClick={() => setShowScanModal(false)}>Close</button>
                  </div>
                </div>
              )}
            </div>

            {/* Recent Activity Section */}
            <div style={{ marginBottom: '3rem' }}>
              <h3 className="js-section-title">Recent Activity</h3>
              {recentActivity.map(activity => (
                <div key={activity.id} className="js-resume-item">
                  <div className="js-resume-info">
                    <h4>{activity.action}</h4>
                    <p>{activity.company} • {activity.date}</p>
                  </div>
                  <div className="js-resume-actions">
                    {activity.score && (
                      <span style={{ 
                        background: '#dcfce7', 
                        color: '#166534', 
                        padding: '0.25rem 0.75rem', 
                        borderRadius: '20px', 
                        fontSize: '0.875rem', 
                        fontWeight: '600' 
                      }}>
                        {activity.score}% Match
                      </span>
                    )}
                    {activity.status && (
                      <span style={{ 
                        background: '#dbeafe', 
                        color: '#1e40af', 
                        padding: '0.25rem 0.75rem', 
                        borderRadius: '20px', 
                        fontSize: '0.875rem', 
                        fontWeight: '600' 
                      }}>
                        {activity.status}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Job Preferences Section */}
            <div>
              <h3 className="js-section-title">Job Preferences</h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                <div style={{ 
                  background: '#f8fafc', 
                  padding: '1rem', 
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{ fontWeight: '600', color: '#1a202c', marginBottom: '0.5rem' }}>Desired Role</div>
                  <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Senior Software Engineer</div>
                </div>
                <div style={{ 
                  background: '#f8fafc', 
                  padding: '1rem', 
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{ fontWeight: '600', color: '#1a202c', marginBottom: '0.5rem' }}>Location</div>
                  <div style={{ color: '#64748b', fontSize: '0.875rem' }}>San Francisco, CA</div>
                </div>
                <div style={{ 
                  background: '#f8fafc', 
                  padding: '1rem', 
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{ fontWeight: '600', color: '#1a202c', marginBottom: '0.5rem' }}>Salary Range</div>
                  <div style={{ color: '#64748b', fontSize: '0.875rem' }}>$120,000 - $150,000</div>
                </div>
                <div style={{ 
                  background: '#f8fafc', 
                  padding: '1rem', 
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{ fontWeight: '600', color: '#1a202c', marginBottom: '0.5rem' }}>Work Type</div>
                  <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Hybrid</div>
                </div>
              </div>
              <button 
                className="js-action-button secondary"
                style={{ marginTop: '1rem' }}
                onClick={() => console.log('Edit preferences')}
              >
                Edit Preferences
              </button>
            </div>

            {/* DREAM JOB SECTION */}
            <div style={{ marginBottom: '2.5rem', background: '#f8fafc', borderRadius: 12, padding: '2rem', border: '2px solid #2563eb' }}>
              <h3 className="js-section-title" style={{ color: '#2563eb' }}>Dream Job</h3>
              {userProfile.dreamJobs.length === 0 && <div style={{ color: '#64748b', marginBottom: 12 }}>No dream jobs added yet.</div>}
              {userProfile.dreamJobs.map(job => (
                <div key={job.id} style={{ marginBottom: 16, padding: 12, borderRadius: 8, background: userProfile.activeDreamJobId === job.id ? '#dbeafe' : '#fff', border: userProfile.activeDreamJobId === job.id ? '2px solid #2563eb' : '1px solid #e2e8f0', boxShadow: userProfile.activeDreamJobId === job.id ? '0 2px 8px #2563eb22' : 'none' }}>
                  <div style={{ fontWeight: 600, fontSize: '1.1rem', color: '#1a202c' }}>{job.title}</div>
                  <div style={{ color: '#64748b', margin: '8px 0' }}>{job.description}</div>
                  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                    <button className="js-action-button primary" style={{ background: userProfile.activeDreamJobId === job.id ? '#2563eb' : undefined }} onClick={() => setActiveDreamJob(job.id)}>
                      {userProfile.activeDreamJobId === job.id ? 'Active Dream Job' : 'Set as Active'}
                    </button>
                    <button className="js-action-button secondary" onClick={() => openEditDreamJob(job)}>Edit</button>
                    <button className="js-action-button secondary" style={{ color: '#dc2626', borderColor: '#dc2626' }} onClick={() => deleteDreamJob(job.id)}>Delete</button>
                  </div>
                </div>
              ))}
              <button className="js-action-button primary" style={{ marginTop: 8 }} onClick={openAddDreamJob}>+ Add Dream Job</button>
              {/* Dream Job Modal/Form */}
              {showDreamJobForm && (
                <div style={{ background: '#fff', border: '2px solid #2563eb', borderRadius: 12, padding: 24, marginTop: 16, boxShadow: '0 4px 16px #2563eb22' }}>
                  <h4 style={{ color: '#2563eb', marginBottom: 12 }}>{editingDreamJob ? 'Edit Dream Job' : 'Add Dream Job'}</h4>
                  <input name="title" value={dreamJobForm.title} onChange={handleDreamJobFormChange} placeholder="Dream Job Title" style={{ width: '100%', marginBottom: 12, padding: 8, borderRadius: 6, border: '1px solid #e2e8f0' }} />
                  <textarea name="description" value={dreamJobForm.description} onChange={handleDreamJobFormChange} placeholder="Describe your dream job in detail..." style={{ width: '100%', minHeight: 80, marginBottom: 12, padding: 8, borderRadius: 6, border: '1px solid #e2e8f0' }} />
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button className="js-action-button primary" onClick={saveDreamJob}>{editingDreamJob ? 'Save' : 'Add'}</button>
                    <button className="js-action-button secondary" onClick={() => { setShowDreamJobForm(false); setEditingDreamJob(null); }}>Cancel</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}