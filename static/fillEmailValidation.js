var fillEmailSubmitButton = document.querySelector('.fillemail-submit-button');
fillEmailSubmitButton.addEventListener("click", fillEmailFormValidation);

var email = document.getElementById("email")

function fillEmailFormValidation(e){
    e.preventDefault();

    var flag = 0;

    //validate all fields not empty
    if(email.value.length == 0 ){
        document.getElementById("msg-3").innerHTML = "This field is required!";
        flag = 1;
    }else{
         document.getElementById("msg-3").innerHTML = ""
    }

    if(flag==1){
        return false;
    }
    else{
        var fillEmailForm = document.getElementById('fillEmailForm');
        fillEmailForm.submit();
    }
}