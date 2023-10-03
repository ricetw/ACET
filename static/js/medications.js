document.addEventListener("DOMContentLoaded", function() {
    // 列出藥物
    const medical_list = document.getElementById('medical-list');
    const mediacl_data_element = document.getElementById('medical-data');
    const medical_data = JSON.parse(mediacl_data_element.dataset.medical);

    function renderMedical(data){
        medical_list.innerHTML = '';
        data.forEach(medical => {
            const tr = document.createElement('tr');
            const medicalClass = medical['drug_class'] === 0 ? '注射' : medical['drug_class'] === 1 ? '口服' : medical['drug_class'] === 2 ? '外用' : '其他';
            tr.innerHTML = `
                <td class="col-1"><input type="checkbox" name="medical" value="${medical['id']}"></td>
                <td class="col-2">${medicalClass}</td>
                <td>${medical['name']}</td>
                <td class="col-1"><button class="detailbtn" data-id="${medical['id']}">詳細</button></td>
                <td class="col-1"><button class="editbtn" data-id="${medical['id']}">編輯</button></td>
                <td class="col-1"><button class="deletebtn" data-id="${medical['id']}">刪除</button></td>
            `;  
            medical_list.appendChild(tr);
        });
    }
    renderMedical(medical_data);

    // 搜尋藥物
    const medical_class = document.getElementById('medical-class');
    const medical_name_input = document.getElementById('medical-name');

    medical_class.addEventListener('change', function() {
        const select_class = document.getElementById('medical-class').value;
        const medical_name = document.getElementById('medical-name').value;
        const data = {
            "action": "search",
            "class": select_class,
            "name": medical_name
        };
        searchMedical(data);
    });

    medical_name_input.addEventListener('input', function() {
        const select_class = document.getElementById('medical-class').value;
        const medical_name = document.getElementById('medical-name').value;
        const data = {
            "action": "search",
            "class": select_class,
            "name": medical_name
        };
        searchMedical(data);
    });

    function searchMedical(data) {
        fetch('/web/medications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result['result'] === 0)
                renderMedical(result['data']);
            else{
                console.log(result['message']);
                alert('搜尋失敗');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('錯誤');
        });
    };

    // 新增藥物
    const addModal = document.getElementById('addModal');
    const addbtn = document.getElementById('add-medical');
    const closebtn = document.getElementsByClassName('add-close')[0];

    addbtn.addEventListener('click', function() {
        addModal.style.display = "block";
    });

    closebtn.addEventListener('click', function() {
        addModal.style.display = "none";
    });

    window.addEventListener('click', function(event) {  
        if (event.target == addModal)
            addModal.style.display = "none";
    });

    const addForm = document.getElementById('addForm');
    addForm.addEventListener('submit', function(event) {
        event.preventDefault();

        let add_medical_class = document.getElementById('add-medical-class').value;
        let add_medical_name = document.getElementById('add-medical-name').value;
        let add_medical_effect = document.getElementById('add-medical-effect').value;
        let add_medical_side_effect = document.getElementById('add-medical-side-effect').value;
        
        if (add_medical_class === 'injection')
            add_medical_class = 0;
        else if (add_medical_class === 'oral')
            add_medical_class = 1;
        else if (add_medical_class === 'external')
            add_medical_class = 2;
        else if (add_medical_class === 'other')
            add_medical_class = 3;

        const data = {
            "action": "add",
            'class': add_medical_class,
            'name': add_medical_name,
            'effect': add_medical_effect,
            'side_effect': add_medical_side_effect
        };

        fetch('/web/medications', {
            method: 'POST',
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
                alert('新增失敗！');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('錯誤');
        });
    });

    // 詳細資料
    const detailElement = document.getElementById('detail');
    function renderDetail(data){
        detailElement.innerHTML = '';
        const medical_data = data;
        const medicalClass = medical_data['drug_class'] === 0 ? '注射' : medical_data['drug_class'] === 1 ? '口服' : medical_data['drug_class'] === 2 ? '外用' : '其他';
        const row = document.createElement('tr');
        row.innerHTML = `
            <p>詳細資料</p>
            <p>藥物類別：${medicalClass}</p>
            <p>藥物名稱：${medical_data['name']}</p>
            <p>臨床用途：${medical_data['effect']}</p>
            <p>副作用：${medical_data['side_effect']}</p>
        `;
        detailElement.appendChild(row);
    };
    
    const detailModel = document.getElementById('detailModal');
    const closeDetailbtn = document.getElementsByClassName('detail-close')[0];

    medical_list.addEventListener('click', function(event) {
        if (event.target.className === 'detailbtn'){
            const medical_id = event.target.dataset.id;
            const data = {
                "action": "detail",
                "id": medical_id
            };
            fetch('/web/medications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                if (result['result'] === 0){
                    renderDetail(result['data']);
                    detailModel.style.display = "block";
                }
                else{
                    console.log(result['message']);
                    alert('搜尋失敗！');
                }
            })
            .catch(error => {
                console.log('Error:', error);
                alert('錯誤');
            });
        }
    });

    closeDetailbtn.addEventListener('click', function() {
        detailModel.style.display = "none";
    });

    window.addEventListener('click', function(event) {  
        if (event.target == detailModel)
            detailModel.style.display = "none";
    });

    // 編輯藥物
    const editModal = document.getElementById('editModal');
    const closeEditbtn = document.getElementsByClassName('edit-close')[0];

    medical_list.addEventListener('click', function(event) {
        if (event.target.className === 'editbtn'){
            const medical_id = event.target.dataset.id;
            const data = {
                "action": "detail",
                "id": medical_id
            };
            fetch('/web/medications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                if (result['result'] === 0) {
                    const medical_data = result['data'];
                    const medicalClass = medical_data['drug_class'] === 0 ? 'injection' : medical_data['drug_class'] === 1 ? 'oral' : medical_data['drug_class'] === 2 ? 'external' : 'other';
                    document.getElementById('edit-medical-id').value = medical_data['id'];
                    document.getElementById('edit-medical-class').value = medicalClass;
                    document.getElementById('edit-medical-name').value = medical_data['name'];
                    document.getElementById('edit-medical-effect').value = medical_data['effect'];
                    document.getElementById('edit-medical-side-effect').value = medical_data['side_effect'];
                    editModal.style.display = "block";
                }
                else {
                    console.log(result['message']);
                    alert('搜尋失敗！');
                }
            })
            .catch(error => {
                console.log('Error:', error);
                alert('錯誤');
            });
        }
    });

    closeEditbtn.addEventListener('click', function() {
        editModal.style.display = "none";
    });

    window.addEventListener('click', function(event) {  
        if (event.target == editModal)
            editModal.style.display = "none";
    });

    const editForm = document.getElementById('editForm');
    editForm.addEventListener('submit', function(event) {
        event.preventDefault();

        let edit_medical_class = document.getElementById('edit-medical-class').value;

        if (edit_medical_class === 'injection')
            edit_medical_class = 0;
        else if (edit_medical_class === 'oral')
            edit_medical_class = 1;
        else if (edit_medical_class === 'external')
            edit_medical_class = 2;
        else if (edit_medical_class === 'other')
            edit_medical_class = 3;

        const data = {
            "id": document.getElementById('edit-medical-id').value,
            'class': edit_medical_class,
            'name': document.getElementById('edit-medical-name').value,
            'effect': document.getElementById('edit-medical-effect').value,
            'side_effect': document.getElementById('edit-medical-side-effect').value
        };
        fetch('/web/medications', {
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
                alert('更新失敗');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('錯誤');
        });
    });

    // 刪除藥物
    const deletebtn = document.getElementById('delete-medical');
    deletebtn.addEventListener('click', function() {
        const selectCheckBoxes = document.querySelectorAll('input[name="medical"]:checked');
        const medical_ids = Array.from(selectCheckBoxes).map(checkbox => checkbox.value);
        data = {id: medical_ids};
        deleteMedical(data);
    });
    medical_list.addEventListener('click', function(event) {
        if (event.target.className === 'deletebtn'){
            const medical_id = event.target.dataset.id;
            data = {id: [medical_id]};
            deleteMedical(data);
        }
    });
    function deleteMedical(data){
        fetch('/web/medications', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result['result'] === 0)
                window.location.reload();
            else
            {
                console.log(result['message']);
                alert('刪除失敗！');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('錯誤');
        });
    }
});
