from pycorenlp import StanfordCoreNLP
import json

def dependencyAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators': "tokenize,ssplit,pos,depparse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		wjson = json.dumps(output['sentences'])
		data = json.loads(wjson)
		noun = dict()
		noun_list = list()
		for x in range(len(data[0]['tokens'])):
			if((data[0]['tokens'][x]['pos'] == 'NN') or (data[0]['tokens'][x]['pos'] == 'NNP') or (data[0]['tokens'][x]['pos'] == 'NNS')):
				noun[data[0]['tokens'][x]['index']] = data[0]['tokens'][x]['word']

		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if((tmp['governor']) in noun.keys() and tmp['dep']=='amod'):
				s1 = tmp['dependentGloss'] + " " + tmp['governorGloss']
				noun_list.append(s1)
		print noun_list

	except Exception as err:
		print ("Oops! Error Occured"), err

if __name__=="__main__" :
	try:
		text = "The managing person is a good person"
		res = dependencyAnalysis(text)
		if res != None:
			print res

	except Exception as err:
		print ("Error Occured"), err