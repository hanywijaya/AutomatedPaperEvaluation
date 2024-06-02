var registerSubmitButton = document.querySelector('.register-submit-button');
registerSubmitButton.addEventListener("click", registerFormValidation);

var username = document.getElementById("username")
var email = document.getElementById("email")
var password = document.getElementById("password")
var confpassword = document.getElementById("confpassword")

function registerFormValidation(e){
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

    if(email.value.length == 0 ){
        document.getElementById("msg-3").innerHTML = "This field is required!";
        flag = 1;
    }else{
         document.getElementById("msg-3").innerHTML = ""
    }

    if(confpassword.value.length == 0 ){
        document.getElementById("msg-4").innerHTML = "This field is required!";
        flag = 1;
    }else{
        if(password != confpassword){
            document.getElementById("msg-4").innerHTML = "Passwords don't match!";
        }
        else{
            document.getElementById("msg-4").innerHTML = ""
        }
    }

    if(flag==1){
        return false;
    }
    else{
        var registerForm = document.getElementById('registerForm');
        console.log(registerForm);
        registerForm.submit();
    }
}