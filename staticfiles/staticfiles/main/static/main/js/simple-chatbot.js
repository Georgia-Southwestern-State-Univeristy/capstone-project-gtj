// Simple chatbot implementation
document.addEventListener('DOMContentLoaded', function() {
    console.log('Simple chatbot script loaded');
    
    // Create chat elements
    const chatButton = document.createElement('button');
    const chatWindow = document.createElement('div');
    let isOpen = false;
    let messages = [
      {
        text: "Hi there! I'm your GTJGo travel assistant. How can I help you today?",
        sender: 'bot',
        options: [
          "Transportation",
          "Safety information",
          "Itinerary Generator",
          
        ]
      }
    ];
    
    // Style chat button
    chatButton.innerHTML = '<span style="margin-right: 8px;">💬</span> Travel Assistant';
    chatButton.style.position = 'fixed';
    chatButton.style.bottom = '20px';
    chatButton.style.right = '20px';
    chatButton.style.backgroundColor = '#f9b5ac';
    chatButton.style.color = '#333';
    chatButton.style.padding = '12px 16px';
    chatButton.style.borderRadius = '50px';
    chatButton.style.border = 'none';
    chatButton.style.cursor = 'pointer';
    chatButton.style.zIndex = '9999';
    chatButton.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
    chatButton.style.fontWeight = 'bold';
    chatButton.style.display = 'flex';
    chatButton.style.alignItems = 'center';
    
    // Add button to page
    document.body.appendChild(chatButton);
    
    // Prepare chat window (hidden initially)
    chatWindow.style.position = 'fixed';
    chatWindow.style.bottom = '80px';
    chatWindow.style.right = '20px';
    chatWindow.style.width = '320px';
    chatWindow.style.height = '400px';
    chatWindow.style.backgroundColor = 'white';
    chatWindow.style.borderRadius = '10px';
    chatWindow.style.boxShadow = '0 0 10px rgba(0,0,0,0.2)';
    chatWindow.style.display = 'none';
    chatWindow.style.flexDirection = 'column';
    chatWindow.style.zIndex = '9999';
    chatWindow.style.overflow = 'hidden';
    chatWindow.style.border = '1px solid #ddd';
    
    // Create chat header
    const chatHeader = document.createElement('div');
    chatHeader.style.backgroundColor = '#f9b5ac';
    chatHeader.style.padding = '12px';
    chatHeader.style.color = '#333';
    chatHeader.style.fontWeight = 'bold';
    chatHeader.style.borderRadius = '10px 10px 0 0';
    chatHeader.style.display = 'flex';
    chatHeader.style.justifyContent = 'space-between';
    chatHeader.style.alignItems = 'center';
    
    const headerTitle = document.createElement('div');
    headerTitle.innerText = 'GTJGo Travel Assistant';
    
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '✕';
    closeButton.style.background = 'none';
    closeButton.style.border = 'none';
    closeButton.style.color = '#333';
    closeButton.style.fontSize = '16px';
    closeButton.style.cursor = 'pointer';
    
    chatHeader.appendChild(headerTitle);
    chatHeader.appendChild(closeButton);
    chatWindow.appendChild(chatHeader);
    
    // Create messages container
    const messagesContainer = document.createElement('div');
    messagesContainer.style.flex = '1';
    messagesContainer.style.overflowY = 'auto';
    messagesContainer.style.padding = '12px';
    chatWindow.appendChild(messagesContainer);
    
    // Add chat window to page
    document.body.appendChild(chatWindow);
    
    // Toggle chat window
    chatButton.addEventListener('click', function() {
      isOpen = true;
      chatWindow.style.display = 'flex';
      chatButton.style.display = 'none';
      renderMessages();
    });
    
    closeButton.addEventListener('click', function() {
      isOpen = false;
      chatWindow.style.display = 'none';
      chatButton.style.display = 'flex';
    });
    
    // Response handler
    function getResponse(selection) {
      switch(selection) {
        case "Transportation":
          return {
            text: "What kind of transportation information are you looking for?",
            options: [
              "Public transit in a city",
              "back to main menu",

            ]
          };
          
        case "Public transit in a city":
          return {
            text: "Our Transport section can help you find subway stations, bus stops, and train stations in your destination city. Which city are you visiting?",
            options: [
              "Back to main menu",
            ]
          };
          
        
          
        case "Safety information":
          return {
            text: "What kind of safety information are you looking for?",
            options: [
              "General safety ratings",
              "Back to main menu"
            ]
          };
          case "General safety ratings":
          return {
            text: "Our Safety section provides safety ratings for various countries. Ratings are based on crime rates, health risks, and other factors.",
            options: [
              "Back to main menu",
            ]
          };
          
        case "Itinerary Generator":
          return {
            text: "What questions do you have about itinerary generation?",
            options: [
              "How is the itinerary generated?",
              "Saving favorite lists",
              "Packing tips",
              "Travel preparation checklist",
              "Back to main menu"
            ]
          };
        case "How is the itinerary generated?":
          return {
            text: "The itinerary is generated based on location,weather and interests. You can customize it by entering destinations and travel dates.",
            options: [
              "Saving favorite lists",
              "Packing tips",
              "Travel preparation checklist",
              "Back to main menu"
            ]
          };
        
        case "Back to main menu":
          return {
            text: "What else would you like to know about?",
            options: [
              "Transportation options",
              "Safety information",
              "Itinerary Generator",
    
            ]
          };
          
        default:
          return {
            text: "I'm here to help with your travel plans! What would you like to know about?",
            options: [
              "Transportation",
              "Safety information",
              "Itinerary Generator",
              "Back to main menu"
      
            ]
          };
      }
    }
    
    // Handle option clicks
    function handleOptionClick(option) {
      // Add user message
      messages.push({
        text: option,
        sender: 'user'
      });
      
      // Render typing indicator
      renderMessages(true);
      
      // Add bot response after delay
      setTimeout(function() {
        const response = getResponse(option);
        messages.push({
          text: response.text,
          sender: 'bot',
          options: response.options
        });
        renderMessages();
      }, 700);
    }
    
    // Render messages
    function renderMessages(isTyping = false) {
      messagesContainer.innerHTML = '';
      
      // Add all messages
      messages.forEach(function(message) {
        const messageDiv = document.createElement('div');
        messageDiv.style.marginBottom = '12px';
        messageDiv.style.textAlign = message.sender === 'user' ? 'right' : 'left';
        
        const bubble = document.createElement('div');
        bubble.style.display = 'inline-block';
        bubble.style.padding = '8px 12px';
        bubble.style.borderRadius = '10px';
        bubble.style.maxWidth = '80%';
        bubble.style.wordWrap = 'break-word';
        
        if (message.sender === 'user') {
          bubble.style.backgroundColor = '#f9b5ac';
          bubble.style.color = '#333';
        } else {
          bubble.style.backgroundColor = '#f0f0f0';
          bubble.style.color = '#333';
        }
        
        bubble.textContent = message.text;
        messageDiv.appendChild(bubble);
        
        // Add option buttons if available
        if (message.sender === 'bot' && message.options) {
          const optionsDiv = document.createElement('div');
          optionsDiv.style.marginTop = '8px';
          optionsDiv.style.display = 'flex';
          optionsDiv.style.flexDirection = 'column';
          optionsDiv.style.gap = '6px';
          
          message.options.forEach(function(option) {
            const button = document.createElement('button');
            button.textContent = option;
            button.style.textAlign = 'left';
            button.style.padding = '8px 12px';
            button.style.border = '1px solid #ddd';
            button.style.borderRadius = '6px';
            button.style.backgroundColor = 'white';
            button.style.cursor = 'pointer';
            
            button.addEventListener('click', function() {
              handleOptionClick(option);
            });
            
            optionsDiv.appendChild(button);
          });
          
          messageDiv.appendChild(optionsDiv);
        }
        
        messagesContainer.appendChild(messageDiv);
      });
      
      // Add typing indicator if needed
      if (isTyping) {
        const typingDiv = document.createElement('div');
        typingDiv.style.marginBottom = '12px';
        typingDiv.style.textAlign = 'left';
        
        const typingBubble = document.createElement('div');
        typingBubble.style.display = 'inline-block';
        typingBubble.style.padding = '12px 16px';
        typingBubble.style.borderRadius = '10px';
        typingBubble.style.backgroundColor = '#f0f0f0';
        
        typingBubble.innerHTML = '<div style="display: flex; gap: 4px;"><div style="width: 6px; height: 6px; background-color: #999; border-radius: 50%; animation: typing-dot 1s infinite;"></div><div style="width: 6px; height: 6px; background-color: #999; border-radius: 50%; animation: typing-dot 1s infinite 0.2s;"></div><div style="width: 6px; height: 6px; background-color: #999; border-radius: 50%; animation: typing-dot 1s infinite 0.4s;"></div></div>';
        
        typingDiv.appendChild(typingBubble);
        messagesContainer.appendChild(typingDiv);
      }
      
      // Scroll to bottom
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Add styles for typing animation
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes typing-dot {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
      }
    `;
    document.head.appendChild(style);
    
    // Initialize with first message
    renderMessages();
  });