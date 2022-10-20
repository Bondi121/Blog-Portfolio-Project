const username = document.getElementById("username_login");
const submitButton = document.getElementById("submit_button");

function loginFunction(username) {
    if (username === undefined) {
        return undefined
    }
    else {
        localStorage.setItem ("username", username)
        return true
    }
};

