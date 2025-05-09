---
layout: page
title: "sPESI Calculator for PTE"
date: 2024-01-01
hidden: true
---
The sPESI score is a simplified clinical prediction tool designed to assess the severity and prognosis of pulmonary embolism (PE). By evaluating specific risk factors, it helps clinicians identify patients at low or high risk of mortality, aiding in treatment planning and decision-making.

<div class="card">
    <div class="card-body">
        <form id="sPESIForm">
            <!-- sPESI Score Criteria -->
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="age">
                <label class="form-check-label" for="age">
                    Age > 80 years
                </label>
            </div><hr>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="cancer">
                <label class="form-check-label" for="cancer">
                    History of cancer
                </label>
            </div><hr>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="chronicCardiopulmonary">
                <label class="form-check-label" for="chronicCardiopulmonary">
                    Chronic cardiopulmonary disease
                </label>
            </div><hr>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="heartRate">
                <label class="form-check-label" for="heartRate">
                    Heart rate ≥ 110 bpm
                </label>
            </div><hr>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="sbp">
                <label class="form-check-label" for="sbp">
                    Systolic blood pressure < 100 mmHg
                </label>
            </div><hr>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="oxygen">
                <label class="form-check-label" for="oxygen">
                    Arterial oxygen saturation < 90%
                </label>
            </div><hr>
            <button type="button" class="btn btn-primary w-100" onclick="calculateSPESI()">Calculate sPESI Score
            </button><hr>
        </form>
        <div class="mt-4">
            <div id="resultCard" class="card text-center d-none">
                <div id="result" class="card-body fw-bold"></div>
            </div>
        </div>
    </div>
</div>

<script src="/assets/js/calculator.js"></script>
 
### Interpretation of SPESI Score

- **Score = 0**: Low risk (30-day mortality < 1%)
- **Score ≥ 1**: High risk (30-day mortality > 10%)

### Disclaimer
This tool is for informational purposes only and should not replace professional medical advice. Always consult a healthcare provider for diagnosis and treatment.