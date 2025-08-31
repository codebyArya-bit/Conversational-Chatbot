import React, { useState, useEffect } from 'react';
import { deviceAPI } from '../services/api';
import { DeviceSpec } from '../services/api';

const DeviceSpecs: React.FC = () => {
  const [devices, setDevices] = useState<DeviceSpec[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    device_name: '',
    device_type: '',
    brand: '',
    model: '',
    operating_system: '',
    processor: '',
    ram: '',
    storage: '',
    graphics_card: '',
    network_adapter: '',
    other_specs: '',
    additional_info: '',
    is_primary: false
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    try {
      setLoading(true);
      const response = await deviceAPI.getDeviceSpecs();
      setDevices(response);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load devices');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await deviceAPI.createDeviceSpec(formData);
      setShowForm(false);
      setFormData({
        device_name: '',
        device_type: '',
        brand: '',
        model: '',
        operating_system: '',
        processor: '',
        ram: '',
        storage: '',
        graphics_card: '',
        network_adapter: '',
        other_specs: '',
        additional_info: '',
        is_primary: false
      });
      await loadDevices();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to save device');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (deviceId: number) => {
    if (!window.confirm('Are you sure you want to delete this device?')) {
      return;
    }

    try {
      await deviceAPI.deleteDeviceSpec(deviceId);
      await loadDevices();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to delete device');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
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
              <h1 className="text-2xl font-bold text-gray-900">Device Specifications</h1>
              <button
                onClick={() => setShowForm(!showForm)}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                {showForm ? 'Cancel' : 'Add Device'}
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
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Device Name *
                    </label>
                    <input
                      type="text"
                      name="device_name"
                      value={formData.device_name}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="My Laptop"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Device Type *
                    </label>
                    <select
                      name="device_type"
                      value={formData.device_type}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="laptop">Laptop</option>
                      <option value="desktop">Desktop</option>
                      <option value="tablet">Tablet</option>
                      <option value="smartphone">Smartphone</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Operating System
                    </label>
                    <input
                      type="text"
                      name="operating_system"
                      value={formData.operating_system}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Windows 11, macOS, Ubuntu, etc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Processor
                    </label>
                    <input
                      type="text"
                      name="processor"
                      value={formData.processor}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Intel i7, AMD Ryzen 5, etc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      RAM
                    </label>
                    <input
                      type="text"
                      name="ram"
                      value={formData.ram}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="8GB, 16GB, etc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Storage
                    </label>
                    <input
                      type="text"
                      name="storage"
                      value={formData.storage}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="256GB SSD, 1TB HDD, etc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Graphics Card
                    </label>
                    <input
                      type="text"
                      name="graphics_card"
                      value={formData.graphics_card}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="NVIDIA GTX 1660, Intel UHD, etc."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Network Adapter
                    </label>
                    <input
                      type="text"
                      name="network_adapter"
                      value={formData.network_adapter}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Wi-Fi 6, Ethernet, etc."
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Other Specifications
                  </label>
                  <textarea
                    name="other_specs"
                    value={formData.other_specs}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Any additional specifications or notes..."
                  />
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="is_primary"
                    checked={formData.is_primary}
                    onChange={handleInputChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label className="ml-2 block text-sm text-gray-700">
                    Set as primary device
                  </label>
                </div>

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
                    {submitting ? 'Saving...' : 'Save Device'}
                  </button>
                </div>
              </form>
            </div>
          )}

          <div className="px-6 py-4">
            {devices.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500">No devices registered yet.</p>
                <button
                  onClick={() => setShowForm(true)}
                  className="mt-2 text-blue-600 hover:text-blue-800"
                >
                  Add your first device
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {devices.map((device) => (
                  <div key={device.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {device.device_name}
                        {device.is_primary && (
                          <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            Primary
                          </span>
                        )}
                      </h3>
                      <button
                        onClick={() => handleDelete(device.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                    
                    <div className="space-y-2 text-sm text-gray-600">
                      <p><span className="font-medium">Type:</span> {device.device_type}</p>
                      {device.operating_system && (
                        <p><span className="font-medium">OS:</span> {device.operating_system}</p>
                      )}
                      {device.processor && (
                        <p><span className="font-medium">Processor:</span> {device.processor}</p>
                      )}
                      {device.ram && (
                        <p><span className="font-medium">RAM:</span> {device.ram}</p>
                      )}
                      {device.storage && (
                        <p><span className="font-medium">Storage:</span> {device.storage}</p>
                      )}
                      {device.graphics_card && (
                        <p><span className="font-medium">Graphics:</span> {device.graphics_card}</p>
                      )}
                      {device.network_adapter && (
                        <p><span className="font-medium">Network:</span> {device.network_adapter}</p>
                      )}
                      {device.other_specs && (
                        <p><span className="font-medium">Other:</span> {device.other_specs}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeviceSpecs;