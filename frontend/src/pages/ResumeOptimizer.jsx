import { useState } from 'react';

export default function ResumeOptimizer() {
  const [fileUploaded, setFileUploaded] = useState(false);
  
  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Hero Section */}
      <section className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Optimize your resume to get more interviews</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          CareerTool helps you optimize your resume for any job, highlighting the key experience and skills recruiters need to see.
        </p>
      </section>

      {/* Upload Card */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8 border border-gray-200">
        <h2 className="text-2xl font-semibold text-center mb-6">Scan Your Resume For Free</h2>
        
        <div className="flex flex-col items-center justify-center border-2 border-dashed border-blue-200 rounded-lg p-12 bg-blue-50 mb-8">
          {!fileUploaded ? (
            <>
              <UploadIcon className="w-12 h-12 text-blue-500 mb-4" />
              <p className="text-gray-600 mb-4">Drag & drop your resume file here</p>
              <p className="text-gray-500 text-sm mb-4">or</p>
              <label className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md cursor-pointer transition-colors">
                Browse Files
                <input type="file" className="hidden" onChange={() => setFileUploaded(true)} />
              </label>
              <p className="text-gray-400 text-xs mt-2">Supports PDF, DOCX (max 5MB)</p>
            </>
          ) : (
            <>
              <CheckCircleIcon className="w-12 h-12 text-green-500 mb-4" />
              <p className="text-gray-600 mb-2">Resume_2024.pdf</p>
              <p className="text-green-600 font-medium mb-4">Successfully uploaded!</p>
              <button className="text-blue-600 hover:text-blue-800 font-medium">
                Change file
              </button>
            </>
          )}
        </div>
      </div>

      {/* Analysis Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-6">Searchability</h2>
        <p className="text-gray-600 mb-6">
          We analyze your resume to understand your work history and relevance to the job's requirements and company culture.
        </p>
        
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tips</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <TableRow 
                category="Contact Information" 
                status="Complete" 
                tip="Ensure your email and phone are visible"
              />
              <TableRow 
                category="Summary" 
                status="Needs Work" 
                tip="Add a 3-4 sentence professional summary"
              />
              <TableRow 
                category="Section Headings" 
                status="Complete" 
                tip="Standard headings improve ATS parsing"
              />
              <TableRow 
                category="Job Title Match" 
                status="Needs Work" 
                tip="Include target job title in your resume"
              />
              <TableRow 
                category="Date Formatting" 
                status="Complete" 
                tip="Consistent date format detected"
              />
            </tbody>
          </table>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center bg-blue-50 rounded-lg p-8">
        <h3 className="text-xl font-semibold mb-4">Ready to optimize your resume?</h3>
        <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-8 rounded-md transition-colors">
          Get Full Analysis Report
        </button>
      </section>
    </div>
  );
}

// Component for table rows
function TableRow({ category, status, tip }) {
  const statusColor = status === "Complete" ? "text-green-600" : "text-yellow-600";
  
  return (
    <tr>
      <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{category}</td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className={`${statusColor} font-medium`}>{status}</span>
      </td>
      <td className="px-6 py-4 text-gray-600">{tip}</td>
    </tr>
  );
}

// Mock icons (replace with actual icons from your library)
function UploadIcon(props) {
  return (
    <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>
  );
}

function CheckCircleIcon(props) {
  return (
    <svg {...props} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}