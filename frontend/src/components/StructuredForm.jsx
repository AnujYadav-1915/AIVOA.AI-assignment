import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchHCPs, submitInteractionForm, updateFormData, resetFormData } from '../store/interactionSlice';

const StructuredForm = () => {
  const dispatch = useDispatch();
  const { hcps, status, formData } = useSelector((state) => state.interaction);

  useEffect(() => {
    if (hcps.length === 0) {
      dispatch(fetchHCPs());
    }
  }, [dispatch, hcps.length]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateFormData({ [name]: value }));
  };

  const handleRadioChange = (val) => {
    dispatch(updateFormData({ sentiment: val }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.hcp_id) {
      alert("Please select an HCP");
      return;
    }
    dispatch(submitInteractionForm(formData)).then(() => {
      alert("Interaction logged successfully!");
      dispatch(resetFormData());
    });
  };

  return (
    <div className="content-area">
      <h2 className="form-header">Log HCP Interaction</h2>
      <form onSubmit={handleSubmit}>
        
        <div className="row">
          <div className="col form-group">
            <label>HCP Name:</label>
            <select name="hcp_id" value={formData.hcp_id || ''} onChange={handleChange} required>
              <option value="">Search or select HCP...</option>
              {hcps.map(hcp => (
                <option key={hcp.id} value={hcp.id}>
                  {hcp.name} - {hcp.specialty}
                </option>
              ))}
            </select>
          </div>
          <div className="col form-group">
            <label>Interaction Type</label>
            <select name="interaction_type" value={formData.interaction_type || 'Meeting'} onChange={handleChange}>
              <option value="Meeting">Meeting</option>
              <option value="Email">Email</option>
              <option value="Phone">Phone</option>
            </select>
          </div>
        </div>

        <div className="row">
          <div className="col form-group">
            <label>Date</label>
            <input type="date" name="date" value={formData.date || ''} onChange={handleChange} />
          </div>
          <div className="col form-group">
            <label>Time</label>
            <input type="time" name="time" value={formData.time || ''} onChange={handleChange} />
          </div>
        </div>

        <div className="form-group">
          <label>Attendees</label>
          <input type="text" name="attendees" value={formData.attendees || ''} onChange={handleChange} placeholder="Enter names or search..." />
        </div>

        <div className="form-group">
          <label>Topics Discussed</label>
          <textarea name="topics" value={formData.topics || ''} onChange={handleChange} rows="3" placeholder="Enter key discussion points..."></textarea>
          <button type="button" className="btn-summarize">
            🎤 Summarize from Voice Note (Requires Consent)
          </button>
        </div>

        <div className="section-label">Materials Shared / Samples Distributed</div>
        
        <div className="item-list">
          <div>
            <div style={{fontWeight: 500, fontSize: '0.875rem', marginBottom: '4px'}}>Materials Shared</div>
            <span>{formData.materials_shared || 'No materials added.'}</span>
          </div>
          <button type="button" className="btn-outline">🔍 Search/Add</button>
        </div>

        <div className="item-list">
          <div>
            <div style={{fontWeight: 500, fontSize: '0.875rem', marginBottom: '4px'}}>Samples Distributed</div>
            <span>{formData.samples_distributed || 'No samples added.'}</span>
          </div>
          <button type="button" className="btn-outline">📦 Add Sample</button>
        </div>

        <div className="form-group" style={{marginTop: '1.5rem'}}>
          <label>Observed/Inferred HCP Sentiment</label>
          <div className="radio-group">
            <label className="radio-label">
              <input type="radio" checked={formData.sentiment === 'Positive'} onChange={() => handleRadioChange('Positive')} />
              <span>😊 Positive</span>
            </label>
            <label className="radio-label">
              <input type="radio" checked={formData.sentiment === 'Neutral'} onChange={() => handleRadioChange('Neutral')} />
              <span>😐 Neutral</span>
            </label>
            <label className="radio-label">
              <input type="radio" checked={formData.sentiment === 'Negative'} onChange={() => handleRadioChange('Negative')} />
              <span>😞 Negative</span>
            </label>
          </div>
        </div>

        <div className="form-group">
          <label>Outcomes</label>
          <textarea name="outcomes" value={formData.outcomes || ''} onChange={handleChange} rows="2" placeholder="Key outcomes or agreements..."></textarea>
        </div>

        <div className="form-group">
          <label>Follow-up Actions</label>
          <textarea name="action_items" value={formData.action_items || ''} onChange={handleChange} rows="2" placeholder="Enter next steps or tasks..."></textarea>
        </div>

        <div className="ai-suggestions">
          <h4>AI Suggested Follow-ups:</h4>
          <ul>
            <li><a href="#">+ Schedule follow-up meeting in 2 weeks</a></li>
            <li><a href="#">+ Send OncoBoost Phase III PDF</a></li>
            <li><a href="#">+ Add Dr. Sharma to advisory board invite list</a></li>
          </ul>
        </div>
        
        <div style={{textAlign: 'right', marginTop: '1rem'}}>
           <button type="submit" disabled={status === 'loading'} className="btn-outline" style={{display: 'inline-block', background: '#3b82f6', color: 'white', borderColor: '#3b82f6', padding: '0.5rem 2rem', fontWeight: 600}}>
              Save
           </button>
        </div>
      </form>
    </div>
  );
};

export default StructuredForm;
