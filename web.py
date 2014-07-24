#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from bs4 import BeautifulSoup

import glob
import os

print("// ==UserScript==")
print("// @name        ia solver")
print("// @namespace   ia")
print("// @description Test Solver")
print("// @include     http://*.ugr.es/SCACP/*")
print("// @include file:///*")
print("// @version     1.1")
print("// @grant       none")
print("// ==/UserScript==")
print("//Array de respuestas")
print("var obj = {")

lineas = ""
lines = {}

os.chdir("files")

#for file in sorted(glob.glob('tema3-miguel.html'), reverse = True):
for file in sorted(glob.glob('*.html'), reverse = True):

	soup = BeautifulSoup(open(file)) #fichero html a parsear

	#numero = 1

	for text in soup.find_all("div", class_="respuestasGift"):

		question = text.find("strong", class_="tituloGift").get_text()
		question = question.replace("\n", "")
		#question = "PRegunta"

		answer =  "" #answer" #text

		#quitamos los puntuacion
		punts = text.findAll("strong", text="Puntuación: 0.0")
		[punt.extract() for punt in punts]
		punts = text.findAll("strong", text="Puntuación: 1.0")
		[punt.extract() for punt in punts]
		punts = text.findAll("strong", text="Puntuación: -1.0")
		[punt.extract() for punt in punts]
		punts = text.findAll("strong", text="Puntuación: 0.33333334")
		[punt.extract() for punt in punts]

		#obtenemos todos los strong que no tengan class (los titulos) y los concatenamos
		for br in text.findAll('strong'):
			if not br.has_attr('class') :
				answer += br.get_text().replace("\n", "") + "\\n"

		#quitamos el ultimo caracter (salto de linea)
		answer = answer[:-2]


		question = question.replace(" ", "");
		question = question.strip();

		answer = answer.replace("(100.0 %)", "");
		answer = answer.replace("(50.0 %)", "");

		answer = answer.replace("'", "\\'");

		# if (question.contains("de forma inteligente")) 
		# if question.find("is") != -1:
		# 	print question

		

		answer = answer.strip()


		### 1--CORREGIR LAS QUE TIENEN MUCHOS VERDADEROS
		### 2--USAR UNA COLECCIÓN PARA EVITAR DUPLICADOS
		### 3--TRATAR LAS QUE SON DE RESPUESTAS MULTIPLES con negativos y las normales

		# Si no hay respuesta, una de dos o no está en la base de datos o es una de verdero y falso
		##NOTA FALTA CONTROLAR CUANDO NO TENGAMOS LA RESPUESTA
		if len(answer) == 0:
			#answer = "verdadero/falso" #aciertoGift

			#if text.find("div", class_="aciertoGift") and text.find("input", attrs={"type" : "radio", "value":"Verdadero", "checked":"true"}) :

			if text.find("div", class_="aciertoGift") and text.find("input", attrs={"type" : "radio", "value": "Verdadero"}) and text.find("input", attrs={"type" : "radio", "value": "Verdadero"}).has_attr("checked"):
				answer = "verdadero"
			elif text.find("div", class_="aciertoGift") and text.find("input", attrs={"type" : "radio", "value" : "Verdadero", "checked": "checked"}):
				answer = "verdadero"
			elif text.find("div", class_="falloGift") and text.find("input", attrs={"type" : "radio", "value": "Falso", "checked":"checked"}):
				answer = "falso"
			elif text.find("div", class_="aciertoGift") and text.find("input", attrs={"type" : "radio", "value": "Verdadero"}) and not text.find("input", attrs={"type" : "radio", "value": "Verdadero"}).has_attr("checked"):
				answer = "verdadero"
			elif text.find("div", class_="falloGift") and text.find("input", attrs={"type" : "radio", "value": "Falso"}) and not text.find("input", attrs={"type" : "radio", "value": "Falso"}).has_attr("checked"):
				answer = "falso";
			else:
				#Las acertadas pasaran por aqui (no hay respuesta y no son checkbox controlable, dejamos la respuesta en blanco y así esa línea no se agrega)
				#print question
				answer = "";	
		
		if len(answer) > 0:
			#lineas += "		'" + question + "': '" + answer + "',\n"
			if question in lines:
				if lines[question] != answer:
					#Esto se usa para detectar respuestas diferentes
					1+1
					# print "DIFERENTES!!!!------" + file
					# print question
					# print lines[question]  
					# print answer
					# print "--------------------"
			else:
				lines[question] = answer;



#recorremos el diccionario
for key, value in lines.iteritems():
    lineas +=  "		'" + key + "': '" + value + "',\n"


#quitamos el ultimo caracter (coma y salto de linea)
lineas = lineas[:-2]

print(lineas)
print("};")
print("");
print("//Obtenemos todos los elementos strong y los recorremos")
print("var links = document.getElementsByTagName('strong');")
print("for (var i = 0; i < links.length; i++) {")
print("	//Buscamos la cabecera de la pregunta")
print("	if (links[i].className == 'tituloGift') {")
print("		//Agregamos la respuesta al title, así lo veremos como tooltip")
print("		var question = links[i].textContent.replace(/ /g, '').trim();")
print("")
print("		links[i].title = obj[question];")
print("		try {")
print("			var answers = obj[question].split('\\n');")
print("")	
print("			for (var answer in answers) {")
print("")	
print("				var labels = links[i].parentNode.getElementsByTagName('input');")
print("")	
print("				for(var j = 0; j < labels.length; j++) {")
print("")	
print("					var itm = labels[j];")
print("")	
print("					if (itm.type == 'checkbox') {")
print("")	
print("						if (itm.nextSibling.textContent.trim() === answers[answer].trim()) {")
print("							itm.checked = true;")
print("						}")
print("					} else if (itm.type == 'radio') {")
print("						if (itm.value === 'Verdadero' && answers[answer] === 'verdadero') {")
print("							itm.checked = true;")
print("						} else if (itm.value === 'Falso' && answers[answer] === 'falso') {")
print("							itm.checked = true;")
print("						}")
print("					}")
print("				}")
print("			}")
print("			// Comprobamos si hay combos (esto es  fijo)")
print("			var selects = links[i].parentNode.getElementsByTagName('select');")
print("			if (selects.length > 0) {")
print("				// Opcion combo 1")
print("				var resp = answers[0].split(' -> ');")
print("				var options = selects[0].getElementsByTagName('option');")
print("				for (opt in options) {")
print("					if (options[opt].value.trim() === resp[1].trim()) {")
print("						options[opt].selected = true;")
print("						break;")
print("					}")
print("				}")
print("				// Opcion combo 2")
print("				resp = answers[1].split(' -> ');")
print("				options = selects[1].getElementsByTagName('option');")
print("				for (opt in options) {")
print("					if (options[opt].value.trim() === resp[1].trim()) {")
print("						options[opt].selected = true;")
print("						break;")
print("					}")
print("				}")
print("				// Opcion combo 3")
print("				resp = answers[2].split(' -> ');")
print("				options = selects[2].getElementsByTagName('option');")
print("				for (opt in options) {")
print("					if (options[opt].value.trim() === resp[1].trim()) {")
print("						options[opt].selected = true;")
print("						break;")
print("					}")
print("				}")
print("			}")
print("		} catch(err) {")
print("			console.log(err);")
print("		}")
print("	}")
print("}")
