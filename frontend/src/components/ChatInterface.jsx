import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { sendChatMessage } from '../store/interactionSlice';

const ChatInterface = () => {
  const dispatch = useDispatch();
  const { chatHistory, status } = useSelector((state) => state.interaction);
  const [message, setMessage] = useState('');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleSend = (e) => {
    e.preventDefault();
    if (message.trim() === '') return;
    
    dispatch(sendChatMessage({ message, session_id: "user123" }));
    setMessage('');
  };

  return (
    <>
      <div className="chat-header">
        <span style={{fontSize: '1.25rem'}}>🤖</span>
        <div>
          <h3>AI Assistant</h3>
          <p>Log interaction via chat</p>
        </div>
      </div>

      <div className="chat-history">
        {chatHistory.length === 0 && (
          <div className="chat-message ai">
            <div className="message-content" style={{color: '#64748b', fontStyle: 'italic', fontSize: '0.8rem'}}>
              Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.
            </div>
          </div>
        )}
        {chatHistory.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {status === 'loading' && (
          <div className="chat-message ai loading">
            <div className="message-content">...</div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      
      <form className="chat-input-area" onSubmit={handleSend}>
        <input 
          type="text" 
          value={message} 
          onChange={(e) => setMessage(e.target.value)} 
          placeholder="Describe interaction..."
          disabled={status === 'loading'}
        />
        <button type="submit" disabled={status === 'loading' || !message.trim()}>
          ⏏ Log
        </button>
      </form>
    </>
  );
};

export default ChatInterface;
