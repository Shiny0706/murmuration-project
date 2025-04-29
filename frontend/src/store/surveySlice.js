import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  data: [],
  loading: false,
  error: null,
};

const surveySlice = createSlice({
  name: 'survey',
  initialState,
  reducers: {
    setSurveyData: (state, action) => {
      state.data = action.payload;
      state.loading = false;
      state.error = null;
    },
    setSentimentCounts: (state, action) => {
      state.sentimentCounts = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.loading = false;
    },
  },
});

export const { setSurveyData, setSentimentCounts, setLoading, setError } = surveySlice.actions;
export default surveySlice.reducer; 