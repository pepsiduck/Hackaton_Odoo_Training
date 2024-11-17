let username = document.getElementById("username");
let long_username = document.getElementById("long_username");

username.addEventListener("input",function(){
    if(username.value.length >= 15){
        long_username.innerHTML = "<p>Username Too long</p>";
    } else {
        long_username.innerHTML = "";
    }
});

let passwords_message = document.getElementById("passwords_message");
let password = document.getElementById("password");
let password_again = document.getElementById("password_again");

password.addEventListener("input",function(){
    if(password.value !== password_again.value) {
        passwords_message.innerHTML = "<p>Mots de passe différents</p>";
    } else {
        passwords_message.innerHTML = "";
    }
});

password_again.addEventListener("input",function(){
    if(password.value !== password_again.value) {
        passwords_message.innerHTML = "<p>Mots de passe différents</p>";
    } else {
        passwords_message.innerHTML = "";
    }
});
