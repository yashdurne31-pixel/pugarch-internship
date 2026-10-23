/**
 * Inspections Management Controller.
 * Smart Hygiene Risk Prediction System.
 */

class InspectionsController {
  constructor() {
    this.tableBody = document.getElementById('inspections-tbody');
    this.searchInput = document.getElementById('search-inspections');
    this.filterButtons = document.querySelectorAll('.filter-btn');
    this.currentFilter = 'All';
    this.searchQuery = '';

    // Modal elements
    this.newModal = document.getElementById('modal-new-inspection');
    this.reportModal = document.getElementById('modal-inspection-report');
    this.newForm = document.getElementById('form-new-inspection');
    this.facilitySelect = document.getElementById('new-facility-id');

    this.initEvents();
  }

  async init() {
    await this.loadFacilities();
    await this.loadInspections();
  }

  initEvents() {
    // Search input
    if (this.searchInput) {
      let timeout = null;
      this.searchInput.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          this.searchQuery = this.searchInput.value.trim();
          this.loadInspections();
        }, 300);
      });
    }

    // Risk filters
    this.filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        this.filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.currentFilter = btn.dataset.filter || 'All';
        this.loadInspections();
      });
    });

    // Record inspection button & modal triggers
    const openBtn = document.getElementById('btn-open-new-inspection');
    if (openBtn) {
      openBtn.addEventListener('click', () => this.openNewModal());
    }

    const closeBtns = document.querySelectorAll('.modal-close-trigger');
    closeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        if (this.newModal) this.newModal.classList.remove('open');
        if (this.reportModal) this.reportModal.classList.remove('open');
      });
    });

    // New Inspection Form submission
    if (this.newForm) {
      this.newForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.submitNewInspection();
      });
    }
  }

  async loadFacilities() {
    if (!this.facilitySelect) return;
    try {
      const facilities = await window.ApiService.getFacilities();
      this.facilitySelect.innerHTML = '<option value="">-- Choose Registered Facility --</option>';
      facilities.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f.id;
        opt.textContent = `${f.name} (${f.facility_type}) - ${f.license_number}`;
        this.facilitySelect.appendChild(opt);
      });
    } catch (err) {
      console.error('Failed to load facilities:', err);
    }
  }

  async loadInspections() {
    if (!this.tableBody) return;
    this.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:24px;color:var(--text-muted)">Loading verified inspection logs...</td></tr>`;

    try {
      const records = await window.ApiService.getInspections(this.currentFilter, this.searchQuery);
      this.renderTable(records);
    } catch (err) {
      this.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:24px;color:var(--hazard-red)">Error loading records: ${err.message}</td></tr>`;
    }
  }

  renderTable(records) {
    if (!records || records.length === 0) {
      this.tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:32px;color:var(--text-secondary)">No inspection records match the current filter.</td></tr>`;
      return;
    }

    this.tableBody.innerHTML = '';
    records.forEach(rec => {
      const tr = document.createElement('tr');

      let riskClass = 'low';
      if (rec.predicted_risk_level === 'Medium Risk') riskClass = 'medium';
      if (rec.predicted_risk_level === 'High Risk') riskClass = 'high';

      tr.innerHTML = `
        <td><strong>#${rec.id}</strong></td>
        <td>
          <div style="font-weight:600">${rec.facility_name || 'Commercial Facility'}</div>
          <div style="font-size:0.75rem;color:var(--text-secondary)">${rec.facility_type || ''} • ${rec.license_number || ''}</div>
        </td>
        <td>
          <span class="risk-tag ${riskClass}">
            <span style="font-size:8px">●</span> ${rec.predicted_risk_level}
          </span>
        </td>
        <td>
          <strong style="font-family:var(--font-mono);font-size:0.95rem">${rec.predicted_risk_score.toFixed(1)}</strong>
          <span style="font-size:0.75rem;color:var(--text-secondary)">/100</span>
        </td>
        <td>
          <div style="font-size:0.84rem">${rec.inspector_name}</div>
          <div style="font-size:0.75rem;color:var(--text-secondary)">${rec.inspection_date} (${rec.inspection_type})</div>
        </td>
        <td>
          <span class="badge" style="font-size:0.76rem;background:rgba(255,255,255,0.06);padding:3px 8px;border-radius:4px">
            ${(rec.hygiene_grade || 'Grade A').split(' (')[0]}
          </span>
        </td>
        <td>
          <div class="action-btn-group">
            <button class="btn-sm btn-view-report" data-id="${rec.id}">Details</button>
            <button class="btn-sm btn-danger btn-delete-insp" data-id="${rec.id}">Delete</button>
          </div>
        </td>
      `;

      // Event listeners for actions
      tr.querySelector('.btn-view-report').addEventListener('click', () => this.viewReport(rec.id));
      tr.querySelector('.btn-delete-insp').addEventListener('click', () => this.deleteInspection(rec.id));

      this.tableBody.appendChild(tr);
    });
  }

  openNewModal() {
    if (this.newModal) {
      this.newModal.classList.add('open');
      const today = new Date().toISOString().split('T')[0];
      const dateInput = document.getElementById('new-inspection-date');
      if (dateInput) dateInput.value = today;
    }
  }

  async submitNewInspection() {
    const fId = parseInt(this.facilitySelect.value, 10);
    if (!fId) {
      window.Toast?.show('Please select a facility.', 'warning');
      return;
    }

    const payload = {
      facility_id: fId,
      facility_type: "Restaurant", // will be populated from facility in backend
      inspector_name: document.getElementById('new-inspector-name').value.trim() || 'Inspector',
      inspection_date: document.getElementById('new-inspection-date').value,
      inspection_type: document.getElementById('new-inspection-type').value,
      temperature_compliance_score: parseFloat(document.getElementById('new-temp').value),
      sanitation_protocol_score: parseFloat(document.getElementById('new-sanit').value),
      water_potability_index: parseFloat(document.getElementById('new-water').value),
      ppe_handwashing_score: parseFloat(document.getElementById('new-ppe').value),
      pest_control_score: parseFloat(document.getElementById('new-pest').value),
      food_handler_cert_ratio: parseFloat(document.getElementById('new-cert').value),
      structural_maintenance_score: parseFloat(document.getElementById('new-struct').value),
      waste_management_score: parseFloat(document.getElementById('new-waste').value),
      cross_contamination_control: parseFloat(document.getElementById('new-cross').value),
      historical_violation_count: parseInt(document.getElementById('new-violation').value, 10),
      ambient_kitchen_temp: parseFloat(document.getElementById('new-amb-temp').value),
      relative_humidity: parseFloat(document.getElementById('new-amb-hum').value),
      notes: document.getElementById('new-notes').value.trim(),
    };

    const submitBtn = document.getElementById('btn-submit-inspection');
    if (submitBtn) submitBtn.disabled = true;

    try {
      const created = await window.ApiService.createInspection(payload);
      window.Toast?.show(`Inspection #${created.id} saved with ${created.predicted_risk_level}`, 'success');
      if (this.newModal) this.newModal.classList.remove('open');
      this.newForm.reset();
      await this.loadInspections();
      if (window.AnalyticsControllerInstance) {
        window.AnalyticsControllerInstance.loadStats();
      }
    } catch (err) {
      window.Toast?.show(`Failed to save inspection: ${err.message}`, 'error');
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  }

  async viewReport(id) {
    try {
      const rec = await window.ApiService.getInspectionById(id);
      if (!this.reportModal) return;

      const titleEl = document.getElementById('modal-report-title');
      const contentEl = document.getElementById('modal-report-content');

      if (titleEl) titleEl.textContent = `Inspection Report #${rec.id} - ${rec.facility_name}`;

      let recsHtml = '';
      if (rec.recommendations && rec.recommendations.length > 0) {
        recsHtml = rec.recommendations.map(r => `
          <div class="rec-item ${r.includes('CRITICAL') ? 'critical' : r.includes('URGENT') ? 'urgent' : 'routine'}">
            <span>●</span> <span>${r}</span>
          </div>
        `).join('');
      } else {
        recsHtml = `<div style="color:var(--safe-green)">No remediation notices issued.</div>`;
      }

      contentEl.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;background:rgba(255,255,255,0.03);padding:14px;border-radius:var(--radius-md)">
          <div>
            <div style="font-size:0.8rem;color:var(--text-secondary)">Verified Grade</div>
            <div style="font-family:var(--font-heading);font-size:1.4rem;font-weight:800;color:var(--primary)">${rec.hygiene_grade}</div>
          </div>
          <div style="text-align:right">
            <div style="font-size:0.8rem;color:var(--text-secondary)">Predicted Risk Score</div>
            <div style="font-family:var(--font-mono);font-size:1.6rem;font-weight:800">${rec.predicted_risk_score.toFixed(1)} / 100</div>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:0.85rem;margin-bottom:16px">
          <div><strong>Inspector:</strong> ${rec.inspector_name}</div>
          <div><strong>Inspection Date:</strong> ${rec.inspection_date}</div>
          <div><strong>Type:</strong> ${rec.inspection_type}</div>
          <div><strong>Confidence:</strong> ${rec.confidence_percentage}%</div>
          <div><strong>Temp Compliance:</strong> ${rec.temperature_compliance_score}%</div>
          <div><strong>Sanitation Protocol:</strong> ${rec.sanitation_protocol_score}%</div>
          <div><strong>Pest Audit:</strong> ${rec.pest_control_score}%</div>
          <div><strong>Water Potability:</strong> ${rec.water_potability_index}%</div>
          <div><strong>Prior Violations:</strong> ${rec.historical_violation_count}</div>
          <div><strong>Kitchen Ambient:</strong> ${rec.ambient_kitchen_temp}°C | ${rec.relative_humidity}% RH</div>
        </div>

        <div style="margin-top:14px">
          <div class="recs-heading">Actionable Remediation Notice:</div>
          ${recsHtml}
        </div>

        ${rec.notes ? `<div style="margin-top:14px;font-size:0.82rem;color:var(--text-secondary);background:rgba(0,0,0,0.2);padding:10px;border-radius:var(--radius-sm)"><strong>Inspector Notes:</strong> ${rec.notes}</div>` : ''}
      `;

      this.reportModal.classList.add('open');
    } catch (err) {
      window.Toast?.show(`Failed to fetch report: ${err.message}`, 'error');
    }
  }

  async deleteInspection(id) {
    if (!confirm(`Are you sure you want to delete inspection log #${id}?`)) return;

    try {
      await window.ApiService.deleteInspection(id);
      window.Toast?.show(`Inspection #${id} deleted.`, 'success');
      await this.loadInspections();
      if (window.AnalyticsControllerInstance) {
        window.AnalyticsControllerInstance.loadStats();
      }
    } catch (err) {
      window.Toast?.show(`Delete failed: ${err.message}`, 'error');
    }
  }
}

window.InspectionsController = InspectionsController;
