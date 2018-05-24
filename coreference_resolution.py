from pycorenlp import StanfordCoreNLP
import json

def fun(text):
	nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
	output = nlp.annotate(text, properties={'annotators': 'coref','outputFormat':'json'})
	#'annotators': 'tokenize,ssplit,pos,depparse,parse,dcoref'
	#print output['corefs']
	dmp = json.dumps(output['corefs'])
	data = json.loads(dmp)
	dmp2 = json.dumps(output['sentences'])
	sen = json.loads(dmp2)

	pnoun = ['he', 'she', 'they', 'it', 'we']
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
					tup = (data[keys][x]['text'], data[keys][x]['sentNum'])
					lis.append(tup)
					del(tup)

			if len(lis) == 0:
				coref.pop(key, None)
			else:
				coref[key] = lis

	text = []
	for idx in range(len(sen)):
		tmp = ""
		for x in range(len(sen[idx]['tokens'])):
			tmp += sen[idx]['tokens'][x]['word']
			if x<len(sen[idx]['tokens'])-1:
				tmp += " "

		text.append(tmp)

	for key in coref.keys():
		tp = coref[key]
		for ele in (tp):
			word = ele[0]
			idx = ele[1]

			text[idx-1] = text[idx-1].replace(word, key)

	print text

fun("We reached at 10am. the staff was good. they treated us well. they were nice.")