from pycorenlp import StanfordCoreNLP
import json

def getCoreNLPAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators':"tokenize,ssplit,openie", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		return output

	except Exception as er:
		print er
		return 'Failure\n'

def getOpenIE(output):
	wjson = json.dumps(output['sentences'])
	data = json.loads(wjson)
	
	openie_dict = {}
	for i in range(0, len(data[0]['openie'])):
		sub = data[0]['openie'][i]['subject'].encode('utf-8')
		obj = data[0]['openie'][i]['object'].encode('utf-8')
		if sub in openie_dict:
			openie_dict[sub] += " "+obj
		else:
			openie_dict[sub] = obj 

	print openie_dict


text = "The room is good but food was worse and room is big"
print getOpenIE(getCoreNLPAnalysis(text))