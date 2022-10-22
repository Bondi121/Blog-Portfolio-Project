const username = document.getElementById("username_login");
const form = document.getElementById("form_login")

function loginFunction(username) {
    if (username === undefined) {
        return undefined
    }
    else {
        fetch ()
        localStorage.setItem ("username", username)
        return true
    }
};

function isLogin() {
    const user = localStorage.getItem("username") 
    if (user === null) {
        return false 
    } else {
        return true
    }
}

form.addEventListener("submit", function() {
    loginFunction(username.value)
})

