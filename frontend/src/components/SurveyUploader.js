import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setSurveyData, setLoading, setError } from '../store/surveySlice';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function SurveyUploader() {
  const [file, setFile] = useState(null);
  const dispatch = useDispatch();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    dispatch(setLoading(true));
    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      dispatch(setSurveyData(response.data.surveys));
    } catch (error) {
      dispatch(setError(error.response?.data?.detail || 'Failed to upload file'));
    }
  };

  return (
    <div>
      <h2 className="text-lg font-medium text-gray-900 mb-4">Upload Survey Data</h2>
      <form onSubmit={handleUpload} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            CSV File
          </label>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="mt-1 block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          />
        </div>
        <button
          type="submit"
          disabled={!file}
          className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white 
            ${file ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'}`}
        >
          Upload
        </button>
      </form>
    </div>
  );
}

export default SurveyUploader; 