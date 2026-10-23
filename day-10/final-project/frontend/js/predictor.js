/**
 * Live Interactive Risk Predictor & Simulator Controller.
 * Smart Hygiene Risk Prediction System.
 */

class PredictorController {
  constructor() {
    this.form = document.getElementById('predictor-form');
    this.needle = document.getElementById('gauge-needle');
    this.scoreValEl = document.getElementById('gauge-score-value');
    this.riskBanner = document.getElementById('risk-banner');
    this.riskTitle = document.getElementById('risk-title');
    this.gradePill = document.getElementById('grade-pill');
    this.probSafe = document.getElementById('prob-safe');
    this.probWarn = document.getElementById('prob-warn');
    this.probDanger = document.getElementById('prob-danger');
    this.probSafeVal = document.getElementById('prob-safe-val');
    this.probWarnVal = document.getElementById('prob-warn-val');
    this.probDangerVal = document.getElementById('prob-danger-val');
    this.recsList = document.getElementById('recs-list');
    this.riskFactorsList = document.getElementById('risk-factors-list');

    this.initSliderSync();
    this.initPresets();
    this.initFormSubmit();
  }

  initSliderSync() {
    const sliders = document.querySelectorAll('.range-slider');
    sliders.forEach(slider => {
      const badgeId = slider.dataset.valueId;
      const badge = document.getElementById(badgeId);
      if (badge) {
        slider.addEventListener('input', () => {
          badge.textContent = slider.value + (slider.dataset.unit || '');
        });
      }
    });
  }

  initPresets() {
    const presetSafeBtn = document.getElementById('preset-safe');
    const presetWarnBtn = document.getElementById('preset-warn');
    const presetDangerBtn = document.getElementById('preset-danger');

    if (presetSafeBtn) {
      presetSafeBtn.addEventListener('click', () => {
        this.applyPreset({
          facility_type: 'Hospital Cafeteria',
          inspection_type: 'Routine',
          temperature_compliance_score: 97,
          sanitation_protocol_score: 96,
          water_potability_index: 99,
          ppe_handwashing_score: 95,
          pest_control_score: 98,
          food_handler_cert_ratio: 95,
          structural_maintenance_score: 92,
          waste_management_score: 94,
          cross_contamination_control: 97,
          historical_violation_count: 0,
          ambient_kitchen_temp: 23,
          relative_humidity: 48,
        });
        this.runPrediction();
        window.Toast?.show('Applied Preset: Grade A (Safe Facility)', 'success');
      });
    }

    if (presetWarnBtn) {
      presetWarnBtn.addEventListener('click', () => {
        this.applyPreset({
          facility_type: 'Restaurant',
          inspection_type: 'Follow-up',
          temperature_compliance_score: 72,
          sanitation_protocol_score: 68,
          water_potability_index: 82,
          ppe_handwashing_score: 70,
          pest_control_score: 66,
          food_handler_cert_ratio: 70,
          structural_maintenance_score: 74,
          waste_management_score: 72,
          cross_contamination_control: 70,
          historical_violation_count: 3,
          ambient_kitchen_temp: 31,
          relative_humidity: 68,
        });
        this.runPrediction();
        window.Toast?.show('Applied Preset: Grade B (Conditional Warning)', 'warning');
      });
    }

    if (presetDangerBtn) {
      presetDangerBtn.addEventListener('click', () => {
        this.applyPreset({
          facility_type: 'Fast Food',
          inspection_type: 'Complaint-driven',
          temperature_compliance_score: 35,
          sanitation_protocol_score: 32,
          water_potability_index: 55,
          ppe_handwashing_score: 28,
          pest_control_score: 20,
          food_handler_cert_ratio: 30,
          structural_maintenance_score: 40,
          waste_management_score: 32,
          cross_contamination_control: 25,
          historical_violation_count: 8,
          ambient_kitchen_temp: 38,
          relative_humidity: 88,
        });
        this.runPrediction();
        window.Toast?.show('Applied Preset: Grade C (Critical Hazard)', 'error');
      });
    }
  }

  applyPreset(values) {
    for (const [key, val] of Object.entries(values)) {
      const el = document.getElementById(`sim-${key}`);
      if (el) {
        el.value = val;
        const badgeId = el.dataset?.valueId;
        const badge = badgeId ? document.getElementById(badgeId) : null;
        if (badge) {
          badge.textContent = val + (el.dataset.unit || '');
        }
      }
    }
  }

  getFormData() {
    return {
      facility_type: document.getElementById('sim-facility_type').value,
      inspection_type: document.getElementById('sim-inspection_type').value,
      temperature_compliance_score: parseFloat(document.getElementById('sim-temperature_compliance_score').value),
      sanitation_protocol_score: parseFloat(document.getElementById('sim-sanitation_protocol_score').value),
      water_potability_index: parseFloat(document.getElementById('sim-water_potability_index').value),
      ppe_handwashing_score: parseFloat(document.getElementById('sim-ppe_handwashing_score').value),
      pest_control_score: parseFloat(document.getElementById('sim-pest_control_score').value),
      food_handler_cert_ratio: parseFloat(document.getElementById('sim-food_handler_cert_ratio').value),
      structural_maintenance_score: parseFloat(document.getElementById('sim-structural_maintenance_score').value),
      waste_management_score: parseFloat(document.getElementById('sim-waste_management_score').value),
      cross_contamination_control: parseFloat(document.getElementById('sim-cross_contamination_control').value),
      historical_violation_count: parseInt(document.getElementById('sim-historical_violation_count').value, 10),
      ambient_kitchen_temp: parseFloat(document.getElementById('sim-ambient_kitchen_temp').value),
      relative_humidity: parseFloat(document.getElementById('sim-relative_humidity').value),
    };
  }

  initFormSubmit() {
    if (this.form) {
      this.form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.runPrediction();
      });
    }
  }

  async runPrediction() {
    const data = this.getFormData();
    const btn = document.getElementById('btn-run-sim');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner"></span> Analyzing Inspection...`;
    }

    try {
      const res = await window.ApiService.predictRisk(data);
      this.renderPrediction(res);
      window.Toast?.show(`Prediction evaluated: ${res.predicted_risk_level}`, 'success');
    } catch (err) {
      window.Toast?.show(`Simulation Failed: ${err.message}`, 'error');
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = `⚡ Run AI Risk Assessment`;
      }
    }
  }

  renderPrediction(res) {
    const score = parseFloat(res.predicted_risk_score);
    this.scoreValEl.textContent = score.toFixed(1);

    // Needle rotation: map 0-100 score to -90deg to +90deg
    const angle = (score / 100) * 180 - 90;
    if (this.needle) {
      this.needle.style.transform = `rotate(${angle}deg)`;
    }

    // Risk Banner
    this.riskBanner.className = 'risk-level-banner';
    let bannerClass = 'low';
    if (res.predicted_risk_level === 'Medium Risk') bannerClass = 'medium';
    if (res.predicted_risk_level === 'High Risk') bannerClass = 'high';
    this.riskBanner.classList.add(bannerClass);

    this.riskTitle.textContent = `${res.predicted_risk_level}`;
    this.gradePill.textContent = res.hygiene_grade.split(' (')[0];

    // Probabilities
    const probs = res.class_probabilities || { 'Low Risk': 33, 'Medium Risk': 33, 'High Risk': 34 };
    const pLow = probs['Low Risk'] || 0;
    const pMed = probs['Medium Risk'] || 0;
    const pHigh = probs['High Risk'] || 0;

    if (this.probSafe) this.probSafe.style.width = `${pLow}%`;
    if (this.probWarn) this.probWarn.style.width = `${pMed}%`;
    if (this.probDanger) this.probDanger.style.width = `${pHigh}%`;

    if (this.probSafeVal) this.probSafeVal.textContent = `${pLow}%`;
    if (this.probWarnVal) this.probWarnVal.textContent = `${pMed}%`;
    if (this.probDangerVal) this.probDangerVal.textContent = `${pHigh}%`;

    // Key Risk Drivers
    if (this.riskFactorsList) {
      this.riskFactorsList.innerHTML = '';
      if (res.key_risk_drivers && res.key_risk_drivers.length > 0) {
        res.key_risk_drivers.forEach(driver => {
          const chip = document.createElement('div');
          chip.className = `btn-sm ${driver.severity === 'Critical' ? 'btn-danger' : ''}`;
          chip.style.display = 'inline-flex';
          chip.style.margin = '3px';
          chip.textContent = `${driver.feature}: ${driver.value} (${driver.impact})`;
          this.riskFactorsList.appendChild(chip);
        });
      } else {
        this.riskFactorsList.innerHTML = `<span style="font-size:0.82rem;color:var(--safe-green)">No critical risk anomalies identified across inspection indicators.</span>`;
      }
    }

    // Recommendations Checklist
    if (this.recsList) {
      this.recsList.innerHTML = '';
      if (res.recommendations && res.recommendations.length > 0) {
        res.recommendations.forEach(rec => {
          const item = document.createElement('div');
          let itemClass = 'routine';
          if (rec.startsWith('CRITICAL')) itemClass = 'critical';
          else if (rec.startsWith('URGENT') || rec.startsWith('PRIORITY')) itemClass = 'urgent';

          item.className = `rec-item ${itemClass}`;
          item.innerHTML = `<span>⚡</span> <span>${rec}</span>`;
          this.recsList.appendChild(item);
        });
      }
    }
  }
}

window.PredictorController = PredictorController;
