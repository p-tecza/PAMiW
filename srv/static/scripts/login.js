
if(localStorage.getItem("logout_bool")=="true"){
    localStorage.setItem("logout_bool","false");
    document.getElementById("logout_success_info").innerHTML="logout successful.";
}
