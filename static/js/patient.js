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

    // 病人資料修改
    const modifyButton = document.getElementById('update_patient_data');

    modifyButton.addEventListener('click', updatePatientData);

    function updatePatientData() {
        data = {
            "height": document.getElementById('patient_height').value,
            "weight": document.getElementById('patient_weight').value
        }
        console.log(data);
        fetch(`/web/patient/${patientData["medical_record_number"]}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result['result'] == 0)
                location.reload();
            else {
                console.log(result['message']);
                alert('修改失敗');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('修改失敗');
        });
    }

    // 病例列表
    const medicalRecordsList = document.getElementById('medical_records_list');
    const medicalRecordsElement = document.getElementById('medical_records_data');
    const medicalRecordsData = JSON.parse(medicalRecordsElement.dataset.medicalRecords);

    function render(datas) {
        medicalRecordsList.innerHTML = '';
        datas.forEach(data => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="col-1">${data['id']}</td>
                <td class="col-1">${data['time']}</td>
                <td class="col-1">${data['doctorid']}</td>
                <td class="col-1">${data['doctor']}</td>
                <td>${data['cases']}</td>
                <td>${data['medication']}</td>
                <td>${data['notice']}</td>
                <td class="col-1">${data['hospitalization'] === true ? "是" : "否"}</td>
                <td class="col-1"><button class="btn btn-primary" onclick="location.href='/web/medical_record/${patientData['medical_record_number']}'">查看</button></td>
                <td class="col-1"><button class="btn btn-primary" onclick="location.href='/web/medical_record/${patientData['medical_record_number']}/edit'">修改</button></td>
            `;
            medicalRecordsList.appendChild(tr);
        });
    }
    render(medicalRecordsData);

    // 新增病例
    const addMedicalRecordButton = document.getElementById('add_medical_record');

    addMedicalRecordButton.addEventListener('click', function() {
        location.href = `/web/medical_record/${patientData['medical_record_number']}/add`;
    });
});