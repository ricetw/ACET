document.addEventListener('DOMContentLoaded', function () {
    const wardBedList = document.getElementById('wardBedList');
    const dataElement = document.getElementById('data');
    const data = JSON.parse(dataElement.dataset.data);
    console.log(data);

    function render(datas) {
        wardBedList.innerHTML = '';
        datas.forEach(data => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${data.medical_record_id}</td>
                <td>${data.medical_record_number}</td>
                <td>${data.name}</td>
                <td>${data.ward_id}</td>
                <td>${data.bed_number}</td>
                <td>${data.time}</td>
             `;
            wardBedList.appendChild(tr);
        });
    }
    render(data)

    const medical_recode_number = document.getElementById('medical_recode_number');

    function search() {
        const data = {
            medical_recode_number: medical_recode_number.value,
        };
        fetch('/web/ward', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(result => {
            if (result['result'] === 0) {
                render(result.data);
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

    medical_recode_number.addEventListener('input', search);
});