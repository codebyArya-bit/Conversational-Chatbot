import React from 'react';

const Services: React.FC = () => {
  const services = [
    {
      title: 'AI-Powered Chat Support',
      description: 'Get instant responses to your technical questions with our intelligent chatbot.',
      features: ['24/7 Availability', 'Instant Responses', 'Context-Aware Conversations', 'Multi-topic Support']
    },
    {
      title: 'Device Management',
      description: 'Manage and track your device specifications for personalized support.',
      features: ['Device Registration', 'Specification Tracking', 'Primary Device Setting', 'Hardware Compatibility']
    },
    {
      title: 'Support Ticket System',
      description: 'Create and track support tickets for complex issues requiring human assistance.',
      features: ['Ticket Creation', 'Priority Levels', 'Status Tracking', 'Admin Response System']
    },
    {
      title: 'User Profile Management',
      description: 'Manage your account, view chat history, and track your support requests.',
      features: ['Profile Overview', 'Chat History', 'Ticket History', 'Account Settings']
    }
  ];

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '50px' }}>
        <h1 style={{ marginBottom: '20px', color: '#333', fontSize: '2.5rem' }}>Our Services</h1>
        <p style={{ color: '#666', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
          Comprehensive AI-powered support solutions designed to help you get the most out of your technology.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginBottom: '50px' }}>
        {services.map((service, index) => (
          <div key={index} style={{ 
            border: '1px solid #e0e0e0', 
            borderRadius: '12px', 
            padding: '30px', 
            backgroundColor: 'white',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            transition: 'transform 0.3s ease'
          }}>
            <h3 style={{ color: '#007bff', marginBottom: '15px', fontSize: '1.4rem' }}>
              {service.title}
            </h3>
            <p style={{ color: '#555', marginBottom: '20px', lineHeight: '1.6' }}>
              {service.description}
            </p>
            <h4 style={{ color: '#333', marginBottom: '10px', fontSize: '1.1rem' }}>Features:</h4>
            <ul style={{ paddingLeft: '20px', color: '#666' }}>
              {service.features.map((feature, featureIndex) => (
                <li key={featureIndex} style={{ marginBottom: '8px' }}>
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div style={{ backgroundColor: '#f8f9fa', padding: '40px', borderRadius: '12px', textAlign: 'center' }}>
        <h2 style={{ color: '#333', marginBottom: '20px' }}>Getting Started</h2>
        <p style={{ color: '#666', marginBottom: '30px', fontSize: '1.1rem' }}>
          Ready to experience our services? Choose how you'd like to begin:
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap' }}>
          <a 
            href="/register" 
            style={{ 
              display: 'inline-block', 
              padding: '12px 24px', 
              backgroundColor: '#007bff', 
              color: 'white', 
              textDecoration: 'none', 
              borderRadius: '6px',
              fontWeight: 'bold',
              transition: 'background-color 0.3s ease'
            }}
          >
            Create Account
          </a>
          <a 
            href="/chat" 
            style={{ 
              display: 'inline-block', 
              padding: '12px 24px', 
              backgroundColor: '#28a745', 
              color: 'white', 
              textDecoration: 'none', 
              borderRadius: '6px',
              fontWeight: 'bold',
              transition: 'background-color 0.3s ease'
            }}
          >
            Start Chatting
          </a>
          <a 
            href="/support" 
            style={{ 
              display: 'inline-block', 
              padding: '12px 24px', 
              backgroundColor: '#ffc107', 
              color: '#333', 
              textDecoration: 'none', 
              borderRadius: '6px',
              fontWeight: 'bold',
              transition: 'background-color 0.3s ease'
            }}
          >
            Get Support
          </a>
        </div>
      </div>
    </div>
  );
};

export default Services;