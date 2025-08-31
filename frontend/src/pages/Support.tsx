import React, { useState, useEffect } from 'react';
import { supportAPI, deviceAPI } from '../services/api';
import { SupportTicket, DeviceSpec } from '../services/api';

const Support: React.FC = () => {
  const [tickets, setTickets] = useState<SupportTicket[]>([]);
  const [devices, setDevices] = useState<DeviceSpec[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'hardware',
    priority: 'medium'
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Load tickets
      const ticketsResponse = await supportAPI.getTickets();
      setTickets(ticketsResponse);
      
      // Load devices for context
      const devicesResponse = await deviceAPI.getDeviceSpecs();
      setDevices(devicesResponse);
      
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await supportAPI.createTicket(formData);
      setShowForm(false);
      setFormData({
        title: '',
        description: '',
        category: 'hardware',
        priority: 'medium'
      });
      await loadData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create ticket');
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open':
        return 'bg-yellow-100 text-yellow-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      case 'closed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h1 className="text-2xl font-bold text-gray-900">Support Center</h1>
              <button
                onClick={() => setShowForm(!showForm)}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                {showForm ? 'Cancel' : 'Create Ticket'}
              </button>
            </div>
          </div>

          {error && (
            <div className="mx-6 mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {showForm && (
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Create Support Ticket</h2>
              
              {devices.length === 0 && (
                <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                  <p className="text-yellow-800">
                    <strong>Tip:</strong> Consider adding your device specifications first for better support.
                    <a href="/device-specs" className="ml-2 text-blue-600 hover:text-blue-800">Add Device</a>
                  </p>
                </div>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title *
                  </label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Brief description of your issue"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Category *
                    </label>
                    <select
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="hardware">Hardware Issue</option>
                      <option value="software">Software Issue</option>
                      <option value="network">Network/Connectivity</option>
                      <option value="account">Account/Login</option>
                      <option value="general">General Inquiry</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Priority *
                    </label>
                    <select
                      name="priority"
                      value={formData.priority}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="low">Low - General question</option>
                      <option value="medium">Medium - Standard issue</option>
                      <option value="high">High - Urgent problem</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description *
                  </label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    required
                    rows={6}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Please provide detailed information about your issue, including:
- What you were trying to do
- What happened instead
- Any error messages you saw
- Steps you've already tried
- When the problem started"
                  />
                </div>

                {devices.length > 0 && (
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
                    <h3 className="text-sm font-medium text-blue-900 mb-2">Your Primary Device Info</h3>
                    {(() => {
                      const primaryDevice = devices.find(d => d.is_primary) || devices[0];
                      return (
                        <div className="text-sm text-blue-800">
                          <p><strong>Device:</strong> {primaryDevice.device_name} ({primaryDevice.device_type})</p>
                          {primaryDevice.operating_system && (
                            <p><strong>OS:</strong> {primaryDevice.operating_system}</p>
                          )}
                          {primaryDevice.processor && (
                            <p><strong>Processor:</strong> {primaryDevice.processor}</p>
                          )}
                          {primaryDevice.ram && (
                            <p><strong>RAM:</strong> {primaryDevice.ram}</p>
                          )}
                        </div>
                      );
                    })()}
                    <p className="text-xs text-blue-700 mt-2">
                      This information will be automatically included with your ticket to help our support team.
                    </p>
                  </div>
                )}

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => setShowForm(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
                  >
                    {submitting ? 'Creating...' : 'Create Ticket'}
                  </button>
                </div>
              </form>
            </div>
          )}

          <div className="px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Support Tickets</h2>
            
            {tickets.length === 0 ? (
              <div className="text-center py-8">
                <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <p className="text-gray-500 mb-4">No support tickets yet</p>
                <button
                  onClick={() => setShowForm(true)}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Create Your First Ticket
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {tickets.map((ticket) => (
                  <div key={ticket.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">{ticket.title}</h3>
                        <p className="text-sm text-gray-600">Ticket #{ticket.ticket_number}</p>
                      </div>
                      <div className="flex space-x-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(ticket.priority)}`}>
                          {ticket.priority} priority
                        </span>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(ticket.status)}`}>
                          {ticket.status}
                        </span>
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <p className="text-gray-700">{ticket.description}</p>
                    </div>
                    
                    <div className="flex justify-between items-center text-sm text-gray-500">
                      <div className="flex space-x-4">
                        <span>Category: {ticket.category}</span>
                        <span>Created: {formatDate(ticket.created_at)}</span>
                        {ticket.updated_at !== ticket.created_at && (
                          <span>Updated: {formatDate(ticket.updated_at)}</span>
                        )}
                      </div>
                      {ticket.status === 'resolved' && ticket.resolved_at && (
                        <span className="text-green-600">Resolved: {formatDate(ticket.resolved_at)}</span>
                      )}
                    </div>
                    
                    {ticket.admin_response && (
                      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
                        <h4 className="text-sm font-medium text-blue-900 mb-2">Support Response:</h4>
                        <p className="text-blue-800">{ticket.admin_response}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Help Section */}
        <div className="mt-8 bg-white shadow rounded-lg">
          <div className="px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Need Help?</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-md font-medium text-gray-900 mb-2">Before Creating a Ticket</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Try restarting your device</li>
                  <li>• Check for software updates</li>
                  <li>• Search our FAQ for common solutions</li>
                  <li>• Try the chatbot for quick answers</li>
                </ul>
              </div>
              <div>
                <h3 className="text-md font-medium text-gray-900 mb-2">Quick Actions</h3>
                <div className="space-y-2">
                  <a
                    href="/chat"
                    className="block text-blue-600 hover:text-blue-800 text-sm"
                  >
                    → Chat with our AI assistant
                  </a>
                  <a
                    href="/device-specs"
                    className="block text-blue-600 hover:text-blue-800 text-sm"
                  >
                    → Manage your device specifications
                  </a>
                  <a
                    href="/profile"
                    className="block text-blue-600 hover:text-blue-800 text-sm"
                  >
                    → View your profile and history
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Support;