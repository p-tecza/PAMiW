var json_products;
var curr_json_products;

localStorage.setItem("logout_bool", "false");


function readJSON() {
    var rawFile = new XMLHttpRequest();
    var it = 0;

    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status == 0) {

                document.getElementById("av_products").innerHTML="";

                fetch('/fetch_json')
                    .then((response) => response.json())
                    .then((json) => {


                        for (var i = 0; i < json.length; i++) {

                            pr = json[i].product_name;
                            qt = json[i].quantity;
                            ct = json[i].category;
                            im = json[i].image;
                            document.getElementById("av_products").innerHTML += "<li>" + pr + " | amount: "
                                + qt + " | category: " + ct + " | image: "+im+"</li>";

                        }

                        console.log("druknij");
                        console.log(json.length + "<- dlugosc jsona");
                        json_products = json;
                        curr_json_products = json_products;
                        console.log("TU JEST JSON PROD: ");
                        console.log(json_products);
                        //productsArr=JSON.parse(json);

                        console.log(typeof (json));

                        for (x in json) {
                            console.log("ok: " + x);
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

function changeProductContentText() {
    var searchValText = document.getElementById("search_product").value;
    var searchValSelect = document.getElementById("select_product").value;

    if (searchValSelect == "any") searchValSelect = "";

    document.getElementById("av_products").innerHTML = "";

    var wysw = json_products.filter(x => x.product_name.includes(searchValText));
    wysw = wysw.filter(x => x.category.includes(searchValSelect));

    curr_json_products = wysw;

    console.log("WYSW = ");
    console.log(wysw);


    for (var i = 0; i < wysw.length; i++) {

        //console.log(single_prod);
        pr = wysw[i].product_name
        qt = wysw[i].quantity
        ct = wysw[i].category

        document.getElementById("av_products").innerHTML += "<li>" + pr + " | amount: "
            + qt + " | category: " + ct + "</li>";
    }

    /* for(var i=0;i<products_arr.length;i++){
        if((products_arr[i]).includes(searchVal)){
            document.getElementById("av_products").innerHTML+="<li>"+products_arr[i]+"</li>";
        }
    } */

}

function changeProductContentSelect() {
    var searchValText = document.getElementById("search_product").value;
    var searchValSelect = document.getElementById("select_product").value;
    if (searchValSelect == "any") searchValSelect = "";

    document.getElementById("av_products").innerHTML = "";

    var wysw = json_products.filter(x => x.product_name.includes(searchValText));
    wysw = wysw.filter(x => x.category.includes(searchValSelect));


    for (var i = 0; i < wysw.length; i++) {

        //console.log(single_prod);
        pr = wysw[i].product_name
        qt = wysw[i].quantity
        ct = wysw[i].category

        document.getElementById("av_products").innerHTML += "<li>" + pr + " | amount: "
            + qt + " | category: " + ct + "</li>";
    }

}

function ajaxFunc() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        document.getElementById("register_nav").style.display = "none";
        console.log("loginasync");
    }
    xhttp.open("GET", "login_form");
    xhttp.send();
}

function showUserContent() {
    console.log("dz");
    document.getElementById("dropdownUserContent").style.display = "block";
}

window.onclick = function (event) {
    if (!event.target.matches('#dropdownUserContent')) {
        if (!event.target.matches('#viewdropdown')) {
            console.log("oob");
            document.getElementById("dropdownUserContent").style.display = "none";
        }
    }
}

function logoutFunction() {
    document.getElementById("dropdownUserContent").style.display = "none";
    console.log("lgout");

    localStorage.setItem("logout_bool", "true");

    const logoutAjax = new XMLHttpRequest();

    logoutAjax.onload = function () {
        redirectSite = this.responseText;
        window.location.replace("http://" + redirectSite);
        document.getElementById("logout_success_info").innerHTML = "logout successful.";
        console.log(redirectSite);
        console.log("dzilam");
        logout_bool = true;
        window.glob = "test";

    }

    logoutAjax.open("GET", "logout");
    logoutAjax.send();

}


readJSON();


function set_output(text) {
    output = document.getElementById("sse_test")
  
    if (!output) {
      output = document.createElement("span")
      output.setAttribute("id", "sse_test")
      document.body.appendChild(output)
    }
  
    output.innerText = text
  }

es = new EventSource("/stream")
es.addEventListener("myevent", function (event) {
    console.log("EVENT SOURCE");
    set_output("entries: " + event.value)
}, false);
es.addEventListener("error", function (event) {
    set_output("Failed to connect to event stream. Is the server running?");
}, false);


async function subscribe() {

    var noVisitorsVar='0';
    //var currentVisitors=document.getElementById("sse_test").innerHTML;


    //console.log(currentVisitors);

    console.log("wys");

    const params = {
        noVisitors:noVisitorsVar
    };

    const options = {
        method: 'POST',
        body: JSON.stringify( params )  
    };


    let response = await fetch("/subscribe", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(params),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
        })
      });
  
    if (response.status == 502) {
      // Status 502 is a connection timeout error,
      // may happen when the connection was pending for too long,
      // and the remote server or a proxy closed it
      // let's reconnect
      await subscribe();
    } else if (response.status != 200) {
      // An error - let's show it
      set_output(response.statusText);
      // Reconnect in one second
      await new Promise(resolve => setTimeout(resolve, 3000));
      await subscribe();
    } else {
      // Get and show the message
      let message = await response.text();
      set_output(message + " entries");
      noVisitorsVar=message;
      // Call subscribe() again to get the next message
      await new Promise(resolve => setTimeout(resolve, 3000));
      await subscribe();
    }
  }
  subscribe();


/* checkUpdates = function() {
    xhr = new XMLHttpRequest(); 
    xhr.open("GET","/progress?task=142");
    xhr.onreadystatechange = e => { console.log(e); checkUpdates(); };
    xhr.ontimeout = checkUpdates();
    xhr.send();
    }
checkUpdates(); */



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