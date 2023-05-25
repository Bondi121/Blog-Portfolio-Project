const username = document.getElementById("username_login");
const form = document.getElementById("form_login")

// when user login, the username is gotten from the username field. 
// The function below help to check if the user is register in our database. 
function loginFunction(username) {
    if (username === undefined) {
        return undefined
    }
    else {
        // The fetch actually sent a request to the check_user route in line 202, if the user is found, it return a 200 status code, otherwise 404 for not found user. 
        fetch ("http://127.0.0.1:5000/check_user/" + username, {
            method: "GET",
            headers:{'content-type': 'application/json'},
            mode: 'no-cors'
        })
        .then(function (response) {
            // This part is a promise that check the return of the fetch content if it is 200 or 404
            if (response.status === 200) {
                // if the response status code is 200, set the username to localstorage, and redirect to homepage
                localStorage.setItem ("username", username)
                window.location.replace("http://127.0.0.1:5000/homepage")
            } else {
                // if the status is 404, redirect the user to not_found page telling the user their username is not found 
                window.location.replace("http://127.0.0.1:5000/not_found")
            }
        })
        return true
    }
};


// function isLogin() {
//     const user = localStorage.getItem("username")
//     if (user === null) {
//         return false 
//     } else {
//         return true
//     }
// }

form.addEventListener("submit", function(event) {
    loginFunction(username.value) // calling the loginFunction and pass the username from the login page
    event.preventDefault() // prevent default behaviour of the submit event 
})

