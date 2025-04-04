import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';

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
        
      case "Public transit in a city":
        return {
          text: "Our Transport section can help you find subway stations, bus stops, and train stations in your destination city. Which city are you visiting?",
          options: [
            "Paris", 
            "London", 
            "Tokyo", 
            "New York",
            "Ask about another city"
          ]
        };
        
      case "Airport transfers":
        return {
          text: "In the Rentals section, you can book transportation from airports to your hotel. Just enter your airport, date, and hotel to see available options.",
          options: [
            "How does it work?",
            "View popular airports",
            "Back to main menu"
          ]
        };
        
      case "Car rentals":
        return {
          text: "While we don't offer direct car rental bookings, our Rentals section focuses on airport transfers and local transportation options.",
          options: [
            "Airport transfers",
            "Public transit options",
            "Back to main menu"
          ]
        };

      case "Safety information":
        return {
          text: "What kind of safety information are you looking for?",
          options: [
            "General safety ratings",
            "Women/Solo traveler safety",
            "Common scams and crimes",
            "Emergency contacts"
          ]
        };
        
      case "General safety ratings":
        return {
          text: "Our Safety section provides comprehensive safety ratings for destinations worldwide. We rate overall safety, crime rates, and provide specific advice for travelers.",
          options: [
            "How are ratings calculated?",
            "Check a specific destination",
            "Back to safety menu"
          ]
        };
        
      case "Women/Solo traveler safety":
        return {
          text: "We offer dedicated safety information for women and solo travelers, including safe neighborhoods, transportation tips, and cultural considerations.",
          options: [
            "Safest destinations for women",
            "Solo travel tips",
            "Back to safety menu"
          ]
        };
        
      case "Common scams and crimes":
        return {
          text: "Our safety guides include information about common tourist scams and crimes in different destinations, along with tips to stay safe.",
          options: [
            "Popular scams to watch for",
            "Check specific destination",
            "Back to safety menu"
          ]
        };
        
      case "Emergency contacts":
        return {
          text: "Our safety information includes emergency phone numbers and helpful contacts for different countries. You can find police, ambulance, and embassy contacts.",
          options: [
            "Back to safety menu",
            "Back to main menu"
          ]
        };

      case "Destination ideas":
        return {
          text: "What kind of destination are you interested in?",
          options: [
            "Beach destinations",
            "City breaks",
            "Adventure travel",
            "Family-friendly places",
            "Cultural experiences"
          ]
        };
        
      case "Beach destinations":
        return {
          text: "Some popular beach destinations include Bali, Cancun, the Greek Islands, and Thailand. Each offers different experiences from relaxation to water sports.",
          options: [
            "Safety in beach destinations",
            "Transportation tips",
            "More destination types",
            "Back to main menu"
          ]
        };
        
      case "City breaks":
        return {
          text: "Popular city destinations include Paris, London, Tokyo, New York, and Barcelona. Each offers unique cultural experiences, cuisine, and attractions.",
          options: [
            "City safety information",
            "Public transportation",
            "More destination types",
            "Back to main menu"
          ]
        };

      case "Travel planning":
        return {
          text: "How can I help with your travel planning?",
          options: [
            "Best time to visit destinations",
            "Saving favorite places",
            "Packing tips",
            "Travel preparation checklist"
          ]
        };
        
      case "Best time to visit destinations":
        return {
          text: "The best time to visit depends on your destination. Would you like general seasonal advice or information about a specific region?",
          options: [
            "Europe seasons",
            "Asia seasons",
            "Americas seasons",
            "Back to planning menu"
          ]
        };
        
      case "Saving favorite places":
        return {
          text: "You can save your favorite destinations to your account by clicking the 'Add to Favorites' button. You'll need to be logged in to use this feature.",
          options: [
            "How to create an account",
            "Managing favorites",
            "Back to planning menu"
          ]
        };
        
      // Default responses for location-specific questions
      case "Paris":
      case "London":
      case "Tokyo":
      case "New York":
        return {
          text: `You can find detailed transportation information for ${selection} in our Transport section. There you'll see subway/metro stations, bus stops, and train connections.`,
          options: [
            "Safety information",
            "Other cities",
            "Back to main menu"
          ]
        };
        
      // Return to menu options
      case "Back to safety menu":
        return getResponse("Safety information");
        
      case "Back to planning menu":
        return getResponse("Travel planning");
        
      case "Back to main menu":
        return {
          text: "What else would you like to know about?",
          options: [
            "Transportation options",
            "Safety information",
            "Destination ideas",
            "Travel planning"
          ]
        };
        
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

      {/* CSS for typing animation */}
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