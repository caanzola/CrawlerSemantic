var fs = require('fs');
var writeStream = fs.createWriteStream("test.txt");

var Crawler = require("crawler");

var c = new Crawler({
	rateLimit: 250
});

let SEPARADOR = ";";

writeStream.write("FechaYLugar" + SEPARADOR + "Titulo" + SEPARADOR + "Autores" + "\n");

// Queue URLs with custom callbacks & parameters
c.queue([{
	uri: 'http://ceur-ws.org/',
	callback: function (error, res, done) {
		if(error){
			console.log(error);

		}else{
			var $ = res.$;
			var links = $("a");
			for(var i = 0; i < links.length; i++) {
				let currentLink = links[i];
				let url = currentLink["attribs"]["href"];
				if(url && url.includes(".org/Vol-")) {
					c.queue([{
						uri: url,
						callback: function(error, res, done) {
							if(error) {
								console.log("error");
							} else {
								var $ = res.$;
								var title = null;
								var authors = [];
								var dateAndPlace = null;

								// Fecha y lugar
								let selector = $(".CEURLOCTIME");
								if(selector.length > 0) {
									if(selector[0]["children"] && selector[0]["children"].length > 0) {
										let data = selector[0]["children"][0]["data"];
										dateAndPlace = data;
									}
								}
								if(dateAndPlace) {
									console.log("Fecha:" + dateAndPlace);
									console.log("\n");
								}

								// Titulo && Autores
								let lis = $("li");
								for(var i = 0; i < lis.length; i++) {
									title = getTitle(lis[i]["children"]);
									authors = getAuthors(lis[i]["children"]);
									if(title && dateAndPlace) {
										console.log("Titulo:" + title);
										console.log("Autores:" + authors);
										console.log("\n");
										writeStream.write(dateAndPlace + SEPARADOR + title + SEPARADOR + authorsListToString(authors) + "\n");
									}
									title = null;
									authors = [];
								}
								dateAndPlace = null;
								console.log("\n");
							}
							done();
						}
					}])
				}
			}
		}
		done();
	}
}]);

function getTitle(li) {
	let al = li[0]["children"];
	if(al && al.length > 0) {
		for(var i = 0; i < al.length; i++) {
			if(al[i]["attribs"] && al[i]["attribs"]["class"] === "CEURTITLE") {
				if(al[i]["children"] && al[i]["children"].length > 0 && al[i]["children"][0]["data"]) {
					return al[i]["children"][0]["data"];
				}
			}
		}
	}
}

function getAuthors(li) {
	let authors = [];
	if(li && li.length > 0) {
		for(var i = 0; i < li.length; i++) {
			let currentLi = li[i];
			if(currentLi["attribs"] && currentLi["attribs"]["class"] && currentLi["attribs"]["class"] === "CEURAUTHOR") {
				let children = currentLi["children"];
				if(children && children.length > 0 && children[0]["data"]) {
					authors.push(children[0]["data"]);
				}
			}
		}
	}
	return authors;
}

function authorsListToString(authors) {
	var authorsString = "";
	for(var i = 0; i < authors.length; i++) {
		authorsString += authors[i] + SEPARADOR;
	}
	return authorsString;
}
