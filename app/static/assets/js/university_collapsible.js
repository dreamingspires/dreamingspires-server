function yesnoCheck() {
    if (document.getElementById('university_check').checked) {
        document.getElementById('div_university').style.display = 'block';
    } else {
        document.getElementById('div_university').style.display = 'none';
    }
}
yesnoCheck()
