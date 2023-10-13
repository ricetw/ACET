document.addEventListener("DOMContentLoaded", function () {
    const personnel = document.getElementById("personnel");
    const database = document.getElementById("database");
    const permissionsElement = document.getElementById("permissions");
    const permissions = permissionsElement.dataset.permissions;

    if (permissions === "2")
    {
        personnel.style.display = "none";
        database.style.display = "none";
    }
    else if (permissions === "1")
    {
        database.style.display = "none";
    }
    else if (permissions === "0")
    {
        personnel.style.display = "block";
        database.style.display = "block";
    }
});