const user_update = document.getElementById("user_update");
const delete_user_button = document.getElementById("delete_user");

//  This function help to hide the update_user link if the user is not login in. If the user is logged in, the update_user will be display and attached to it will be the username stored in the localstorage 
function enableUpdate() {
    if (localStorage.getItem("username") === null) {
        user_update.style.display = "none"
    } else {
        user_update.href = "/update_user/" + localStorage.getItem("username")
    }
}

// Whenever user delete their account, their username is remove from localstorage
delete_user_button.addEventListener("click", function(){
    localStorage.removeItem("username")
}
) 


// calling the function above 
enableUpdate();
