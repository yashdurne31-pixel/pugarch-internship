/**
 * Batch CSV Upload and High-Throughput Prediction Controller.
 * Smart Hygiene Risk Prediction System.
 */

class BatchController {
  constructor() {
    this.dropZone = document.getElementById('csv-drop-zone');
    this.fileInput = document.getElementById('csv-file-input');
    this.sampleBtn = document.getElementById('btn-load-sample-csv');
    this.tableBody = document.getElementById('batch-results-tbody');
    this.summaryBox = document.getElementById('batch-summary-box');
    this.exportBtn = document.getElementById('btn-export-batch');
    this.lastBatchResults = null;

    this.initEvents();
  }

  initEvents() {
    if (this.dropZone && this.fileInput) {
      this.dropZone.addEventListener('click', () => this.fileInput.click());

      this.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        this.dropZone.style.borderColor = 'var(--primary)';
        this.dropZone.style.background = 'rgba(99, 102, 241, 0.08)';
      });

      this.dropZone.addEventListener('dragleave', () => {
        this.dropZone.style.borderColor = 'var(--border-subtle)';
        this.dropZone.style.background = 'transparent';
      });

      this.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        this.dropZone.style.borderColor = 'var(--border-subtle)';
        this.dropZone.style.background = 'transparent';
        if (e.dataTransfer.files.length > 0) {
          this.processFile(e.dataTransfer.files[0]);
        }
      });

      this.fileInput.addEventListener('change', () => {
        if (this.fileInput.files.length > 0) {
          this.processFile(this.fileInput.files[0]);
        }
      });
    }

    if (this.sampleBtn) {
      this.sampleBtn.addEventListener('click', () => this.loadSampleCsv());
    }

    if (this.exportBtn) {
      this.exportBtn.addEventListener('click', () => this.exportCsv());
    }
  }

  async loadSampleCsv() {
    try {
      window.Toast?.show('Loading built-in sample inspections CSV...', 'info');
      let blob;
      try {
        const resp = await fetch('assets/sample_inspections.csv');
        if (resp.ok) {
          blob = await resp.blob();
        }
      } catch (_) {}

      if (!blob) {
        const sampleText = `facility_type,inspection_type,temperature_compliance_score,sanitation_protocol_score,water_potability_index,ppe_handwashing_score,pest_control_score,food_handler_cert_ratio,structural_maintenance_score,waste_management_score,cross_contamination_control,historical_violation_count,ambient_kitchen_temp,relative_humidity
Restaurant,Routine,96.5,94.0,98.0,92.5,95.0,90.0,88.0,92.0,95.0,0,24.0,50.0
Hospital Cafeteria,Routine,98.0,97.5,100.0,98.0,99.0,100.0,95.0,98.0,99.0,0,22.0,46.0
Fast Food,Complaint-driven,42.0,38.5,65.0,35.0,30.0,40.0,45.0,40.0,38.0,7,36.5,82.0
Bakery & Confectionery,Routine,82.0,79.0,90.0,80.0,76.0,82.0,84.0,85.0,80.0,1,26.0,60.0
Supermarket Deli,Routine,88.0,86.0,94.0,88.0,85.0,86.0,88.0,89.0,87.0,1,23.5,54.0
Catering Service,License Renewal,72.0,68.0,82.0,69.0,65.0,70.0,72.0,70.0,68.0,3,31.0,74.0
Restaurant,Follow-up,52.0,48.0,70.0,50.0,42.0,48.0,55.0,50.0,49.0,5,34.0,78.0
Hospital Cafeteria,Routine,94.0,93.0,96.0,92.0,94.0,95.0,91.0,94.0,95.0,0,23.0,48.0`;
        blob = new Blob([sampleText], { type: 'text/csv' });
      }

      const file = new File([blob], 'sample_inspections.csv', { type: 'text/csv' });
      await this.processFile(file);
    } catch (err) {
      window.Toast?.show(`Failed to load sample: ${err.message}`, 'error');
    }
  }

  async processFile(file) {
    if (!file.name.endsWith('.csv')) {
      window.Toast?.show('Please select a valid .csv file.', 'warning');
      return;
    }

    if (this.tableBody) {
      this.tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px;color:var(--text-muted)">Processing batch with ML inference models...</td></tr>`;
    }

    try {
      const data = await window.ApiService.uploadCsv(file);
      this.lastBatchResults = data.results;
      this.renderBatchResults(data);
      window.Toast?.show(`Batch processing complete! ${data.total_rows_evaluated} records scored.`, 'success');
      if (this.exportBtn) this.exportBtn.style.display = 'inline-flex';
    } catch (err) {
      window.Toast?.show(`Batch Upload Failed: ${err.message}`, 'error');
      if (this.tableBody) {
        this.tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:24px;color:var(--hazard-red)">Error: ${err.message}</td></tr>`;
      }
    }
  }

  renderBatchResults(data) {
    if (!this.tableBody) return;
    this.tableBody.innerHTML = '';

    let safeCount = 0;
    let warnCount = 0;
    let dangerCount = 0;

    data.results.forEach(row => {
      let riskClass = 'low';
      if (row.predicted_risk_level === 'Medium Risk') {
        riskClass = 'medium';
        warnCount++;
      } else if (row.predicted_risk_level === 'High Risk') {
        riskClass = 'high';
        dangerCount++;
      } else {
        safeCount++;
      }

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>#${row.row_index}</strong></td>
        <td>${row.facility_type}</td>
        <td>
          <span class="risk-tag ${riskClass}">
            <span style="font-size:8px">●</span> ${row.predicted_risk_level}
          </span>
        </td>
        <td style="font-family:var(--font-mono);font-weight:700">${row.predicted_risk_score.toFixed(1)}</td>
        <td><span class="badge" style="font-size:0.75rem">${row.hygiene_grade.split(' (')[0]}</span></td>
        <td style="font-size:0.8rem;color:var(--text-secondary)">${row.recommendations.join('; ') || 'Standard Monitoring'}</td>
      `;
      this.tableBody.appendChild(tr);
    });

    if (this.summaryBox) {
      this.summaryBox.style.display = 'block';
      this.summaryBox.innerHTML = `
        <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">
          <div><strong>Total Scored:</strong> ${data.total_rows_evaluated}</div>
          <div style="color:var(--safe-green)">● Safe (Grade A): ${safeCount}</div>
          <div style="color:var(--warning-amber)">● Warning (Grade B): ${warnCount}</div>
          <div style="color:var(--hazard-red)">● Hazard (Grade C): ${dangerCount}</div>
        </div>
      `;
    }
  }

  exportCsv() {
    if (!this.lastBatchResults || this.lastBatchResults.length === 0) return;

    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Row,Facility_Type,Predicted_Risk_Level,Risk_Score,Hygiene_Grade,Confidence,Top_Recommendation\n";

    this.lastBatchResults.forEach(r => {
      const topRec = (r.recommendations[0] || 'Standard Monitoring').replace(/,/g, ' ');
      csvContent += `${r.row_index},"${r.facility_type}","${r.predicted_risk_level}",${r.predicted_risk_score},"${r.hygiene_grade}",${r.confidence_percentage}%,"${topRec}"\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `hygiene_predictions_batch_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.Toast?.show('Batch results downloaded as CSV.', 'success');
  }
}

window.BatchController = BatchController;
