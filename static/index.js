const username = document.getElementById("username_login");
const identity = document.getElementById("identity");
const form = document.getElementById("form_login")


function loginFunction(username) {
    if (username === undefined) {
        return undefined
    }
    else {
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

function changeIdentity() {
    const login = isLogin(username.value)
    if (login === true) {
        identity.textContent = localStorage.getItem("username")
    } 
} 

form.addEventListener("submit", function(e) {
    console.log(username.value)
    loginFunction(username.value)
})



console.log('hello world')

// loginFunction(username.value);



