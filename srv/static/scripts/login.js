
//import { logout_bool } from "./mainscript.js";

if(localStorage.getItem("logout_bool")=="true"){
    localStorage.setItem("logout_bool","false");
    document.getElementById("logout_success_info").innerHTML="logout successful.";
}

/* if(logout_bool){
    document.getElementById("logout_success_info").innerHTML="logout successful.";
}
 */

/* $(document).ready(function(){

    $('.test').click(function(){

        $.ajax({
            url:'',
            type:'get',
            contentType:'application/json',
            data:{
                button_text: $(this).text()
            },
            success: function(response){
                $('.test').text(response.seconds)
            }
        })

    })

}) */