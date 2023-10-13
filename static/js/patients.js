document.addEventListener('DOMContentLoaded', function() {
    // 列出所有病人
    const patientList = document.getElementById('person_list');
    const patientElement = document.getElementById('patient-data');
    const patientData = JSON.parse(patientElement.dataset.patient);

    function render(datas) {
        patientList.innerHTML = '';
        datas.forEach(data => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${data['medical_record_number']}</td>
                <td>${data['name']}</td>
                <td>${data['gender']}</td>
                <td>${data['age']}</td>
                <td>${data['birthday']}</td>
                <td class="col-1"><button class="viewbtn btn-sm btn-outline-secondary" type="button" onclick="location.href='/web/patient/${data['medical_record_number']}'">查看</button></td>
                <td class="col-1"><button class="editbtn btn-sm btn-outline-secondary" data-id="${data["medical_record_number"]}">編輯</button></td>
            `;
            patientList.appendChild(tr);
        });
    }
    render(patientData);

    // 新增病人
    const addModal = document.getElementById('addModal');
    const addbtn = document.getElementById('addbtn');
    const closebtn = document.getElementsByClassName('add-close')[0];

    addbtn.addEventListener('click', function() {
        addModal.style.display = 'block';
    });

    closebtn.addEventListener('click', function() {
        addModal.style.display = 'none';
    });

    window.addEventListener('click', function(e) {
        if (e.target == addModal)
            addModal.style.display = 'none';
    });

    const addForm = document.getElementById('addForm');
    addForm.addEventListener('submit', function(e) {
        e.preventDefault();

        let health_id = document.getElementById('add_health_id').value;
        health_id = health_id.replace(/\s/g, '');
        const name = document.getElementById('add_name').value;
        let gender = document.getElementById('add_gender').value;
        const birthday = document.getElementById('add_birthday').value;
        const istwelevDigitNumber = /^\d{12}$/.test(health_id);

        if (!istwelevDigitNumber) {
            alert('健保卡號必須為12位數字');
            return;
        }

        const data = {
            "action": "add",
            "health_id": health_id,
            "name": name,
            "gender": gender,
            "birthday": birthday
        }
        console.log(data);
        fetch('/web/patient', {
            method: 'POST',
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
                alert('新增失敗');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('新增失敗');
        });
    });

    // 搜尋病人
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', function() {
        const searchValue = this.value;
        const data = {
            "action": "search",
            'medical_record_number': searchValue
        };
        fetch('/web/patient', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result['result'] == 0) 
                render(result['data']);
            else{
                console.log(result['message']);
                alert('搜尋失敗');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('搜尋失敗');
        });
    });

    // 編輯病人
    const editModal = document.getElementById('editModal');
    const closeEditbtn = document.getElementsByClassName('edit-close')[0];

    patientList.addEventListener('click', function(e) {
        if (e.target.className === 'editbtn btn-sm btn-outline-secondary') {
            const id = e.target.dataset.id;
            const data = {
                "action": "search",
                "medical_record_number": id
            };
            fetch('/web/patient', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                if (result['result'] === 0) {
                    const data = result['data'][0];
                    document.getElementById('edit_id').value = data['medical_record_number'];
                    document.getElementById('edit_health_id').value = data['health_id'];
                    document.getElementById('edit_name').value = data['name'];
                    document.getElementById('edit_gender').value = data['gender'] === '男' ? 1 : 0;
                    document.getElementById('edit_birthday').value = data['birthday'];
                    editModal.style.display = 'block';
                }
                else {
                    console.log(result['message']);
                    alert('取得資料失敗');
                }
            })
            .catch(error => {
                console.log('Error:', error);
                alert('編輯失敗');
            });
        }
    });

    closeEditbtn.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    window.addEventListener('click', function(e) {
        if (e.target == editModal)
            editModal.style.display = 'none';
    });

    const editForm = document.getElementById('editForm');
    editForm.addEventListener('submit', function(e) {
        e.preventDefault();

        let health_id = document.getElementById('edit_health_id').value;
        health_id = health_id.replace(/\s/g, '');
        const istwelevDigitNumber = /^\d{12}$/.test(health_id);

        if (!istwelevDigitNumber) {
            alert('健保卡號必須為12位數字');
            return;
        }

        const data = {
            "medical_record_number": document.getElementById('edit_id').value,
            "health_id": health_id,
            "name": document.getElementById('edit_name').value,
            "gender": document.getElementById('edit_gender').value,
            "birthday": document.getElementById('edit_birthday').value
        }
        fetch('/web/patient', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result['result'] === 0)
                window.location.reload();
            else{
                console.log(result['message']);
                alert("更新失敗")
            }
        })
        .catch(error => {
            console.log('Error: ', error)
            alert('錯誤');
        });
    });
});
