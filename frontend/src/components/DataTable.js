import React from 'react';
import { useSelector } from 'react-redux';

function DataTable() {
  const { data, loading, error } = useSelector((state) => state.survey);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800">Error</h3>
          <div className="mt-2 text-sm text-red-700">
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="text-center py-4 text-gray-500">
        No survey data available
      </div>
    );
  }

  // Define column headers
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'age', label: 'Age' },
    { key: 'gender', label: 'Gender' },
    { key: 'education_level', label: 'Education Level' },
    { key: 'state', label: 'State' },
    { key: 'city', label: 'City' },
    { key: 'income', label: 'Income' },
    { key: 'q1_rating', label: 'Q1 Rating' },
    { key: 'q2_rating', label: 'Q2 Rating' },
    { key: 'q3_open', label: 'Q3 Response' },
    { key: 'q4_rating', label: 'Q4 Rating' },
    { key: 'q5_open', label: 'Q5 Response' },
    { key: 'sentiment_label', label: 'Sentiment' }
  ];

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, index) => (
            <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              {columns.map((column) => (
                <td
                  key={`${index}-${column.key}`}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                >
                  {row[column.key] || '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable; 