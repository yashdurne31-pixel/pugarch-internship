/**
 * Main Application Coordinator & UI State Manager.
 * Smart Hygiene Risk Prediction System - AegisHygiene AI.
 */

class ToastManager {
  constructor() {
    this.container = document.getElementById('toast-container');
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      document.body.appendChild(this.container);
    }
  }

  show(message, type = 'info', duration = 3500) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'warning') icon = '⚠️';
    if (type === 'error') icon = '❌';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, duration);
  }
}

class App {
  constructor() {
    window.Toast = new ToastManager();
    this.initTabs();
    this.initTheme();
    this.initHealthCheck();
    this.initControllers();
  }

  initTabs() {
    const tabButtons = document.querySelectorAll('.nav-tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.dataset.tab;
        tabButtons.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        const targetEl = document.getElementById(targetId);
        if (targetEl) targetEl.classList.add('active');

        // Trigger updates when tab becomes active
        if (targetId === 'tab-inspections' && window.InspectionsControllerInstance) {
          window.InspectionsControllerInstance.loadInspections();
        } else if (targetId === 'tab-analytics' && window.AnalyticsControllerInstance) {
          window.AnalyticsControllerInstance.init();
        }
      });
    });
  }

  initTheme() {
    const themeBtn = document.getElementById('btn-toggle-theme');
    const saved = localStorage.getItem('aegis_theme');
    if (saved === 'light') {
      document.body.classList.add('light-theme');
    }

    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        localStorage.setItem('aegis_theme', isLight ? 'light' : 'dark');
        window.Toast.show(`Theme switched to ${isLight ? 'Light' : 'Dark'} mode`, 'info');
      });
    }
  }

  async initHealthCheck() {
    const statusText = document.getElementById('backend-status-text');
    const statusDot = document.getElementById('backend-status-dot');

    const check = async () => {
      try {
        const res = await window.ApiService.checkHealth();
        if (res.status === 'healthy') {
          if (statusText) statusText.textContent = 'API Connected (v1.0.0)';
          if (statusDot) {
            statusDot.style.background = 'var(--safe-green)';
            statusDot.style.boxShadow = '0 0 8px var(--safe-green)';
          }
        }
      } catch (err) {
        if (statusText) statusText.textContent = 'API Offline';
        if (statusDot) {
          statusDot.style.background = 'var(--hazard-red)';
          statusDot.style.boxShadow = '0 0 8px var(--hazard-red)';
        }
      }
    };

    await check();
    setInterval(check, 30000); // Check every 30 seconds
  }

  initControllers() {
    window.PredictorControllerInstance = new window.PredictorController();
    window.InspectionsControllerInstance = new window.InspectionsController();
    window.InspectionsControllerInstance.init();
    window.AnalyticsControllerInstance = new window.AnalyticsController();
    window.AnalyticsControllerInstance.init();
    window.BatchControllerInstance = new window.BatchController();

    // Run initial prediction demo
    setTimeout(() => {
      window.PredictorControllerInstance.runPrediction();
    }, 600);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.AegisApp = new App();
});
