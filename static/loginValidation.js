var loginSubmitButton = document.querySelector('.login-submit-button');
loginSubmitButton.addEventListener("click", loginFormValidation);

var username = document.getElementById("username")
var password = document.getElementById("password")

function loginFormValidation(e){
    e.preventDefault();

    var flag = 0;

    //validate all fields not empty
    if(username.value.length == 0){
        document.getElementById("msg-1").innerHTML = "This field is required!";
        flag = 1;
    }else{
        document.getElementById("msg-1").innerHTML = ""
    }

    if(password.value.length == 0 ){
        document.getElementById("msg-2").innerHTML = "This field is required!";
        flag = 1;
    }else{  
        //validate password length > 8 characters
        if(password.value.length < 8){
            document.getElementById("msg-2").innerHTML = "Password must have more than 8 characters!";
            flag = 1;
        }else{
            document.getElementById("msg-2").innerHTML = ""
        }  
    }

    if(flag==1){
        return false;
    }
    else{
        var loginForm = document.getElementById('loginForm');
        loginForm.submit();
    }
}

