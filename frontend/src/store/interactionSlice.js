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
  return { 
    userMessage: messageData.message, 
    aiResponse: response.data.response,
    formData: response.data.form_data
  };
});

const defaultFormState = {
  hcp_id: '',
  interaction_type: 'Meeting',
  date: '2025-04-19',
  time: '19:36',
  attendees: '',
  topics: '',
  materials_shared: '',
  samples_distributed: '',
  sentiment: 'Neutral',
  outcomes: '',
  action_items: ''
};

const initialState = {
  hcps: [],
  chatHistory: [],
  formData: { ...defaultFormState },
  status: 'idle',
  error: null,
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateFormData: (state, action) => {
      state.formData = { ...state.formData, ...action.payload };
    },
    resetFormData: (state) => {
      state.formData = { ...defaultFormState };
    }
  },
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
        // Immediately add the user's message to the chat history so it doesn't disappear!
        state.chatHistory.push({ role: 'user', content: action.meta.arg.message });
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.status = 'succeeded';
        // Add the AI's response
        state.chatHistory.push({ role: 'ai', content: action.payload.aiResponse });
        
        // Auto-populate form data from AI extraction
        if (action.payload.formData) {
          const extracted = action.payload.formData;
          Object.keys(extracted).forEach(key => {
            if (extracted[key] !== null && extracted[key] !== "" && key in state.formData) {
              state.formData[key] = extracted[key];
            }
          });
        }
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
        state.chatHistory.push({ role: 'ai', content: "Error: The server failed to respond. Please refresh the page and try again." });
      });
  },
});

export const { updateFormData, resetFormData } = interactionSlice.actions;
export default interactionSlice.reducer;
