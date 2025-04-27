import { configureStore } from '@reduxjs/toolkit';
import surveyReducer from './surveySlice';

export const store = configureStore({
  reducer: {
    survey: surveyReducer,
  },
}); 