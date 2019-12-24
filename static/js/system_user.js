$(document).ready(function () {
    adduser = document.getElementById('add-user-btn')
    adduserquit = document.getElementById('add-user-quit')
    addacount = document.getElementById('add-user-div')

    adduser.addEventListener("click", function () {
        addacount.style.display = "block"
    }, false)

    adduserquit.addEventListener("click", function () {
        addacount.style.display = "none"
    }, false)
})