function emailValidation(){

    email=document.getElementById("email").value;
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    res = re.test(email);
    
    if(!res){
        document.getElementById("email").style.backgroundColor="#FBB2B2";
    }

}

console.log("oo");