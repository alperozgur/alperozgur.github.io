function calculateWellsPTE() {
    // Wells score criteria for PE
    let score = 0;
    score += document.getElementById('dvtSymptoms').checked ? 3 : 0;
    score += document.getElementById('alternativeLessLikely').checked ? 3 : 0;
    score += document.getElementById('heartRate').checked ? 1.5 : 0;
    score += document.getElementById('immobilization').checked ? 1.5 : 0;
    score += document.getElementById('previousPEorDVT').checked ? 1.5 : 0;
    score += document.getElementById('hemoptysis').checked ? 1 : 0;
    score += document.getElementById('cancer').checked ? 1 : 0;

    // Get the result card and text
    let resultCard = document.getElementById('resultCard');
    let resultText = document.getElementById('result');

    // Display result based on Wells score for PE
    if (score > 4) {
        resultCard.classList.remove('d-none', 'bg-warning', 'bg-success');
        resultCard.classList.add('bg-danger');
        resultText.innerText = `Wells Score is ${score}. High probability of Pulmonary Embolism.`;
    } else {
        resultCard.classList.remove('d-none', 'bg-danger', 'bg-warning');
        resultCard.classList.add('bg-success');
        resultText.innerText = `Wells Score is ${score}. Low probability of Pulmonary Embolism.`;
    }
}

function calculateWellsDVT() {
    // Wells score criteria
    let score = 0;
    score += document.getElementById('cancer').checked ? 1 : 0;
    score += document.getElementById('paralysis').checked ? 1 : 0;
    score += document.getElementById('bedridden').checked ? 1 : 0;
    score += document.getElementById('tenderness').checked ? 1 : 0;
    score += document.getElementById('swelling').checked ? 1 : 0;
    score += document.getElementById('calfSwelling').checked ? 1 : 0;
    score += document.getElementById('pittingEdema').checked ? 1 : 0;
    score += document.getElementById('collateral').checked ? 1 : 0;
    score += document.getElementById('previousDVT').checked ? 1 : 0;
    score -= document.getElementById('alternativeDiagnosis').checked ? 2 : 0;

    // Get the result card and text
    let resultCard = document.getElementById('resultCard');
    let resultText = document.getElementById('result');

    // Display result based on Wells score
    if (score >= 3) {
        resultCard.classList.remove('d-none', 'bg-warning', 'bg-success');
        resultCard.classList.add('bg-danger');
        resultText.innerText = `Wells Score is ${score}. High probability of DVT.`;
    } else if (score >= 1) {
        resultCard.classList.remove('d-none', 'bg-danger', 'bg-success');
        resultCard.classList.add('bg-warning');
        resultText.innerText = `Wells Score is ${score}. Moderate probability of DVT.`;
    } else {
        resultCard.classList.remove('d-none', 'bg-danger', 'bg-warning');
        resultCard.classList.add('bg-success');
        resultText.innerText = `Wells Score is ${score}. Low probability of DVT.`;
    }
}
function calculateBMI() {
    // Get weight and height from the form
    let weight = parseFloat(document.getElementById('weight').value);
    let height = parseFloat(document.getElementById('height').value) / 100; // Convert cm to meters

    // Calculate BMI
    let bmi = weight / (height * height);

    // Get the result card and text
    let resultCard = document.getElementById('resultCard');
    let resultText = document.getElementById('result');

    // Display result based on BMI value
    if (bmi < 18.5) {
        resultCard.classList.remove('d-none', 'bg-warning', 'bg-success', 'bg-danger');
        resultCard.classList.add('bg-warning');
        resultText.innerText = `BMI is ${bmi.toFixed(1)}. You are underweight.`;
    } else if (bmi >= 18.5 && bmi < 24.9) {
        resultCard.classList.remove('d-none', 'bg-warning', 'bg-danger');
        resultCard.classList.add('bg-success');
        resultText.innerText = `BMI is ${bmi.toFixed(1)}. You are at a normal weight.`;
    } else if (bmi >= 24.9 && bmi < 29.9) {
        resultCard.classList.remove('d-none', 'bg-success', 'bg-danger');
        resultCard.classList.add('bg-warning');
        resultText.innerText = `BMI is ${bmi.toFixed(1)}. You are overweight.`;
    } else {
        resultCard.classList.remove('d-none', 'bg-warning', 'bg-success');
        resultCard.classList.add('bg-danger');
        resultText.innerText = `BMI is ${bmi.toFixed(1)}. You have obesity.`;
    }
}

function calculateSPESI() {
    // sPESI score criteria
    let score = 0;
    score += document.getElementById('age').checked ? 1 : 0;
    score += document.getElementById('cancer').checked ? 1 : 0;
    score += document.getElementById('chronicCardiopulmonary').checked ? 1 : 0;
    score += document.getElementById('heartRate').checked ? 1 : 0;
    score += document.getElementById('sbp').checked ? 1 : 0;
    score += document.getElementById('oxygen').checked ? 1 : 0;

    // Get the result card and text
    let resultCard = document.getElementById('resultCard');
    let resultText = document.getElementById('result');

    // Display result based on sPESI score
    if (score > 0) {
        resultCard.classList.remove('d-none', 'bg-success');
        resultCard.classList.add('bg-danger');
        resultText.innerText = `sPESI Score is ${score}. High risk for complications.`;
    } else {
        resultCard.classList.remove('d-none', 'bg-danger');
        resultCard.classList.add('bg-success');
        resultText.innerText = `sPESI Score is ${score}. Low risk for complications.`;
    }
}