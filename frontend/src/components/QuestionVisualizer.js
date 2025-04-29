import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

const API_URL = 'http://localhost:8000';

function QuestionVisualizer({ questionId }) {
  const [data, setData] = useState(null);
  const [groupBy, setGroupBy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { data: surveyData } = useSelector((state) => state.survey);
  
  const groupOptions = [
    { value: null, label: 'Overall' },
    { value: 'gender', label: 'By Gender' },
    { value: 'state', label: 'By State' },
    { value: 'city', label: 'By City' },
    { value: 'education_level', label: 'By Education Level' },
    { value: 'sentiment_label', label: 'By Sentiment' },
    { value: 'age', label: 'By Age' }
  ];

  const fetchData = async () => {
    if (!surveyData || surveyData.length === 0) return;
    
    setLoading(true);
    setError('');
    try {
      const url = `${API_URL}/questions/${questionId}${groupBy ? `?group_by=${groupBy}` : ''}`;
      const response = await axios.get(url);
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch data');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (surveyData && surveyData.length > 0) {
      fetchData();
    }
  }, [questionId, groupBy, surveyData]);

  const isRatingQuestion = ['q1_rating', 'q2_rating', 'q4_rating'].includes(questionId);
  
  const getChartData = () => {
    if (!data) return null;

    // For rating questions (showing distribution)
    if (isRatingQuestion) {
      if (!groupBy) {
        // Overall ratings
        if (!data || !data[0] || !data[0].distribution) {
          return null;
        }
        
        const chartData = {
          labels: Object.keys(data[0].distribution),
          datasets: [
            {
              label: 'Number of Responses',
              data: Object.values(data[0].distribution),
              backgroundColor: [
                'rgba(54, 162, 235, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(153, 102, 255, 0.5)',
              ],
              borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(153, 102, 255, 1)',
              ],
              borderWidth: 1,
            },
          ],
        };
        return chartData;
      } else {
        // Grouped ratings
        if (!data || !Array.isArray(data)) {
          return null;
        }
        console.log("Grouped Data:", data);
        const labels = data.map(item => item.group);
        const chartData = {
          labels,
          datasets: [
            {
              label: 'Average Rating',
              data: data.map(item => item.average),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
            },
          ],
        };
        return chartData;
      }
    }
    
    // For open-ended questions
    else {
      if (!groupBy) {
        // Overall responses (top 5 most common)
        console.log("Data", data);
        if (!data.responses || !data.responses[0] || !data.responses[0].responses) {
          return null;
        }
        const sortedResponses = [...data.responses[0].responses].sort((a, b) => b.count - a.count).slice(0, 5);
        
        const chartData = {
          labels: sortedResponses.map(item => item.response.substring(0, 30) + (item.response.length > 30 ? '...' : '')),
          datasets: [
            {
              label: 'Number of Responses',
              data: sortedResponses.map(item => item.count),
              backgroundColor: [
                'rgba(54, 162, 235, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(153, 102, 255, 0.5)',
              ],
              borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(153, 102, 255, 1)',
              ],
              borderWidth: 1,
            },
          ],
        };
        return chartData;
      } else {
        // Cannot effectively visualize grouped open-ended responses with a chart
        return null;
      }
    }
  };

  const { sentimentCounts } = useSelector((state) => state.survey);
  console.log("Sentiment Counts:", sentimentCounts);
  const getSentimentData = () => {
    if (!sentimentCounts) return null;

    const sentimentData = {
      labels: ['Positive', 'Negative', 'Neutral'],
      datasets: [
        {
          label: 'Number of sentiment counts',
          data: Object.values(sentimentCounts),
          backgroundColor: [
            'rgba(54, 162, 235, 0.5)',
            'rgba(255, 159, 64, 0.5)',
            'rgba(255, 206, 86, 0.5)',
          ],
          borderColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(255, 206, 86, 1)',
          ],
          borderWidth: 1,
        },
      ],
    };
    console.log("Sentiment Data:", sentimentData);
    return sentimentData;
  };

  const chartData = getChartData();
  const sentimentData = getSentimentData();

  return (
    <div className="flex">
      <div className="w-1/2 p-4">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          {questionId === 'q1_rating' && 'Q1: Rating of AI'}
          {questionId === 'q2_rating' && 'Q2: Rating of AI'}
          {questionId === 'q4_rating' && 'Q4: Rating of AI'}
        </h2>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Group By
          </label>
          <select
            value={groupBy || ''}
            onChange={(e) => setGroupBy(e.target.value || null)}
            className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 
                    focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          >
            {groupOptions.map((option) => (
              <option key={option.value || 'overall'} value={option.value || ''}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        )}

        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        )}

        {!loading && !error && chartData && (
          <div className="bg-white p-4 rounded-lg shadow">
            {isRatingQuestion && !groupBy ? (
              <Pie
                data={chartData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top',
                    },
                    title: {
                      display: true,
                      text: 'Rating Distribution'
                    }
                  }
                }}
              />
            ) : (
              <Bar
                data={chartData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top',
                    },
                    title: {
                      display: true,
                      text: groupBy ? 'Average Rating by Group' : 'Top 5 Most Common Responses'
                    }
                  },
                  scales: {
                    y: {
                      beginAtZero: true
                    }
                  }
                }}
              />
            )}
          </div>
        )}

        {!loading && !error && !chartData && (
          <div className="text-center text-gray-500 py-4">
            No chart data available for this view
          </div>
        )}
      </div>
      
      <div className="w-1/2 p-4">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          Sentiment Analysis
        </h2>
        <div className="mb-6">
          <div className="bg-white p-4 rounded-lg shadow mt-6">
            {sentimentData && (
              <Pie data={sentimentData} />
            )}
          </div>
        </div>
      </div>
    </div>

    
  );
}

export default QuestionVisualizer; 