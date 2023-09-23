var dic=[];
var dicMot=[];
var dicPhon=[];
var dicCle=[];


function handleFileSelect(evt) {

	var file = evt.target.files[0];
	Papa.parse(file, {
		header: true,
		dynamicTyping: true,
		complete: function(results) {
			dic.push(results);
			console.log(dic);
			splitdicSelector()
		}
	});

}

$(document).ready(function(){
	$("#csv-file").change(handleFileSelect);
});

function splitdicSelector(){
	for(let i=0; i<dic[0]['data'].length; i++){
		dicMot.push(dic[0]['data'][i][0]);
		dicPhon.push(dic[0]['data'][i][1]);
	}
	console.log("Affichage du dictionaire de mots");
	console.log(dicMot);
	console.log("Affichage du dictionaire de sons");
	console.log(dicPhon);
}


function splitdic(){
	for(let i=0; i<dic.length; i++){
		dicMot.push(dic[i]['data'][0]);
		dicPhon.push(dic[i]['data'][1]);
	}
	console.log("Affichage du dictionaire de mots");
	console.log(dicMot);
	console.log("Affichage du dictionaire de sons");
	console.log(dicPhon);
}



function loadDico(){
	document.querySelector('#gen').addEventListener('mousedown', event=>{
		document.querySelector('#loadingJeuBeta').style.visibility = "visible";
		document.body.style.cursor = 'wait';
	});

	document.getElementById('chargement').innerHTML = '<div class="loading"></div>';

	document.getElementById('choixLettreP').setAttribute('style','border: 4px solid #7ac142;');

	let pathToDictionary = "../dict_fr_ok.csv";

	Papa.parse(pathToDictionary, {
		download: true,
		step: function(row) {
			dic.push(row);
		},
		complete: function() {
			document.getElementById('chargement').innerHTML = '<div id="wrapper"><svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" /><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" /></svg></div>';
			document.getElementById('chargement').style.backgroundColor="beige";
			//document.getElementById('loadDico').disabled=true;
			console.log("All done!");
			console.log(dic);
			console.log("Appel de split dic");
			splitdic(dic);

		}
	});

	$(function () {
		$.getJSON('../dicoPhoncomFr.json', function (data) {
			console.log(data)
			dicCle = data
		});
	});
}



function mainRecherchePhrase() {
	let phrase =  document.getElementById('phrase').value;
	phrase = phrase.toLowerCase().trim();
	return phrase.replace(/'/g, ' ');
}

//Debut de la fonction pour trouver resultat dans phrases //

function mainMixSyllabes(phrase,mode) {
	console.log("phrase a passer à phonToPhrase (avant) :")
	console.log(phrase)
	phrase = phrase.trimEnd();
	var phrase = phrase.split(" ")
	console.log("phrase a passer à phonToPhrase (apres) :")
	console.log(phrase)
	var Lphrases = []
	var tmp = []
	var taille
	var test
	let actualDivId = 0;
	let LphrasesButOnlyThePhrase = []

	Lphrases.push() //ohrase contient elle meme
	//console.log(Lphrases)
	//console.log(phrase)

	//Pour chaque mot dans la phrase
	for (var i in phrase) {
		//console.log(i)
		var j=parseInt(i) + 1;

		for (j;j<phrase.length;j++) {
			var WordsContreP = mixSyllableWord(phrase[i], phrase[j], phrase,mode)
			//console.log("WordContreP : " + WordsContreP)
			for (k in WordsContreP) {
				//console.log("k = " + k)
				tmp = [].concat(phrase)
				/*
				console.log("tmp i = " + tmp[i])
				console.log("WordsContreP[k] = " + WordsContreP[k][0])
				console.log("tmp j = " + tmp[j])
				console.log("WordsContreP[k] = " + WordsContreP[k][1])
				*/

				
				tmp[i] = WordsContreP[k][0]
				tmp[j] = WordsContreP[k][1]
				console.log("------------phrase :")
				console.log(phrase)
				console.log("------------tmp :")
				console.log(tmp)
				taille = phrase.length
				test = true
				for(let l=0;l<taille;l++) {
					if(phrase == tmp) {
						test = false
					}
					if(test) {
						//console.log("------------phrase :")
						//console.log(phrase)
						//console.log("------------tmp :")
						//console.log(tmp)
						//console.log(L1)
						//console.log(L2)
						//console.log("lphrase :")	
						//console.log(Lphrases)
						//console.log(phrase)
						//console.log(tmp)
						if(mode === "phon") {
							let maPhrase = phonToPhrase(tmp).join(' ');
							//LphrasesButOnlyThePhrase sert à éviter le problème lié aux id dans Lphrases
							if(!LphrasesButOnlyThePhrase.includes(maPhrase)) {
								Lphrases.push(`<div class='flexAllCenter' id='divID-${actualDivId}'><button style='padding: 5px; margin: 5px; border-radius: 8px; border: 2px solid #81c784; min-width: 150px; color: black; background-color: white; font-weight: bold;' onclick='trouverOrthographePhonem("${maPhrase}", ${actualDivId})'>${maPhrase}</button><p style='color: darkslategray; font-weight: bold; font-family: fantasy;'></p></div><hr>`)
								LphrasesButOnlyThePhrase.push(maPhrase)
							}
							actualDivId += 1;
						}
						if(mode === "lettre" && !Lphrases.includes("<div class='card shadow-sm bgWhite'>"+ tmp.join(' ') + "</div>") && (tmp.join(' ') !== phrase)) {
							Lphrases.push("<div class='card shadow-sm bgWhite'>"+ tmp.join(' ') + "</div>");
						}
					}
				}
				
			}
		}
	}
	affichageMotPhrase(Lphrases, mode)
	document.querySelector('#loadingJeuBeta').style.visibility = "collapse";
	document.body.style.cursor = 'default';
}

function affichageMotPhrase(l, mode){
	let element = document.getElementById("div1");
	while (element.firstChild){
		element.removeChild(element.firstChild);
	}

	if(mode === "lettre") {
		let actualDivRow =  document.createElement('div');
		actualDivRow.setAttribute("class", "row");
		for(let i=0; i<l.length; i++){
			if(i%5 == 0) {
				document.querySelector('div#div1').append(actualDivRow);
				let divRow = document.createElement('div');
				divRow.setAttribute("class", "row");
				actualDivRow = divRow;
				actualDivRow.setAttribute("style","margin: 20px;");
				let divCol = document.createElement('div');
				divCol.setAttribute("class", "col");
				divCol.innerHTML=l[i];
				actualDivRow.append(divCol);
			}
			else {
				let divCol = document.createElement('div');
				divCol.setAttribute("class", "col");
				divCol.innerHTML=l[i];
				actualDivRow.append(divCol);
			}
		}
	}
	else if(mode === "phon") {
		document.querySelector('div#div1').classList.remove("flexAllCenter");
		for(let i=0; i<l.length; i++){
			let myDiv = document.createElement('div');
			myDiv.innerHTML=l[i];
			document.getElementById('div1').append(myDiv);
		}
	}
}




function mixSyllableWord(word1,word2,phrase,mode) {
	console.log("PASSE-----------------------------------------------------")
	listeWord = [];
	tmp = Array();
	var i = 0;
	var j = 1;
	while(i<word1.length) {
		//console.log(word1)
		//console.log(word1.length)
		//console.log(i)

		tmp = mixSyllableWord2(word1.slice(i,j),word2,phrase,mode)
		//console.log("--------------------tmp--------------------- " )
		//console.log(tmp)

		for (k in tmp) {
			let mot = word1.slice(0,i)+tmp[k][1]+word1.slice(j)
			if (motExiste(mot,dicMot) && mode === "lettre") {
				listeWord.push([mot, tmp[k][0],[i,j],tmp[k][2]])
				//console.log("existe lettre :"+mot)
			}
			if (motExiste(mot,dicPhon) && mode === "phon") {
				listeWord.push([mot, tmp[k][0],[i,j],tmp[k][2]])
				//console.log("existe phon :"+mot)
			}
		}

		j+=1
		if (j>word1.length) {
			i+=1
			j=i+1
		}
		//console.log("listeWord :")
		//console.log(listeWord)

	}
	return listeWord
}

function mixSyllableWord2(sy,word2,phrase,mode) {
	i = 0;
	j = 1;
	liste = [];
	while(i<word2.length) {

		mot = word2.slice(0,i) + sy + word2.slice(j)
		//console.log("mot : "+mot)
		if (motExiste(mot,dicMot) && mode === "lettre") {
			liste.push([mot,word2.slice(i,j),[i,j]])
			//console.log("existe lettre :"+mot)
		}
		if (motExiste(mot,dicPhon) && mode === "phon") {
			liste.push([mot,word2.slice(i,j),[i,j]])
			//console.log("existe phon :"+mot)
		}
		j+=1;
		if (j>word2.length) {
			i+=1
			j=i+1
		}
		//console.log("liste miwSyllabeWord2 : ")
		//console.log(liste)

	}
	return liste
}



function phraseToPhon(phrase) {
	let str=""
	let mots = phrase.split(' ')
	//console.log("phrase avant dans phraseToPhon: ")
	//console.log(mots)
	for(let i=0; i<mots.length; i++) {
		let ind;
		for (let j = 0; j < dicMot.length; j++) { //On trouve l'index de ce mot dans le dico
			if (dicMot[j] == mots[i]) {
				ind = j;
			}
		}
		if(ind != 0) {
			str += (dicPhon[ind] + ' ')
			console.log("Trouvé dans phraseToPhon : "+dicPhon[ind])
		}
		else
			console.log("Mot pas dans le dico ( dans phraseToPhon) : "+mots[i])
	}
	return str;
}


function phonToPhrase(phrase) {
	let str = ""
	let mots = phrase
	//console.log("phrase avant dans phonToPhrase : ")
	//console.log(phrase)
	for(let i=0; i<mots.length; i++) {
		let ind;
		for (let j = 0; j < dicPhon.length; j++) { //On trouve l'index de ce mot dans le dico
			if (dicPhon[j] == mots[i]) {
				ind = j;
			}
		}
		if(ind != 0)
			str += (dicMot[ind] + ' ')
		else
			console.log("Mot pas dans le dico ( dans phonToPhrase) : "+mots[i])
	}
	return str.split(' ');
}



//----------------------------------------------------------------------------

function choixLettreP() {
	document.getElementById('div1').innerHTML = '';
	//trouverOrthographePhonem("je carottes unes manges")
	if (document.getElementById('choixLettreP').value == 'false')
	{
		document.getElementById('choixLettreP').setAttribute('style','border: 4px solid #7ac142;');
		document.getElementById('choixPhonemeP').setAttribute('style','border: 4px solid transparent;');
		document.getElementById('choixLettreP').value = 'true';
		document.getElementById('choixPhonemeP').value = 'false';
	}
}

function choixPhonemeP() {
	document.getElementById('div1').innerHTML = '';
	console.log("phonem !!!")
	if (document.getElementById('choixPhonemeP').value == 'false')
	{
		document.getElementById('choixPhonemeP').setAttribute('style','border: 4px solid #7ac142;');
		document.getElementById('choixLettreP').setAttribute('style','border: 4px solid transparent;');
		document.getElementById('choixPhonemeP').value = 'true';
		document.getElementById('choixLettreP').value = 'false';
	}
}

function redirigeLettreOuPhonemePhrase() {
	if (document.getElementById('choixLettreP').value == 'true')
	{
		mainMixSyllabes(mainRecherchePhrase(),"lettre")
	}
	else //l'utilisateur a choisi les phonèmes
	{
		let phrase = mainRecherchePhrase()
		mainMixSyllabes(phraseToPhon(phrase),"phon")
	}
}

function trouverOrthographePhonem(phrase ,divID) {
	phrasePhon = phraseToPhon(phrase).trimEnd().split(" ")
	console.log(phrasePhon)
	var listeRetour = []
	var string = phrase.trimEnd().split(" ")
	var longueurMax=0


	for(let i in phrasePhon) {
		phrasePhon[i] = dicCle[phrasePhon[i]]
	}
	console.log(phrasePhon)

	/*
	for(let j in string)
	{
		console.log("longueur : " + phrasePhon[j].length)
		if (phrasePhon[j].length > longueurMax)
		{
			longueurMax=phrasePhon[j].length
		}
		console.log("valeur de j : " + j + " correspond a "+  phrasePhon[j])
		console.log(phrasePhon[j])
		for (let k in phrasePhon[j])
		{
			console.log("valeur de k : " + k + " correspond a "+  phrasePhon[j][k])
			//string.push(phrasePhon[j][k])
			string[j]=phrasePhon[j][k]
		}
	console.log("phrase a ajouter : " +string)
	listeRetour.push(string)
	string=phrase.split(" ")
	//console.log("liste = " + listeRetour)
	}
	console.log(string)
	//listeRetour.push(phrasePhon)
	console.log(listeRetour)*/

	for(let j in string) {
		if (phrasePhon[j].length > longueurMax) {
			longueurMax = phrasePhon[j].length
		}

		for (let k=0;k<longueurMax;k++) {
			if (typeof(phrasePhon[j][k]) == "undefined") {
				//string[j] = phrasePhon[j][k]
				break
			}
			else
			{
				string[j] = phrasePhon[j][k]
			}
		listeRetour.push(string.join(" "))
		}

	}
	let myP = document.querySelector(`div#divID-${divID}`).querySelector('p');
	myP.innerText = listeRetour.join("  /  ");
	//console.log(listeRetour)
}



