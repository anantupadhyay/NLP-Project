from pycorenlp import StanfordCoreNLP
import json

def fun(text):
	nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
	output = nlp.annotate(text, properties={'annotators': 'dcoref','outputFormat':'json'})
	#'annotators': 'tokenize,ssplit,pos,depparse,parse,dcoref'
	#print output['corefs']
	dmp = json.dumps(output['corefs'])
	data = json.loads(dmp)

	pnoun = ['he', 'she', 'they', 'it', 'their', 'we']
	coref = dict()
	for keys in data:
		if len(data[keys]) > 1:
			key = ""
			lis = list()
			for x in range(len(data[keys])):
				if data[keys][x]['isRepresentativeMention'] == True:
					coref.setdefault(data[keys][x]['text'], [])
					key = data[keys][x]['text']

				elif data[keys][x]['isRepresentativeMention'] == False and data[keys][x]['text'].lower() in pnoun:
					lis.append(data[keys][x]['text'])
					lis.append(data[keys][x]['sentNum'])

			coref[key] = lis

	print coref

fun("the staff members are good, they treated us well")