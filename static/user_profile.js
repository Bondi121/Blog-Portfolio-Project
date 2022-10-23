const user_update = document.getElementById("user_update");

function enableUpdate() {
    if (localStorage.getItem("username") === null) {
        user_update.style.display = "none"
    } else {
        user_update.href = "/update_user/" + localStorage.getItem("username")
    }
}

enableUpdate();