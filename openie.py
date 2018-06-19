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
	# print output
	wjson = json.dumps(output['sentences'])
	data = json.loads(wjson)
	
	openie_dict = {}
	for i in range(0, len(data[0]['openie'])):
		sub = data[0]['openie'][i]['subject'].encode('utf-8')
		obj = data[0]['openie'][i]['object'].encode('utf-8')
		if sub in openie_dict:
			# pass
			openie_dict[sub] += " "+obj
		else:
			openie_dict[sub] = obj 

	for key in openie_dict:
		openie_dict[key] = list(set(openie_dict[key].split()))

	print openie_dict


text = "The room is good but food was worse and room is big"
text = "complementry food wastage asked to pay 1000/- for a meal."
text = "the fruits were fresh"
text = "Leather doors with leather handles, kind of like old time steamer trunks."
text = "the decor is decidedly along the lines of a corporate apartment."
print getOpenIE(getCoreNLPAnalysis(text))