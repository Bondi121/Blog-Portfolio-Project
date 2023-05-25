const username = document.getElementById("username");

if (localStorage.getItem("username")) {
    // The if condition part of the code will check if the username is stored in the localstorage, if stored, it will update the username.value with the localstorage value 
    username.value = localStorage.getItem("username")
}

