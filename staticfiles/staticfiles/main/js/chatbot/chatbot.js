// Import React and necessary components
import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';

// Chatbot component
const TravelChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { 
      text: "Hi there! I'm your GTJGo travel assistant. How can I help you today?", 
      sender: 'bot',
      options: [
        "Transportation options",
        "Safety information",
        "Destination ideas",
        "Travel planning"
      ]
    }
  ]);
  const messagesEndRef = useRef(null);
  const [isBotTyping, setIsBotTyping] = useState(false);

  // Responses based on user selections
  const getResponse = (selection) => {
    switch(selection) {
      case "Transportation options":
        return {
          text: "What kind of transportation information are you looking for?",
          options: [
            "Public transit in a city",
            "Airport transfers",
            "Car rentals"
          ]
        };
        
      // Add the other response options here...
      
      default:
        return {
          text: "I'm here to help with your travel plans! What would you like to know about?",
          options: [
            "Transportation options",
            "Safety information",
            "Destination ideas",
            "Travel planning"
          ]
        };
    }
  };

  const handleOptionClick = (option) => {
    // Add user message
    const userMessage = { text: option, sender: 'user' };
    setMessages([...messages, userMessage]);
    
    // Simulate bot typing
    setIsBotTyping(true);
    
    // Simulate bot response after a short delay
    setTimeout(() => {
      const response = getResponse(option);
      const botResponse = { 
        text: response.text, 
        sender: 'bot',
        options: response.options
      };
      setMessages(prev => [...prev, botResponse]);
      setIsBotTyping(false);
    }, 700);
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat button */}
      {!isOpen && (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-pink-200 hover:bg-pink-300 text-gray-800 rounded-full p-4 shadow-lg flex items-center"
        >
          <MessageCircle size={24} />
          <span className="ml-2 font-medium">Travel Assistant</span>
        </button>
      )}
      
      {/* Chat window */}
      {isOpen && (
        <div className="bg-white rounded-lg shadow-xl flex flex-col w-80 sm:w-96 h-96 border border-gray-200">
          {/* Header */}
          <div className="bg-pink-200 text-gray-800 p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-bold">GTJGo Travel Assistant</h3>
            <button onClick={() => setIsOpen(false)} className="text-gray-700 hover:text-gray-900">
              <X size={20} />
            </button>
          </div>
          
          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto">
            {messages.map((message, index) => (
              <div 
                key={index} 
                className={`mb-3 ${message.sender === 'user' ? 'text-right' : ''}`}
              >
                <div 
                  className={`inline-block p-3 rounded-lg ${
                    message.sender === 'user' ? 'bg-pink-100 text-gray-800' : 'bg-gray-100 text-gray-800'}`}
                >
                  {message.text}
                </div>
                
                {/* Options buttons for bot messages */}
                {message.sender === 'bot' && message.options && (
                  <div className="mt-2 flex flex-col gap-2">
                    {message.options.map((option, optIndex) => (
                      <button
                        key={optIndex}
                        onClick={() => handleOptionClick(option)}
                        className="text-left text-sm bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 py-2 px-3 rounded-lg transition-colors"
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {isBotTyping && (
              <div className="mb-3">
                <div className="inline-block bg-gray-100 p-3 rounded-lg text-gray-800">
                  <div className="typing-animation">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      <style jsx>{`
        .typing-animation {
          display: flex;
          align-items: center;
          column-gap: 6px;
          padding: 0 3px;
        }
        .typing-animation span {
          background-color: #9CA3AF;
          border-radius: 50%;
          height: 6px;
          width: 6px;
          display: block;
          opacity: 0.4;
        }
        .typing-animation span:nth-child(1) {
          animation: pulse 1s infinite ease-in-out;
        }
        .typing-animation span:nth-child(2) {
          animation: pulse 1s infinite ease-in-out .2s;
        }
        .typing-animation span:nth-child(3) {
          animation: pulse 1s infinite ease-in-out .4s;
        }
        @keyframes pulse {
          0%, 100% {
            opacity: 0.4;
            transform: scale(1);
          }
          50% {
            opacity: 1;
            transform: scale(1.2);
          }
        }
      `}</style>
    </div>
  );
};

export default TravelChatbot;