import React, { useState } from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import SurveyUploader from './components/SurveyUploader';
import QuestionVisualizer from './components/QuestionVisualizer';
import DataTable from './components/DataTable';

function App() {
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [question, setQuestion] = useState('q1_rating');

  const questionOptions = [
    { id: 'q1_rating', label: 'Q1: Rating' },
    { id: 'q2_rating', label: 'Q2: Rating' },
    { id: 'q4_rating', label: 'Q4: Rating' },
  ];

  return (
    <Provider store={store}>
      <div className="min-h-screen bg-gray-100">
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <header className="bg-white shadow">
            <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
              <h1 className="text-3xl font-bold text-gray-900">Survey Data Explorer</h1>
              <p className="mt-1 text-sm text-gray-500">
                Analyzing responses from the AI sentiment survey
              </p>
            </div>
          </header>
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <div className="bg-white shadow rounded-lg p-6 mb-8">
                <SurveyUploader onUploadSuccess={() => setUploadSuccess(true)} />
              </div>
              
              <div className="bg-white shadow rounded-lg p-6 mb-8">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Survey Data Table</h2>
                <DataTable data={store.getState().survey.data} />
              </div>
                
              <div className="bg-white shadow rounded-lg p-6 mb-8">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Select Question to Visualize</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  {questionOptions.map((option) => (
                    <div 
                      key={option.id}
                      onClick = {() => setQuestion(option.id)}
                      className={`
                        p-4 border rounded-md cursor-pointer transition
                        ${question === option.id 
                          ? 'border-blue-500 bg-blue-50' 
                          : 'border-gray-200 hover:bg-gray-50'}
                      `}
                    >
                      <span className="block text-sm font-medium">
                        {option.label}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="bg-white shadow rounded-lg p-6">
                <QuestionVisualizer 
                  questionId={question}
                  hasData={uploadSuccess}
                />
              </div>
            </div>
          </main>
        </div>
      </div>
    </Provider>
  );
}

export default App; 