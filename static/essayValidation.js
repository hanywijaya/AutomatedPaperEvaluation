var essaySubmitButton = document.querySelector('.essay-submit-button');
var essay = document.getElementById("essayInput")

checkEssay();

// alert("hey");

function checkEssay(){
    if(essay.value === ''){
        // alert("none");
        essaySubmitButton.disabled=true;
        essaySubmitButton.style.backgroundColor="gray";
    }
    else{
        // alert("have");
        essaySubmitButton.disabled=false;
        essaySubmitButton.style.backgroundColor="#000938";
    }
}

function essayFormValidation(e){
    e.preventDefault();

    var flag = 0;

    //validate all fields not empty
    if(essay.value === '' ){
        flag = 1;
    }
    else alert(essay.value);

    if(flag==1){
        alert("hey");
        return false;
    }
    else{
        var essayForm = document.getElementById('essayForm');
        essayForm.submit();
    }
}