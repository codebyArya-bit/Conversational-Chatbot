import React, { useState, useEffect } from 'react';
import { chatAPI } from '../services/api';

interface ChatSession {
  id: number;
  title: string;
  created_at: string;
  message_count: number;
}

const ChatHistory: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    try {
      setLoading(true);
      const response = await chatAPI.getChatSessions();
      setSessions(response);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch chat history');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSession = async (sessionId: number) => {
    if (!window.confirm('Are you sure you want to delete this chat session?')) {
      return;
    }

    try {
      await chatAPI.deleteSession(sessionId);
      setSessions(sessions.filter(session => session.id !== sessionId));
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to delete session');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <div>Loading chat history...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px' }}>
        <div style={{ color: 'red', marginBottom: '20px' }}>
          Error: {error}
        </div>
        <button onClick={fetchChatHistory} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '30px', color: '#333' }}>Chat History</h1>
      
      {sessions.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
          <h3 style={{ color: '#666', marginBottom: '10px' }}>No chat sessions found</h3>
          <p style={{ color: '#888' }}>Start a new conversation to see your chat history here.</p>
          <a href="/chat" style={{ display: 'inline-block', marginTop: '20px', padding: '10px 20px', backgroundColor: '#007bff', color: 'white', textDecoration: 'none', borderRadius: '4px' }}>
            Start New Chat
          </a>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '20px' }}>
          {sessions.map((session) => (
            <div key={session.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: 'white' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                <h3 style={{ margin: '0', color: '#333' }}>{session.title}</h3>
                <button 
                  onClick={() => handleDeleteSession(session.id)}
                  style={{ padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}
                >
                  Delete
                </button>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: '#666', fontSize: '14px' }}>
                <span>{session.message_count} messages</span>
                <span>{new Date(session.created_at).toLocaleDateString()}</span>
              </div>
              <div style={{ marginTop: '15px' }}>
                <a 
                  href={`/chat/${session.id}`} 
                  style={{ display: 'inline-block', padding: '8px 16px', backgroundColor: '#007bff', color: 'white', textDecoration: 'none', borderRadius: '4px', fontSize: '14px' }}
                >
                  Continue Chat
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ChatHistory;