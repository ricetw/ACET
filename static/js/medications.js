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
        if (event.target == addModal) {
            addModal.style.display = "none";
        }
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
        console.log(data);

        fetch('/web/medications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            if (result['result'] === 0)
            {
                console.log(result['message']);
                window.location.reload();
            }
            else
            {
                console.log(result['message']);
                alert('新增失敗！');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('錯誤');
        });
    });
});