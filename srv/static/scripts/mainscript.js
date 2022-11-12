var json_products;
var curr_json_products;

localStorage.setItem("logout_bool","false");


        function readTextFile(file)
        {
            var rawFile = new XMLHttpRequest();
            var it=0;

            rawFile.onreadystatechange = function ()
            {
                if(rawFile.readyState === 4)
                {
                    if(rawFile.status === 200 || rawFile.status == 0)
                    {

                        fetch('/fetch_json')
                        .then((response) => response.json())
                        .then((json) => {


                            for(var i=0 ; i<json.length;i++){

                                pr=json[i].product_name
                                qt=json[i].quantity
                                ct=json[i].category
                                document.getElementById("av_products").innerHTML+="<li>"+pr+ " | amount: "
                                +qt+" | category: "+ct+"</li>";

                            }

                        console.log("druknij");
                        console.log(json.length+"<- dlugosc jsona");
                        json_products = json;
                        curr_json_products=json_products;
                        console.log("TU JEST JSON PROD: ");
                        console.log(json_products);
                        //productsArr=JSON.parse(json);
        
                        console.log(typeof(json));

                        for(x in json){
                        console.log("ok: "+x);
                        }
        
        });




                       /*  var allText = rawFile.responseText;
                        var pr="";
                        for(var x=0;x<allText.length;x++){

                            if(allText.charAt(x)=='\n'){
                                products_arr[it]=pr;
                                document.getElementById("av_products").innerHTML+="<li>"+pr+"</li>";
                                pr="";
                                it++;
                                continue;
                            }
                            var pr=pr+allText.charAt(x);     
                        }
                        products_arr[it]=pr;
                        document.getElementById("av_products").innerHTML+="<li>"+pr+"</li>";
                        console.log(products_arr);
                        //alert(allText); */
                    }
                }
            }
            rawFile.open("GET", "fetch_json");
            rawFile.send();
        }

        function changeProductContentText(){
            var searchValText=document.getElementById("search_product").value;
            var searchValSelect=document.getElementById("select_product").value;

            if(searchValSelect=="any") searchValSelect="";

            document.getElementById("av_products").innerHTML="";

            var wysw=json_products.filter(x => x.product_name.includes(searchValText));
            wysw=wysw.filter(x => x.category.includes(searchValSelect));

            curr_json_products=wysw;

            console.log("WYSW = ");
            console.log(wysw);


            for(var i=0;i<wysw.length;i++){

                //console.log(single_prod);
                pr=wysw[i].product_name
                qt=wysw[i].quantity
                ct=wysw[i].category

                document.getElementById("av_products").innerHTML+="<li>"+pr+ " | amount: "
                +qt+" | category: "+ct+"</li>";
            }

            /* for(var i=0;i<products_arr.length;i++){
                if((products_arr[i]).includes(searchVal)){
                    document.getElementById("av_products").innerHTML+="<li>"+products_arr[i]+"</li>";
                }
            } */

        }

        function changeProductContentSelect(){
            var searchValText=document.getElementById("search_product").value;
            var searchValSelect=document.getElementById("select_product").value;
            if(searchValSelect=="any") searchValSelect="";

            document.getElementById("av_products").innerHTML="";

            var wysw=json_products.filter(x => x.product_name.includes(searchValText));
            wysw=wysw.filter(x => x.category.includes(searchValSelect));

        
            for(var i=0;i<wysw.length;i++){

                //console.log(single_prod);
                pr=wysw[i].product_name
                qt=wysw[i].quantity
                ct=wysw[i].category

                document.getElementById("av_products").innerHTML+="<li>"+pr+ " | amount: "
                +qt+" | category: "+ct+"</li>";
            }
            
        }

        function ajaxFunc(){
            const xhttp = new XMLHttpRequest();
            xhttp.onload = function() {
            document.getElementById("register_nav").style.display="none";
            console.log("loginasync");
        }
        xhttp.open("GET", "login_form");
        xhttp.send();
        }

        function showUserContent(){
            console.log("dz");
            document.getElementById("dropdownUserContent").style.display = "block";
        }

        window.onclick = function(event) {
            if (!event.target.matches('#dropdownUserContent')) {
                if(!event.target.matches('#viewdropdown')){
                    console.log("oob");
                    document.getElementById("dropdownUserContent").style.display = "none";
                }
            }
        }

        function logoutFunction(){
            document.getElementById("dropdownUserContent").style.display = "none";
            console.log("lgout");

            localStorage.setItem("logout_bool","true");

            const logoutAjax = new XMLHttpRequest();

            logoutAjax.onload=function(){
                redirectSite=this.responseText;
                window.location.replace("http://"+redirectSite);
                document.getElementById("logout_success_info").innerHTML="logout successful.";
                console.log(redirectSite);
                console.log("dzilam");
                logout_bool=true;
                window.glob="test";

            }

            logoutAjax.open("GET", "logout");
            logoutAjax.send();

        }


        readTextFile("products.txt");

    /* var data = fetch('/fetch_json')
        .then((response) => response.json())
        .then((json) => {


            console.log("TEST");

            //console.log(json["product_name"]);

            //productsArr=JSON.parse(json);
        
            console.log(typeof(json));

            for(x in json["product_name"]){
                console.log("ok: "+x);
            }
        
        }); */