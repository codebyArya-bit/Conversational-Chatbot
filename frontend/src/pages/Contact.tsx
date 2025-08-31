import React, { useState } from 'react';

const Contact: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
    priority: 'medium'
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSubmitMessage('Thank you for your message! We\'ll get back to you within 24 hours.');
      setFormData({
        name: '',
        email: '',
        subject: '',
        message: '',
        priority: 'medium'
      });
    } catch (error) {
      setSubmitMessage('Sorry, there was an error sending your message. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactMethods = [
    {
      title: 'Live Chat',
      description: 'Get instant help from our AI chatbot',
      icon: '💬',
      action: 'Start Chat',
      link: '/chat',
      color: '#007bff'
    },
    {
      title: 'Support Ticket',
      description: 'Create a ticket for complex issues',
      icon: '🎫',
      action: 'Create Ticket',
      link: '/support',
      color: '#28a745'
    },
    {
      title: 'Email Support',
      description: 'Send us an email for detailed inquiries',
      icon: '📧',
      action: 'Send Email',
      link: 'mailto:support@chatbot.com',
      color: '#ffc107'
    },
    {
      title: 'Phone Support',
      description: 'Call us for urgent matters',
      icon: '📞',
      action: 'Call Now',
      link: 'tel:+1-800-CHATBOT',
      color: '#dc3545'
    }
  ];

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '50px' }}>
        <h1 style={{ marginBottom: '20px', color: '#333', fontSize: '2.5rem' }}>Contact Us</h1>
        <p style={{ color: '#666', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
          We're here to help! Choose the best way to reach us or send us a message directly.
        </p>
      </div>

      {/* Contact Methods */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '50px' }}>
        {contactMethods.map((method, index) => (
          <div key={index} style={{
            border: '1px solid #e0e0e0',
            borderRadius: '12px',
            padding: '30px',
            backgroundColor: 'white',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            textAlign: 'center',
            transition: 'transform 0.3s ease'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '15px' }}>{method.icon}</div>
            <h3 style={{ color: method.color, marginBottom: '10px', fontSize: '1.3rem' }}>
              {method.title}
            </h3>
            <p style={{ color: '#666', marginBottom: '20px', lineHeight: '1.5' }}>
              {method.description}
            </p>
            <a 
              href={method.link}
              style={{
                display: 'inline-block',
                padding: '10px 20px',
                backgroundColor: method.color,
                color: method.title === 'Email Support' ? '#333' : 'white',
                textDecoration: 'none',
                borderRadius: '6px',
                fontWeight: 'bold',
                transition: 'opacity 0.3s ease'
              }}
            >
              {method.action}
            </a>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '50px', alignItems: 'start' }}>
        {/* Contact Form */}
        <div>
          <h2 style={{ color: '#333', marginBottom: '20px', fontSize: '1.8rem' }}>Send us a Message</h2>
          <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '20px' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '5px', color: '#333', fontWeight: 'bold' }}>
                Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '5px', color: '#333', fontWeight: 'bold' }}>
                Email *
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '5px', color: '#333', fontWeight: 'bold' }}>
                Priority
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleInputChange}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '5px', color: '#333', fontWeight: 'bold' }}>
                Subject *
              </label>
              <input
                type="text"
                name="subject"
                value={formData.subject}
                onChange={handleInputChange}
                required
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '5px', color: '#333', fontWeight: 'bold' }}>
                Message *
              </label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                required
                rows={6}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem',
                  resize: 'vertical'
                }}
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              style={{
                padding: '15px 30px',
                backgroundColor: isSubmitting ? '#6c757d' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                fontSize: '1.1rem',
                fontWeight: 'bold',
                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                transition: 'background-color 0.3s ease'
              }}
            >
              {isSubmitting ? 'Sending...' : 'Send Message'}
            </button>

            {submitMessage && (
              <div style={{
                padding: '15px',
                backgroundColor: submitMessage.includes('error') ? '#f8d7da' : '#d4edda',
                color: submitMessage.includes('error') ? '#721c24' : '#155724',
                border: `1px solid ${submitMessage.includes('error') ? '#f5c6cb' : '#c3e6cb'}`,
                borderRadius: '6px'
              }}>
                {submitMessage}
              </div>
            )}
          </form>
        </div>

        {/* Contact Information */}
        <div>
          <h2 style={{ color: '#333', marginBottom: '20px', fontSize: '1.8rem' }}>Get in Touch</h2>
          
          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ color: '#007bff', marginBottom: '15px' }}>Business Hours</h3>
            <div style={{ color: '#666', lineHeight: '1.6' }}>
              <p><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM EST</p>
              <p><strong>Saturday:</strong> 10:00 AM - 4:00 PM EST</p>
              <p><strong>Sunday:</strong> Closed</p>
              <p style={{ marginTop: '10px', fontStyle: 'italic' }}>
                *AI Chatbot available 24/7
              </p>
            </div>
          </div>

          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ color: '#007bff', marginBottom: '15px' }}>Contact Information</h3>
            <div style={{ color: '#666', lineHeight: '1.8' }}>
              <p><strong>Email:</strong> support@chatbot.com</p>
              <p><strong>Phone:</strong> +1 (800) CHATBOT</p>
              <p><strong>Address:</strong> 123 Tech Street, Digital City, DC 12345</p>
            </div>
          </div>

          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ color: '#007bff', marginBottom: '15px' }}>Response Times</h3>
            <div style={{ color: '#666', lineHeight: '1.6' }}>
              <p><strong>Live Chat:</strong> Instant</p>
              <p><strong>Email:</strong> Within 24 hours</p>
              <p><strong>Support Tickets:</strong> 2-4 business days</p>
              <p><strong>Phone:</strong> During business hours</p>
            </div>
          </div>

          <div style={{ backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '8px' }}>
            <h4 style={{ color: '#333', marginBottom: '10px' }}>Quick Tip</h4>
            <p style={{ color: '#666', margin: '0', fontSize: '0.95rem' }}>
              For the fastest response, try our AI chatbot first! It can handle most common questions instantly and is available 24/7.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;