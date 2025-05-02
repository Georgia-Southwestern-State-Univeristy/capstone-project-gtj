import React from 'react';
import ReactDOM from 'react-dom';
import TravelChatbot from './chatbot';

document.addEventListener('DOMContentLoaded', function() {
  // Create a div for the chatbot if it doesn't exist
  let chatbotRoot = document.getElementById('chatbot-root');
  if (!chatbotRoot) {
    chatbotRoot = document.createElement('div');
    chatbotRoot.id = 'chatbot-root';
    document.body.appendChild(chatbotRoot);
  }
  
  // Render the chatbot component
  ReactDOM.render(React.createElement(TravelChatbot), chatbotRoot);
  
  console.log('Chatbot initialized');
});