import React from 'react';

const Resources: React.FC = () => {
  const resourceCategories = [
    {
      title: 'Getting Started',
      resources: [
        { name: 'Quick Start Guide', description: 'Learn how to use the chatbot effectively', type: 'Guide' },
        { name: 'Account Setup', description: 'Step-by-step account creation and configuration', type: 'Tutorial' },
        { name: 'First Chat Session', description: 'How to start your first conversation', type: 'Tutorial' }
      ]
    },
    {
      title: 'Device Management',
      resources: [
        { name: 'Adding Device Specs', description: 'How to register your devices for better support', type: 'Guide' },
        { name: 'Device Compatibility', description: 'Understanding supported device types', type: 'Reference' },
        { name: 'Troubleshooting Devices', description: 'Common device-related issues and solutions', type: 'FAQ' }
      ]
    },
    {
      title: 'Support System',
      resources: [
        { name: 'Creating Support Tickets', description: 'When and how to create support tickets', type: 'Guide' },
        { name: 'Ticket Priority Levels', description: 'Understanding different priority levels', type: 'Reference' },
        { name: 'Response Times', description: 'Expected response times for different ticket types', type: 'Reference' }
      ]
    },
    {
      title: 'Advanced Features',
      resources: [
        { name: 'Chat History Management', description: 'Accessing and managing your conversation history', type: 'Guide' },
        { name: 'Profile Customization', description: 'Personalizing your user experience', type: 'Tutorial' },
        { name: 'Admin Features', description: 'Administrative functions and capabilities', type: 'Reference' }
      ]
    }
  ];

  const faqs = [
    {
      question: 'How do I start a conversation with the chatbot?',
      answer: 'Simply navigate to the Chat page and type your question. The AI will respond instantly to help you with your inquiry.'
    },
    {
      question: 'What types of questions can the chatbot answer?',
      answer: 'Our chatbot can help with technical support, device troubleshooting, general inquiries, and guide you through various processes.'
    },
    {
      question: 'When should I create a support ticket instead of using chat?',
      answer: 'Create a support ticket for complex issues that require human intervention, account-specific problems, or when you need a formal record of your request.'
    },
    {
      question: 'How do I add my device specifications?',
      answer: 'Go to the Device Specs page in your profile, click "Add Device," and fill in the required information about your hardware.'
    },
    {
      question: 'Can I access my chat history?',
      answer: 'Yes, all your conversations are saved and can be accessed through the Chat History page in your profile.'
    }
  ];

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Guide': return '#007bff';
      case 'Tutorial': return '#28a745';
      case 'Reference': return '#ffc107';
      case 'FAQ': return '#dc3545';
      default: return '#6c757d';
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '50px' }}>
        <h1 style={{ marginBottom: '20px', color: '#333', fontSize: '2.5rem' }}>Resources & Documentation</h1>
        <p style={{ color: '#666', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
          Everything you need to know to make the most of our chatbot platform.
        </p>
      </div>

      {/* Resource Categories */}
      <div style={{ marginBottom: '60px' }}>
        <h2 style={{ color: '#333', marginBottom: '30px', fontSize: '2rem' }}>Documentation</h2>
        {resourceCategories.map((category, categoryIndex) => (
          <div key={categoryIndex} style={{ marginBottom: '40px' }}>
            <h3 style={{ color: '#007bff', marginBottom: '20px', fontSize: '1.5rem' }}>
              {category.title}
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              {category.resources.map((resource, resourceIndex) => (
                <div key={resourceIndex} style={{
                  border: '1px solid #e0e0e0',
                  borderRadius: '8px',
                  padding: '20px',
                  backgroundColor: 'white',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                    <h4 style={{ color: '#333', margin: '0', fontSize: '1.2rem' }}>{resource.name}</h4>
                    <span style={{
                      padding: '4px 8px',
                      backgroundColor: getTypeColor(resource.type),
                      color: resource.type === 'Reference' ? '#333' : 'white',
                      borderRadius: '4px',
                      fontSize: '0.8rem',
                      fontWeight: 'bold'
                    }}>
                      {resource.type}
                    </span>
                  </div>
                  <p style={{ color: '#666', margin: '0', lineHeight: '1.5' }}>
                    {resource.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* FAQ Section */}
      <div style={{ marginBottom: '40px' }}>
        <h2 style={{ color: '#333', marginBottom: '30px', fontSize: '2rem' }}>Frequently Asked Questions</h2>
        <div style={{ display: 'grid', gap: '20px' }}>
          {faqs.map((faq, index) => (
            <div key={index} style={{
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
              padding: '25px',
              backgroundColor: 'white',
              boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
            }}>
              <h4 style={{ color: '#007bff', marginBottom: '15px', fontSize: '1.2rem' }}>
                {faq.question}
              </h4>
              <p style={{ color: '#555', margin: '0', lineHeight: '1.6' }}>
                {faq.answer}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Contact Section */}
      <div style={{ backgroundColor: '#f8f9fa', padding: '40px', borderRadius: '12px', textAlign: 'center' }}>
        <h2 style={{ color: '#333', marginBottom: '20px' }}>Need More Help?</h2>
        <p style={{ color: '#666', marginBottom: '30px', fontSize: '1.1rem' }}>
          Can't find what you're looking for? We're here to help!
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap' }}>
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
            Ask the Chatbot
          </a>
          <a 
            href="/support" 
            style={{ 
              display: 'inline-block', 
              padding: '12px 24px', 
              backgroundColor: '#28a745', 
              color: 'white', 
              textDecoration: 'none', 
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            Create Support Ticket
          </a>
          <a 
            href="/contact" 
            style={{ 
              display: 'inline-block', 
              padding: '12px 24px', 
              backgroundColor: '#6c757d', 
              color: 'white', 
              textDecoration: 'none', 
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            Contact Us
          </a>
        </div>
      </div>
    </div>
  );
};

export default Resources;