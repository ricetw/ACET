document.addEventListener('DOMContentLoaded', function() {
    const dataElement = document.getElementById('data');
    const data = JSON.parse(dataElement.dataset.data);
    console.log(data);
    document.getElementById('patient_id').value = data['medical_record_number'];
    document.getElementById('patient_name').value = data['name'];
    document.getElementById('patient_gender').value = data['gender'] === 1 ? '男' : '女';
    document.getElementById('patient_age').value = data['age'];
    document.getElementById('patient_birthday').value = data['birthday'];
    document.getElementById('patient_height').value = data['height'];
    document.getElementById('patient_weight').value = data['weight'];
    document.getElementById('date').value = data['datetime'].split(' ')[0];
    document.getElementById('time').value = data['datetime'].split(' ')[1];
    document.getElementById('doctor_id').value = data['doctorid'];
    const contentInputs = document.getElementById('contentInputs');
    for (let i = 0; i < data['cases'].length; i++) {
        if (i > 0) {
            const newBr = document.createElement('br');
            contentInputs.appendChild(newBr);
        }
        const newContentInput = document.createElement('input');
        newContentInput.type = 'text';
        newContentInput.id = `add_content_${i}`;
        newContentInput.name = `add_content_${i}`;
        newContentInput.value = data['cases'][i];
        newContentInput.disabled = true;
        contentInputs.appendChild(newContentInput);
    }
    const medicineInputs = document.getElementById('medicineInputs');
    for (let i = 0; i < data['medication'].length; i++) {
        if (i > 0) {
            const newBr = document.createElement('br');
            medicineInputs.appendChild(newBr);
        }
        const newMedicineInput = document.createElement('input');
        newMedicineInput.type = 'text';
        newMedicineInput.id = `add_medicine_${i}`;
        newMedicineInput.name = `add_medicine_${i}`;
        newMedicineInput.value = data['medication'][i];
        newMedicineInput.disabled = true;
        medicineInputs.appendChild(newMedicineInput);
    }
    document.getElementById('notice').value = data['notice'];
    document.getElementById('hospitalization').value = data['hospitalization'] === true ? '是' : '否';
    const hospitalization = document.getElementById('hospitalization');
    const hospitalizationInputs = document.getElementById('hospitalizatonInputs');
    if (hospitalization.value === '是') {
        hospitalizationInputs.style.display = 'block';
        document.getElementById('room').value = data['ward'];
        document.getElementById('bed').value = data['bed'];
    } 
    else 
        hospitalizationInputs.style.display = 'none';
    const backbtn = document.getElementById('back')
    backbtn.addEventListener('click', function() {
        window.location.href = `/web/patient/${data['medical_record_number']}`;
    });
});