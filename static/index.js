// This file is associated with the index.html

const identity = document.getElementById("identity");
const create_post = document.getElementById("create_post_id");
const profile_id = document.getElementById("profile_id");
const registration_id = document.getElementById("registration_id")
const login_id = document.getElementById("login_id")

// This function chenages teh identity of the button to either Anonymous or the user username if the user is login 
function changeIdentity() {
    if (localStorage.getItem("username")) {
        identity.textContent = localStorage.getItem("username")
    } else {
        identity.textContent = "Anonymous"
    }
} 

// This function help to hide the create_post link if the user is not login in
function enablePost() {
    if (localStorage.getItem("username") === null) {
        create_post.style.display = "none"
    }
}

// This function help to hide the profile link if the user is not login in. If the user is logged in, it will add the username to the profile for each different user
function enableProfile() {
    if (localStorage.getItem("username") === null) {
        profile_id.style.display = "none"
    } else {
        profile_id.href = "/profile/" + localStorage.getItem("username")
    }
}

// Help to hide the registration and login link if the user is logged. The two link wil not be displayed if the user is logged 
function disableLogin () {
    if (localStorage.getItem("username")) {
        registration_id.style.display = "none"
        login_id.style.display = "none"
    }
}


// Calling the function defined above. 
changeIdentity();
enablePost();
enableProfile()
disableLogin();
// loginFunction(username.value);

