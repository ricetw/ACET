document.addEventListener('DOMContentLoaded', function() {
    const dataElement = document.getElementById('data');
    const inputData = JSON.parse(dataElement.dataset.data);
    const dataList = document.getElementById('medical_records_list');

    function renderData(datas) {
        dataList.innerHTML = '';
        datas.forEach(data => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${data.id}</td>
                <td>${data.medical_record_number}</td>
                <td>${data.time}</td>
                <td>${data.doctor_id}</td>
                <td>${data.doctor}</td>
                <td>${data.cases}</td>
                <td>${data.medication}</td>
                <td>${data.hospitalization}</td>
                <td><button class="btn btn-primary" onclick="location.href='/web/medical_record/${data.medical_record_number}&${data.id}'">查看</button></td>
            `;
            dataList.appendChild(tr);
        });
    }
    renderData(inputData);
    
    const ms_id = document.getElementById('ms_id');
    const medical_record_number = document.getElementById('medical_record_number');

    ms_id.addEventListener('input', search);
    medical_record_number.addEventListener('input', search);

    function search() {
        const data = {
            ms_id: ms_id.value,
            medical_record_number: medical_record_number.value,
        };
        fetch('/web/medical_records', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(result => {
            if (result['result'] === 0) {
                renderData(result.data);
            }
            else {
                console.log(result['message']);
                alert('搜尋失敗');
            }
        })
        .catch(err => {
            console.log(err);
            alert('錯誤');
        });
    }
});