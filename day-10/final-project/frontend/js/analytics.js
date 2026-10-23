/**
 * Analytics & Model Performance Controller.
 * Smart Hygiene Risk Prediction System.
 */

class AnalyticsController {
  constructor() {
    this.totalFacEl = document.getElementById('kpi-total-facilities');
    this.totalInspEl = document.getElementById('kpi-total-inspections');
    this.avgScoreEl = document.getElementById('kpi-avg-score');
    this.criticalEl = document.getElementById('kpi-critical-count');
    this.featContainer = document.getElementById('feature-importance-list');
    this.modelTableBody = document.getElementById('model-benchmark-tbody');

    this.lightboxModal = document.getElementById('modal-chart-lightbox');
    this.lightboxImg = document.getElementById('lightbox-img');
    this.lightboxTitle = document.getElementById('lightbox-title');

    this.initChartClick();
  }

  async init() {
    await this.loadStats();
    await this.loadFeatureImportance();
    await this.loadModelBenchmarks();
  }

  async loadStats() {
    try {
      const stats = await window.ApiService.getStats();
      if (this.totalFacEl) this.totalFacEl.textContent = stats.total_facilities || 0;
      if (this.totalInspEl) this.totalInspEl.textContent = stats.total_inspections || 0;
      if (this.avgScoreEl) this.avgScoreEl.textContent = (stats.average_risk_score || 0).toFixed(1);
      if (this.criticalEl) this.criticalEl.textContent = stats.critical_hazard_count || 0;
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }

  async loadFeatureImportance() {
    if (!this.featContainer) return;
    try {
      const data = await window.ApiService.getFeatureImportance();
      const topFeatures = data.ranked_features.slice(0, 8);

      this.featContainer.innerHTML = '';
      topFeatures.forEach((item, idx) => {
        const row = document.createElement('div');
        row.style.marginBottom = '12px';

        const label = item.feature.replace(/_/g, ' ').toUpperCase();
        const percent = (item.composite_score * 100).toFixed(1);

        row.innerHTML = `
          <div style="display:flex;justify-content:space-between;font-size:0.8rem;font-weight:600;margin-bottom:4px">
            <span><strong style="color:var(--primary)">#${idx + 1}</strong> ${label}</span>
            <span style="font-family:var(--font-mono)">${item.composite_score.toFixed(3)} (${percent}%)</span>
          </div>
          <div class="prob-track">
            <div class="prob-fill" style="width:${percent}%;background:linear-gradient(90deg, var(--primary), var(--accent-cyan))"></div>
          </div>
        `;
        this.featContainer.appendChild(row);
      });
    } catch (err) {
      this.featContainer.innerHTML = `<div style="color:var(--text-muted)">Unable to load feature importance: ${err.message}</div>`;
    }
  }

  async loadModelBenchmarks() {
    if (!this.modelTableBody) return;
    try {
      const info = await window.ApiService.getModelInfo();
      const benchmarks = info.metrics.models_benchmark;
      const bestModel = info.metrics.best_model_name;

      this.modelTableBody.innerHTML = '';
      for (const [name, metrics] of Object.entries(benchmarks)) {
        const tr = document.createElement('tr');
        const isBest = name === bestModel;

        tr.innerHTML = `
          <td>
            <strong>${name}</strong>
            ${isBest ? '<span class="badge" style="margin-left:6px;background:rgba(16,185,129,0.15);color:var(--safe-green);padding:2px 6px;border-radius:4px;font-size:0.7rem">BEST MODEL</span>' : ''}
          </td>
          <td style="font-family:var(--font-mono)">${(metrics.accuracy * 100).toFixed(2)}%</td>
          <td style="font-family:var(--font-mono)">${(metrics.f1_weighted * 100).toFixed(2)}%</td>
          <td style="font-family:var(--font-mono)">${(metrics.roc_auc_weighted * 100).toFixed(2)}%</td>
          <td style="font-family:var(--font-mono)">${metrics.cv_f1_mean.toFixed(4)} ± ${metrics.cv_f1_std.toFixed(4)}</td>
        `;

        if (isBest) {
          tr.style.background = 'rgba(99, 102, 241, 0.08)';
        }

        this.modelTableBody.appendChild(tr);
      }
    } catch (err) {
      this.modelTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--text-muted)">Unable to load benchmark data: ${err.message}</td></tr>`;
    }
  }

  initChartClick() {
    const chartCards = document.querySelectorAll('.chart-img-container');
    chartCards.forEach(container => {
      container.addEventListener('click', () => {
        const img = container.querySelector('.chart-img');
        const title = container.dataset.title || 'Visual Analytics Inspection Chart';
        if (img && this.lightboxModal && this.lightboxImg) {
          this.lightboxImg.src = img.src;
          if (this.lightboxTitle) this.lightboxTitle.textContent = title;
          this.lightboxModal.classList.add('open');
        }
      });
    });
  }
}

window.AnalyticsController = AnalyticsController;
