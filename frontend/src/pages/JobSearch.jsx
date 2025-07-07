import { useState } from "react";

export default function JobSearch() {
  const [salaryRange, setSalaryRange] = useState([50, 100]); // $50k-$100k

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Job Search</h1>
      
      <div className="mb-6">
        <label className="block mb-2">Salary Range (${salaryRange[0]}k - ${salaryRange[1]}k)</label>
        <input
          type="range"
          min="30"
          max="200"
          value={salaryRange[0]}
          onChange={(e) => setSalaryRange([e.target.value, salaryRange[1]])}
          className="w-full"
        />
        {/* Add a second slider for max salary */}
      </div>

      {/* Add more filters (location, remote, etc.) */}
    </div>
  );
}