/**
 * API Service Client for Smart Hygiene Risk Prediction System.
 * Connects with FastAPI backend endpoints.
 */

const API_BASE = (typeof window !== 'undefined' && (window.location.protocol === 'file:' || window.location.origin === 'null'))
  ? 'http://127.0.0.1:8000'
  : '';

class ApiService {
  static async request(endpoint, options = {}) {
    try {
      const url = `${API_BASE}${endpoint}`;
      const config = {
        headers: {
          'Accept': 'application/json',
          ...(options.headers || {})
        },
        ...options
      };

      const response = await fetch(url, config);
      if (!response.ok) {
        let errMessage = `HTTP Error ${response.status}`;
        try {
          const errData = await response.json();
          if (errData.detail) {
            errMessage = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
          } else if (errData.message) {
            errMessage = errData.message;
          }
        } catch (_) {}
        throw new Error(errMessage);
      }

      return await response.json();
    } catch (err) {
      console.error(`API Request Error [${endpoint}]:`, err);
      throw err;
    }
  }

  // Health
  static checkHealth() {
    return this.request('/api/health');
  }

  // Predict
  static predictRisk(payload) {
    return this.request('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  static uploadCsv(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.request('/api/predict/upload-csv', {
      method: 'POST',
      body: formData
    });
  }

  // Inspections
  static getInspections(risk = null, search = null) {
    const params = new URLSearchParams();
    if (risk && risk !== 'All') params.append('risk', risk);
    if (search) params.append('search', search);
    return this.request(`/api/inspections?${params.toString()}`);
  }

  static getInspectionById(id) {
    return this.request(`/api/inspections/${id}`);
  }

  static createInspection(payload) {
    return this.request('/api/inspections', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  static deleteInspection(id) {
    return this.request(`/api/inspections/${id}`, {
      method: 'DELETE'
    });
  }

  // Facilities
  static getFacilities() {
    return this.request('/api/facilities');
  }

  // Analytics
  static getStats() {
    return this.request('/api/analytics/stats');
  }

  static getFeatureImportance() {
    return this.request('/api/analytics/feature-importance');
  }

  static getModelInfo() {
    return this.request('/api/analytics/model-info');
  }
}

window.ApiService = ApiService;
