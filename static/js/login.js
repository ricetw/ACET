document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const data = {
            username: username,
            password: password
        };

        fetch("/web/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.result === 0)
                window.location.href = "/web/index";
            else
                resultDiv.innerHTML = `登入失敗！醫護號或密碼錯誤`;
        })
        .catch(error => {
            console.error("登入失敗：", error);
            resultDiv.innerHTML = "登入失敗，請重試。";
        });
    });
});
