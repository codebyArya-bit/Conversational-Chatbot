import React from 'react';

const About: React.FC = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '30px', color: '#333' }}>About Our Chatbot</h1>
      
      <div style={{ lineHeight: '1.6', color: '#555' }}>
        <section style={{ marginBottom: '30px' }}>
          <h2 style={{ color: '#007bff', marginBottom: '15px' }}>What We Do</h2>
          <p>
            Our AI-powered conversational chatbot is designed to provide intelligent support and assistance 
            for various technical and general inquiries. We leverage advanced natural language processing 
            to understand and respond to your questions effectively.
          </p>
        </section>

        <section style={{ marginBottom: '30px' }}>
          <h2 style={{ color: '#007bff', marginBottom: '15px' }}>Key Features</h2>
          <ul style={{ paddingLeft: '20px' }}>
            <li style={{ marginBottom: '10px' }}>Intelligent conversation handling</li>
            <li style={{ marginBottom: '10px' }}>Device specification management</li>
            <li style={{ marginBottom: '10px' }}>Support ticket system</li>
            <li style={{ marginBottom: '10px' }}>User profile management</li>
            <li style={{ marginBottom: '10px' }}>Admin dashboard for ticket management</li>
            <li style={{ marginBottom: '10px' }}>Chat history tracking</li>
          </ul>
        </section>

        <section style={{ marginBottom: '30px' }}>
          <h2 style={{ color: '#007bff', marginBottom: '15px' }}>How It Works</h2>
          <p>
            Simply start a conversation with our chatbot, and it will assist you with your queries. 
            You can also create support tickets for more complex issues that require human intervention. 
            Our system tracks your device specifications to provide more personalized assistance.
          </p>
        </section>

        <section style={{ marginBottom: '30px' }}>
          <h2 style={{ color: '#007bff', marginBottom: '15px' }}>Technology Stack</h2>
          <p>
            Built with modern web technologies including React, TypeScript, Flask, and powered by 
            advanced AI models to ensure reliable and intelligent responses.
          </p>
        </section>

        <div style={{ marginTop: '40px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px', textAlign: 'center' }}>
          <h3 style={{ color: '#333', marginBottom: '15px' }}>Ready to Get Started?</h3>
          <p style={{ marginBottom: '20px' }}>Experience the power of AI-assisted support today.</p>
          <a 
            href="/chat" 
            style={{ 
              display: 'inline-block', 
              padding: '12px 24px', 
              backgroundColor: '#007bff', 
              color: 'white', 
              textDecoration: 'none', 
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            Start Chatting
          </a>
        </div>
      </div>
    </div>
  );
};

export default About;