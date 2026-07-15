import React from 'react';
import StructuredForm from './StructuredForm';
import ChatInterface from './ChatInterface';

const LogInteractionScreen = () => {
  return (
    <div className="log-interaction-container">
      <div className="left-column">
        <StructuredForm />
      </div>
      <div className="right-column">
        <ChatInterface />
      </div>
    </div>
  );
};

export default LogInteractionScreen;
