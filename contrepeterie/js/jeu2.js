function test(){
    let elem = document.getElementById('myH1');
    elem.parentNode.removeChild(elem);


    var br = document.createElement("BR");


    var divM = document.createElement("div");
    var divR = document.createElement("div");
    var divCT = document.createElement("div");
    var divCS = document.createElement("div");

    divR.appendChild(divCT);
    divR.appendChild(divCS);
    divM.appendChild(divR);

    var divT = document.createElement("DIV");
    var h = document.createTextNode("01 : 00");

    var divS = document.createElement("DIV");
    var s = document.createTextNode("Score : 00");

    divS.id='score';
    divT.id='timer';
    divM.id='menu';

    divT.appendChild(h);
    divS.appendChild(s);
    divCT.appendChild(divT);
    divCS.appendChild(divS);
    divM.appendChild(br);
    document.getElementById("myDIV").appendChild(divM);

    var btn1 = document.createElement("BUTTON");
    var t1 = document.createTextNode("Start");
    btn1.id='play';
    btn1.appendChild(t1);
    document.getElementById("menu").appendChild(btn1);

    var btn2 = document.createElement("BUTTON");
    var t2 = document.createTextNode("Restart");

    btn2.id='reset';
    btn2.appendChild(t2);
    document.getElementById("myDIV").appendChild(btn2);
    btn2.style.visibility="hidden";


    menu.style.textAlign="center";


    $("#play").click(function(){
        Start();
        btn1.parentNode.removeChild(btn1);
        let divD = document.createElement("DIV");
        divD.setAttribute('id','d');
        document.getElementById("myDIV").appendChild(divD);
        jouer(0);
    });

    $("#reset").click(function(){
        selection1=null;
        selection2=null;
        Reset();
        Start();
        jouer(0);
    });

}


function writeText(){
    document.getElementById("text").textContent = 'Répondez avant que le temps soit écoulé ! Bonne chance !';
}

function removeButton() {
    var elem = document.getElementById('myButton');
    elem.parentNode.removeChild(elem);
}

var x = document.getElementById("myDIV");

// Start the animation with JavaScript
function myFunction() {
    x.style.WebkitAnimation = "mymove 1s 1"; // Code for Chrome, Safari and Opera
    x.style.animation = "mymove 1s 1";     // Standard syntax
}



// Code for Chrome, Safari and Opera
x.addEventListener("webkitAnimationStart", myStartFunction);
x.addEventListener("webkitAnimationEnd", myEndFunction);



// Standard syntax
x.addEventListener("animationstart", myStartFunction);
x.addEventListener("animationend", myEndFunction);


function myStartFunction() {
    this.style.margin= "0px auto 100px auto";
}

function myEndFunction() {
    this.style.color="black";
    this.style.backgroundColor = "white";
    this.style.width = "1000px";
    this.style.height = "500px";

    this.style.margin= "0px auto 100px auto";
    this.style.borderRadius= "25px";
    test();
}

const target = document.getElementById('jeu'),
    button = document.getElementById('myButton');

button.addEventListener('click', function(){
    target.scrollIntoView({
        block: 'start',
        behavior: 'smooth',
        inline: 'nearest'
    });
    setTimeout(function(){
        window.location.hash = '#jeu';
    }, 1000);
});








/* Timer type coumpte à rebours */



var secondes = 0;
var minutes = 1;
var on = false;
var reset = false;




function chrono(){


    if(minutes>= 1 && secondes==0){
        minutes-=1;
        secondes=59;
    }
    else
        secondes -= 1;

    if(minutes == 0 && secondes <= 0){
        Stop();
        $('span').unbind("click");
        end=true;
    }

    if(secondes>59){
        minutes++;
        secondes=secondes-60;
    }

    affTimer();
}


function Start(){

    if(on===false){
        pts=0;
        timerID = setInterval(chrono, 1000);
        on = true;
        reset = false;
    }
}



function Stop(){
    if(on===true){
        on = false;
        clearTimeout(timerID);
        let btn2 = document.getElementById("reset");
        btn2.style.visibility="visible";
        var p = document.createElement("P");
        var br = document.createElement("BR");
        var t = document.createTextNode("Temps écoulé !");
        var t2 = document.createTextNode("Bravo vous avez trouvé " + indexj + " contrepèteries sur "+ tabContrepeterie.length + " contrepèteries disponibles");
        p.id = 'rep';
        p.appendChild(t);
        p.appendChild(br);
        p.appendChild(t2);
        document.getElementById("myDIV").appendChild(p);
    }
}



function affTimer(){
    if(minutes<10 && secondes<10){
        $("#timer").html("0"+minutes+" : 0"+secondes);
    }
    else if(minutes<10 && secondes>=10){
        $("#timer").html("0"+minutes+" : "+secondes);
    }
    else if(minutes>=10 && secondes<10){
        $("#timer").html(+minutes+" : 0"+secondes);
    }
    else if(minutes>=10 && secondes>10){
        $("#timer").html(+minutes+" : "+secondes);
    }
}
function generate_table(arr) {
    var body = document.getElementsByTagName("body")[0];


    console.log(arr);
    var tbl = document.createElement("table");
    var tblBody = document.createElement("tbody");

    // creating all cells

    // creates a table row
    var row = document.createElement("tr");
    for (var j = 0; j < arr.length; j++) {
        // Create a <td> element and a text node, make the text
        // node the contents of the <td>, and put the <td> at
        // the end of the table row
        var cell = document.createElement("td");
        for (var i=0; i<arr[j].length; i++){
            var cellText = document.createTextNode(arr[j][i]);
        }

        cell.appendChild(cellText);
        row.appendChild(cell);
    }

    // add the row to the end of the table body
    tblBody.appendChild(row);


    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // appends <table> into <body>
    body.appendChild(tbl);
    // sets the border attribute of tbl to 2;
    tbl.setAttribute("border", "2");
}


function Reset(){
    if(reset===false)
    {
        let btn2 = document.getElementById("reset");
        btn2.style.visibility="hidden";
        clearInterval(timerID);
        secondes = 30;
        minutes = 0;
        $("#timer").html("00 : 30");
        let supp = document.getElementById('rep');
        supp.parentNode.removeChild(supp);
        reset = true;
    }
    on = false;
}

function affHighscore(){
    if(localStorage.score1m == null || localStorage.score1m == 'undefined'){
        $("#unF").html("1ere place : 00");
    }
    else{
        $("#unF").html("1ere place : "+ localStorage.score1m);
    }
    if(localStorage.score2m == null || localStorage.score2m == 'undefined'){
        $("#deuxF").html("2eme place : 00");
    }
    else{
        $("#deuxF").html("2eme place : "+ localStorage.score2f);
    }
    if(localStorage.score3m == null || localStorage.score3m == 'undefined'){
        $("#troisF").html("3eme place : 00");
    }
    else{
        $("#troisF").html("3eme place : "+ localStorage.score3m);
    }
    if(localStorage.score4m == null || localStorage.score4m == 'undefined'){
        $("#quatreF").html("4eme place : 00");
    }
    else{
        $("#quatreF").html("4eme place : "+ localStorage.score4m);
    }
    if(localStorage.score5m == null || localStorage.score5m == 'undefined'){
        $("#cinqF").html("5eme place : 00");
    }
    else{
        $("#cinqF").html("5eme place : "+ localStorage.score5m);
    }

}

function highscore(indexj){
    if (localStorage.score1m == null){
        localStorage.score1m = indexj;
    }
    if (indexj > localStorage.score1m){
        localStorage.score5m = localStorage.score4m;
        localStorage.score4m = localStorage.score3m;
        localStorage.score3m = localStorage.score2m;
        localStorage.score2m = localStorage.score1m;
        localStorage.score1m = indexj;
    }
    else if (indexj > localStorage.score2m){
        localStorage.score5m = localStorage.score4m;
        localStorage.score4m = localStorage.score3m;
        localStorage.score3m = localStorage.score2m;
        localStorage.score2m = indexj;
    }
    else if (indexj > localStorage.score3m){
        localStorage.score5m = localStorage.score4m;
        localStorage.score4m = localStorage.score3m;
        localStorage.score3m = indexj;
    }
    else if (indexj > localStorage.score4m){
        localStorage.score5m = localStorage.score4m;
        localStorage.score4m = indexj;
    }
    else if (indexj > localStorage.score5f){
        localStorage.score5f = indexj;
    }
    affHighscore();
}
affHighscore();
