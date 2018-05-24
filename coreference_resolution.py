from pycorenlp import StanfordCoreNLP
from googletrans import Translator
import json

def correct_spell(text):
	translator = Translator()
	spell = translator.translate(text, dest='en')
	return spell.text

def resolve_coreference_in_text(text):
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

	new_text = []
	for idx in range(len(sen)):
		tmp = ""
		for x in range(len(sen[idx]['tokens'])):
			tmp += sen[idx]['tokens'][x]['word']
			if x<len(sen[idx]['tokens'])-1:
				tmp += " "

		new_text.append(tmp)

	for key in coref.keys():
		tp = coref[key]
		for ele in (tp):
			word = ele[0]
			idx = ele[1]

			new_text[idx-1] = new_text[idx-1].replace(word, key)

	return new_text

if __name__=="__main__" :
	txt = "We reached on 24.05.2018. the staff was good. they treated us well. they were nice."
	text = correct_spell(txt)
	print text
	text = text.encode("utf-8")
	
	var = resolve_coreference_in_text(text)
	for sen in var:
		print sen.encode("utf-8")