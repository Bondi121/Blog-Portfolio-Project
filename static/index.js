const identity = document.getElementById("identity");


/*
function changeIdentity() {
    const login = isLogin(username.value)
    if (login === true) {
        identity.value = localStorage.getItem("username")
    } 
} */


function changeIdentity() {
    identity.textContent = localStorage.getItem("username")
} 

changeIdentity();
// loginFunction(username.value);



