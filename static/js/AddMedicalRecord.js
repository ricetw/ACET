document.addEventListener('DOMContentLoaded', function() {
    const patientElement = document.getElementById('patient_data');
    const patientData = JSON.parse(patientElement.dataset.patient);
    document.getElementById('patient_id').value = patientData['medical_record_number'];
    document.getElementById('patient_name').value = patientData['name'];
    document.getElementById('patient_gender').value = patientData['gender'] === 1 ? '男' : '女';
    document.getElementById('patient_age').value = patientData['age'];
    document.getElementById('patient_birthday').value = patientData['birthday'];
    document.getElementById('patient_height').value = patientData['height'];
    document.getElementById('patient_weight').value = patientData['weight'];

    // 新增病例
    const today = document.getElementById('today_button');

    today.addEventListener('click', function() {
        const current = new Date();
        const year = current.getFullYear();
        const month = String(current.getMonth() + 1).padStart(2, '0');
        const date = String(current.getDate()).padStart(2, '0');
        const hour = String(current.getHours()).padStart(2, '0');
        const minute = String(current.getMinutes()).padStart(2, '0');

        document.getElementById('add_date').value = `${year}-${month}-${date}`;
        document.getElementById('add_time').value = `${hour}:${minute}`;
    });

    const addContentButton = document.getElementById('add_content_button');
    const contentInputs = document.getElementById('contentInputs');
    let contentCount = 1;

    addContentButton.addEventListener('click', function() {
        contentCount++;
        const newBr = document.createElement('br');
        contentInputs.appendChild(newBr);
        const newContentInput = document.createElement('input');
        newContentInput.type = 'text';
        newContentInput.id = `add_content_${contentCount}`;
        newContentInput.name = `add_content_${contentCount}`;
        contentInputs.appendChild(newContentInput);
    });

    const addMedicineButton = document.getElementById('add_medicine_button');
    const medicineInputs = document.getElementById('medicineInputs');
    let medicineCount = 1;

    addMedicineButton.addEventListener('click', function() {
        medicineCount++;
        const newBr = document.createElement('br');
        medicineInputs.appendChild(newBr);
        const newMedicineInput = document.createElement('input');
        newMedicineInput.type = 'text';
        newMedicineInput.id = `add_medicine_${medicineCount}`;
        newMedicineInput.name = `add_medicine_${medicineCount}`;
        medicineInputs.appendChild(newMedicineInput);
        document.getElementById(`add_medicine_${medicineCount}`).setAttribute('list', `medicineList_${medicineCount}`);
        const newMedicineList = document.createElement('datalist');
        newMedicineList.id = `medicineList_${medicineCount}`;
        medicineInputs.appendChild(newMedicineList);
        bindInputEventListeners(newMedicineInput);
    });

    
    bindInputEventListeners(document.getElementById(`add_medicine_1`));

    function bindInputEventListeners(medicineInput) {
        medicineInput.addEventListener('input', function() {
            const medicine = medicineInput.value.trim();
            if (medicine.length > 0) {
                console.log(medicine);
                console.log(document.getElementById('drug_class').value);
                data = {
                    "action": "search",
                    "name": medicine,
                    "class": document.getElementById('drug_class').value
                }
                fetch(`/web/medications`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data),
                })
                .then(response => response.json())
                .then(result => {
                    if (result['result'] == 0) {
                        console.log(medicineInput.id.split('_')[2]);
                        const medicineList = document.getElementById(`medicineList_${medicineInput.id.split('_')[2]}`);
                        console.log(medicineList);
                        medicineList.innerHTML = '';
                        result['data'].forEach(medicine => {
                            console.log(medicine.name);
                            const option = document.createElement('option');
                            option.value = medicine.name;
                            medicineList.appendChild(option);
                        });
                    }
                    else {
                        console.log(result['message']);
                        alert('查詢失敗');
                    }
                })
                .catch(error => {
                    console.log('Error:', error);
                    alert('錯誤');
                });
            }
        });
    }

    const hospitalizationCheckbox = document.getElementById('add_hospitalization');
    const hospitalizationInputs = document.getElementById('hospitalizatonInputs');

    hospitalizationCheckbox.addEventListener('change', function() {
        if (hospitalizationCheckbox.checked) 
            hospitalizationInputs.style.display = 'block';
        else 
            hospitalizationInputs.style.display = 'none';
    });

    addForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const contentList = [];
        for (let i = 1; i <= contentCount; i++) {
            const contentInput = document.getElementById(`add_content_${i}`);
            if (contentInput) {
                const contentValue = contentInput.value.trim();
                if (contentValue) 
                    contentList.push(contentValue);
            }
        }

        const medicineList = [];
        for (let i = 1; i <= medicineCount; i++) {
            const medicineInput = document.getElementById(`add_medicine_${i}`);
            if (medicineInput) {
                const medicineValue = medicineInput.value.trim();
                if (medicineValue) 
                    medicineList.push(medicineValue);
            }
        }
        console.log(contentList);
        console.log(medicineList);

        data = {
            "medical_record_number": patientData['medical_record_number'],
            "content": contentList,
            "medicine": medicineList,
            "notice": document.getElementById('add_notice').value,
            "hospitalization": hospitalizationCheckbox.checked,
            "doctorid": document.getElementById('add_doctor_id').value,
            "datetime": `${document.getElementById('add_date').value} ${document.getElementById('add_time').value}`,
            "ward": document.getElementById('add_room').value,
            "bed": document.getElementById('add_bed').value
        }
        console.log(data);

        fetch(`/web/medical_record/${patientData['medical_record_number']}/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result['result'] == 0)
                location.href = `/web/patient/${patientData['medical_record_number']}`;
                // console.log(result['message']);
            else {
                console.log(result['message']);
                alert('新增失敗');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('新增失敗');
        });
    });
});