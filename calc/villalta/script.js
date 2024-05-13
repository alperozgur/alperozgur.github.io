function calculateScore() {
    var pain = parseInt(document.getElementById('pain').value);
    var cramps = parseInt(document.getElementById('cramps').value);
    var swelling = parseInt(document.getElementById('swelling').value);
    var pigmentation = parseInt(document.getElementById('pigmentation').value);
    var ulcer = parseInt(document.getElementById('ulcer').value);

    var score = pain + cramps + swelling + pigmentation + ulcer;
    document.getElementById('score').textContent = score;
}
