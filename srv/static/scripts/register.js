function emailValidation(){

    email=document.getElementById("email").value;
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    res = re.test(email);
    
    if(!res){
        document.getElementById("email").style.backgroundColor="#FBB2B2";
    }else{
        document.getElementById("email").style.backgroundColor="#FFFFFF";
    }

}

function checkData(){

    {
        let p=document.getElementById("register_pass").value;
        let rp=document.getElementById("register_r_pass").value;

        if(p!=rp){
            document.getElementById("register_r_pass").style.backgroundColor="#FBB2B2";
        }else{
            document.getElementById("register_r_pass").style.backgroundColor="#FFFFFF";
        }

    }

}

console.log("oo");