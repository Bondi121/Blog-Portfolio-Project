const identity = document.getElementById("identity");
const create_post = document.getElementById("create_post_id");
const profile_id = document.getElementById("profile_id");

function changeIdentity() {
    if (localStorage.getItem("username")) {
        identity.textContent = localStorage.getItem("username")
    } else {
        identity.textContent = "Anonymous"
    }
} 

function enablePost() {
    if (localStorage.getItem("username") === null) {
        create_post.style.display = "none"
    }
}

function enableProfile() {
    if (localStorage.getItem("username") === null) {
        profile_id.style.display = "none"
    } else {
        profile_id.href = "/profile/" + localStorage.getItem("username")
    }
}



changeIdentity();
enablePost();
enableProfile()
// loginFunction(username.value);



