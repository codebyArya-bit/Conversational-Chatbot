import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://student-chatbot-ap9p.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

export interface ChatMessage {
  id: number;
  message: string;
  response: string;
  timestamp: string;
}

export interface ChatSession {
  id: number;
  session_id?: string;
  title: string;
  created_at: string;
  updated_at?: string;
  message_count: number;
}

export interface DeviceSpec {
  id: number;
  device_name?: string;
  device_type: string;
  brand: string;
  model: string;
  operating_system: string;
  ram: string;
  storage: string;
  processor: string;
  graphics_card?: string;
  network_adapter?: string;
  additional_info?: string;
  other_specs?: string;
  is_primary?: boolean;
}

export interface SupportTicket {
  id: number;
  ticket_number?: string;
  title: string;
  description: string;
  category?: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
  admin_response?: string;
  device_info?: DeviceSpec;
  user?: { email: string; username: string; };
}

// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await api.post('/api/auth/login', { username, password });
    return response.data;
  },
  
  register: async (username: string, email: string, password: string) => {
    const response = await api.post('/api/auth/register', { username, email, password });
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/api/auth/logout');
    return response.data;
  },
  
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/auth/user');
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  sendMessage: async (message: string) => {
    const response = await api.post('/api/chat', { message });
    return response.data;
  },
  
  getChatHistory: async (): Promise<ChatMessage[]> => {
    const response = await api.get('/api/chat/history');
    return response.data;
  },
  
  getChatSessions: async (): Promise<ChatSession[]> => {
    const response = await api.get('/api/chat/sessions');
    return response.data;
  },
  
  deleteSession: async (sessionId: number) => {
    const response = await api.delete(`/api/chat/sessions/${sessionId}`);
    return response.data;
  },
};

// Device Specs API
export const deviceAPI = {
  getDeviceSpecs: async (): Promise<DeviceSpec[]> => {
    const response = await api.get('/api/device-specs');
    return response.data;
  },
  
  createDeviceSpec: async (deviceSpec: Omit<DeviceSpec, 'id'>) => {
    const response = await api.post('/api/device-specs', deviceSpec);
    return response.data;
  },
  
  updateDeviceSpec: async (id: number, deviceSpec: Partial<DeviceSpec>) => {
    const response = await api.put(`/api/device-specs/${id}`, deviceSpec);
    return response.data;
  },
  
  deleteDeviceSpec: async (id: number) => {
    const response = await api.delete(`/api/device-specs/${id}`);
    return response.data;
  },
};

// Support Tickets API
export const supportAPI = {
  getTickets: async (): Promise<SupportTicket[]> => {
    const response = await api.get('/api/support/tickets');
    return response.data;
  },
  
  createTicket: async (ticket: { title: string; description: string; priority: string }) => {
    const response = await api.post('/api/support/tickets', ticket);
    return response.data;
  },
  
  getTicket: async (id: number): Promise<SupportTicket> => {
    const response = await api.get(`/api/support/tickets/${id}`);
    return response.data;
  },
  
  updateTicket: async (id: number, updates: Partial<SupportTicket>) => {
    const response = await api.put(`/api/support/tickets/${id}`, updates);
    return response.data;
  },
};

// Admin API
export const adminAPI = {
  getAllTickets: async (): Promise<SupportTicket[]> => {
    const response = await api.get('/api/admin/tickets');
    return response.data;
  },
  
  respondToTicket: async (id: number, response: string) => {
    const result = await api.post(`/api/admin/tickets/${id}/respond`, { response });
    return result.data;
  },
  
  updateTicketStatus: async (id: number, status: string) => {
    const result = await api.put(`/api/admin/tickets/${id}/status`, { status });
    return result.data;
  },
};

export default api;