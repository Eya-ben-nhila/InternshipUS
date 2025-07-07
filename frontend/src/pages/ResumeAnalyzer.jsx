import { useState } from 'react';

export default function ResumeAnalyzer() {
  const [keywords, setKeywords] = useState(["React", "Team Leadership", "Python"]); // Mock data

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Resume Analysis</h1>
      <input 
        type="file" 
        className="mb-4 border p-2 rounded w-full max-w-md" 
        accept=".pdf,.docx"
      />
      
      <div>
        <h2 className="text-xl font-semibold mb-2">Top Keywords:</h2>
        <div className="flex flex-wrap gap-2">
          {keywords.map((keyword) => (
            <span key={keyword} className="bg-green-100 px-3 py-1 rounded-full">
              {keyword}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}