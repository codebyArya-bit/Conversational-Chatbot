import React, { useState, useEffect, useRef } from 'react';
import { chatAPI, ChatMessage } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const history = await chatAPI.getChatHistory();
      setMessages(history);
    } catch (err) {
      console.error('Failed to load chat history:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setError('');
    setLoading(true);

    // Add user message to chat immediately
    const tempMessage: ChatMessage = {
      id: Date.now(),
      message: userMessage,
      response: '',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempMessage]);

    try {
      const response = await chatAPI.sendMessage(userMessage);
      
      // Update the message with the response
      setMessages(prev => 
        prev.map(msg => 
          msg.id === tempMessage.id 
            ? { ...msg, response: response.response, id: response.id }
            : msg
        )
      );
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to send message. Please try again.');
      // Remove the temporary message on error
      setMessages(prev => prev.filter(msg => msg.id !== tempMessage.id));
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Chat Header */}
        <div className="bg-blue-600 text-white p-4">
          <h1 className="text-2xl font-bold">AI Assistant Chat</h1>
          <p className="text-blue-100">Welcome, {user?.username}! Ask me anything about technical issues.</p>
        </div>

        {/* Chat Messages */}
        <div className="h-96 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <p className="text-lg mb-2">👋 Hello! I'm your AI assistant.</p>
              <p>Ask me about any technical issues you're experiencing, and I'll do my best to help!</p>
            </div>
          ) : (
            messages.map((msg) => (
              <div key={msg.id} className="space-y-2">
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="bg-blue-600 text-white rounded-lg px-4 py-2 max-w-xs lg:max-w-md">
                    <p className="text-sm">{msg.message}</p>
                    <p className="text-xs text-blue-100 mt-1">
                      {formatTimestamp(msg.timestamp)}
                    </p>
                  </div>
                </div>
                
                {/* AI Response */}
                {msg.response && (
                  <div className="flex justify-start">
                    <div className="bg-white border rounded-lg px-4 py-2 max-w-xs lg:max-w-md shadow-sm">
                      <div className="flex items-center mb-1">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                        <span className="text-xs text-gray-500 font-medium">AI Assistant</span>
                      </div>
                      <p className="text-sm text-gray-800 whitespace-pre-wrap">{msg.response}</p>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
          
          {/* Loading indicator */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white border rounded-lg px-4 py-2 shadow-sm">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-xs text-gray-500 font-medium mr-2">AI Assistant</span>
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        {/* Chat Input */}
        <div className="border-t bg-white p-4">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !inputMessage.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
            >
              <PaperAirplaneIcon className="h-5 w-5" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
          <p className="text-xs text-gray-500 mt-2">
            💡 Tip: Be specific about your technical issue for better assistance!
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="font-semibold text-gray-900 mb-2">Common Issues</h3>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• Software installation problems</li>
            <li>• Network connectivity issues</li>
            <li>• Hardware troubleshooting</li>
          </ul>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="font-semibold text-gray-900 mb-2">Need More Help?</h3>
          <p className="text-sm text-gray-600 mb-2">
            If the AI can't solve your issue, you can create a support ticket for human assistance.
          </p>
          <a href="/support" className="text-blue-600 hover:text-blue-800 text-sm font-medium">
            Create Support Ticket →
          </a>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="font-semibold text-gray-900 mb-2">Your Profile</h3>
          <p className="text-sm text-gray-600 mb-2">
            Keep your device specifications updated for better personalized support.
          </p>
          <a href="/device-specs" className="text-blue-600 hover:text-blue-800 text-sm font-medium">
            Update Device Info →
          </a>
        </div>
      </div>
    </div>
  );
};

export default Chat;