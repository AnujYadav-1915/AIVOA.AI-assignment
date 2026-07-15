import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchHCPs = createAsyncThunk('interaction/fetchHCPs', async () => {
  const response = await axios.get(`${API_URL}/hcps`);
  return response.data;
});

export const submitInteractionForm = createAsyncThunk('interaction/submitForm', async (formData) => {
  const response = await axios.post(`${API_URL}/interactions`, formData);
  return response.data;
});

export const sendChatMessage = createAsyncThunk('interaction/sendChat', async (messageData) => {
  const response = await axios.post(`${API_URL}/chat`, messageData);
  return { userMessage: messageData.message, aiResponse: response.data.response };
});

const initialState = {
  hcps: [],
  chatHistory: [],
  status: 'idle',
  error: null,
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchHCPs.fulfilled, (state, action) => {
        state.hcps = action.payload;
      })
      .addCase(submitInteractionForm.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(submitInteractionForm.fulfilled, (state) => {
        state.status = 'succeeded';
      })
      .addCase(submitInteractionForm.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(sendChatMessage.pending, (state, action) => {
        state.status = 'loading';
        // Optimistically add user message (in a real app, manage this separately for better UI)
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.chatHistory.push({ role: 'user', content: action.payload.userMessage });
        state.chatHistory.push({ role: 'ai', content: action.payload.aiResponse });
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export default interactionSlice.reducer;
