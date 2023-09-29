document.addEventListener("DOMContentLoaded", function () {
    // 頁面載入，顯示人員列表
    const personnel_list = document.getElementById("personnel_list");
    const personnelElement = document.getElementById("personnel-data");
    const personnel = JSON.parse(personnelElement.dataset.personnel);

    function renderPersonnel(data) {
        personnel_list.innerHTML = "";
        data.forEach(person => {
            const row = document.createElement("tr");
            const permissions = person.permissions === 1 ? "人事主管" : "護理師/醫生";
            row.innerHTML = `
                <td class="col-1"><input type="checkbox" name="person" value="${person.ms_id}"></td>
                <td class="col-2">${person.ms_id}</td>
                <td>${person.name}</td>
                <td class="col-3">${permissions}</td>
                <td class="col-1"><button class="detailButton" data-id="${person.ms_id}">詳細資料</button></td>
                <td class="col-1"><button class="editButton" data-id="${person.ms_id}">編輯</button></td>
                <td class="col-1"><button class="deleteButton" data-id="${person.ms_id}">删除</button></td>
            `;
            personnel_list.appendChild(row);
        });
    }
    renderPersonnel(personnel);

    // 詳細資料
    const detailElement = document.getElementById("detail");

    function renderDetail(data) {
        detailElement.innerHTML = "";
        const person = data;
        const permissions = person.permissions === 1 ? "人事主管" : "護理師/醫生";
        const row = document.createElement("tr");
        row.innerHTML = `
            <p>詳細資料</p>
            <p>醫護號: ${person.ms_id}</p>
            <p>姓名: ${person.name}</p>
            <p>職位: ${permissions}</p>
        `;
        detailElement.appendChild(row);
    }

    const detailModel = document.getElementById("detailModel");
    const closeDetailButton = document.getElementsByClassName("detail-close")[0];

    personnel_list.addEventListener("click", function (e) {
        if (e.target.classList.contains("detailButton")) {
            const personId = e.target.dataset.id;
            data = {
                action: "detail",
                ms_id: personId
            };
            fetch("/web/personnel", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.result === 0)
                {
                    renderDetail(result.data);
                    detailModel.style.display = "block";
                }
                else
                    alert("查詢失敗");
            })
        }
    });

    closeDetailButton.addEventListener("click", function () {
        detailModel.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == detailModel) {
            detailModel.style.display = "none";
        }
    });

    // 編輯人員
    const editmodal = document.getElementById("editModal");
    const closeEditButton = document.getElementsByClassName("edit-close")[0];

    personnel_list.addEventListener("click", function (e) {
        if (e.target.classList.contains("editButton")) {
            const personId = e.target.dataset.id;
            data = {
                action: "detail",
                ms_id: personId
            };
            fetch("/web/personnel", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.result === 0)
                {
                    document.getElementById("edit_ms_id").value = result.data.ms_id;
                    document.getElementById("edit_name").value = result.data.name;
                    document.getElementById("edit_permissions-select").value = result.data.permissions === 1 ? "supervisor" : "nurse";
                    editmodal.style.display = "block";
                }
                else
                    alert("查詢失敗");
            })
            .catch(error => {
                console.error("錯誤", error);
                alert("錯誤");
            });
        }
    });

    closeEditButton.addEventListener("click", function () {
        editmodal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == editmodal) {
            editmodal.style.display = "none";
        }
    });

    const editForm = document.getElementById("editForm");
    editForm.addEventListener("submit", function (e){
        e.preventDefault();

        let ms_id = document.getElementById("edit_ms_id").value;
        let name = document.getElementById("edit_name").value;
        let permissions_select = document.getElementById("edit_permissions-select").value;

        if (permissions_select === "supervisor")
            permissions_select = 1;
        else
            permissions_select = 2;

        const person_data = {
            ms_id: ms_id,
            name: name,
            permissions: permissions_select
        };
        fetch("/web/personnel", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(person_data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.result === 0)
                window.location.href = "/web/personnel";
            else
                alert("編輯失敗");
        })
        .catch(error => {
            console.error("錯誤", error);
            alert("錯誤");
        });
    });

    // 刪除人員
    personnel_list.addEventListener("click", function (e) {
        if (e.target.classList.contains("deleteButton")) {
            const personId = e.target.dataset.id;

            fetch("/web/personnel", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ms_id: [personId]})
            })
            .then(response => response.json())
            .then(result => {
                if (result.result === 0)
                    window.location.href = "/web/personnel";
                else
                    alert("刪除失敗");
            })
            .catch(error => {
                console.error("錯誤", error);
                alert("錯誤");
            });
        }
    });

    // 刪除選中人員
    const deletebtn = document.getElementById("deletebtn");
    deletebtn.addEventListener("click", function () {
        const selectedCheckboxes = document.querySelectorAll('input[name="person"]:checked');
        const selectedIds = Array.from(selectedCheckboxes).map(checkbox => checkbox.value);

        fetch("/web/personnel", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ms_id: selectedIds})
        })
        .then(response => response.json())
        .then(result => {
            if (result.result === 0)
                window.location.href = "/web/personnel";
            else
                alert("刪除失敗");
        })
        .catch(error => {
            console.error("錯誤", error);
            alert("錯誤");
        });
    });

    // 搜尋人員
    const search = document.getElementById("search");
    const searchbtn = document.getElementById("searchbtn");
    search.addEventListener("input", function (e) {
        const searchValue = e.target.value;

        data = {
            action: "search",
            ms_id: searchValue
        };

        fetch("/web/personnel", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.result === 0)
                renderPersonnel(result.data);
            else
                alert("查詢失敗");
        })
        .catch(error => {
            console.error("錯誤", error);
            alert("錯誤");
        });

    });
    
    // 新增人員視窗
    const addmodal = document.getElementById("addModal");
    const addPersonButton = document.getElementById("addPersonButton");
    const closeButton = document.getElementsByClassName("add-close")[0];

    addPersonButton.addEventListener("click", function () {
        addmodal.style.display = "block";
    });

    closeButton.addEventListener("click", function () {
        addmodal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == addmodal) {
            addmodal.style.display = "none";
        }
    });

    const personForm = document.getElementById("personForm");
    personForm.addEventListener("submit", function (e){
        e.preventDefault();

        let ms_id = document.getElementById("ms_id").value;
        let name = document.getElementById("name").value;
        let password = document.getElementById("password").value;
        let permissions_select = document.getElementById("permissions-select").value;

        if (permissions_select === "supervisor")
            permissions_select = 1;
        else
            permissions_select = 2;

        const person_data = {
            action: "add",
            ms_id: ms_id,
            name: name,
            password: password,
            permissions: permissions_select
        };

        fetch("/web/personnel", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(person_data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.result === 0)
                window.location.href = "/web/personnel";
            else
                alert("新增失敗");
        })
        .catch(error => {
            console.error("錯誤", error);
            alert("錯誤");
        });

        addmodal.style.display = "none";
        personForm.reset();
    })
});
