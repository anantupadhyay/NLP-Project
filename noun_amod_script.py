from pycorenlp import StanfordCoreNLP
import json

def dependencyAnalysis(text):
	try:
		output = StanfordCoreNLP('http://13.127.253.52:9000/').annotate(text, properties={'annotators': "tokenize,ssplit,pos,depparse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		wjson = json.dumps(output['sentences'])
		data = json.loads(wjson)
		noun = dict() # Maps nouns with their indexs
		idx = set() # Stores index of all nouns which are related by nsubj
		noun_list = list() # final list of output
		check_list = ['NN', 'NNP', 'NNS']
		for x in range(len(data[0]['tokens'])):
			if(data[0]['tokens'][x]['pos'] in check_list):
				noun[data[0]['tokens'][x]['index']] = data[0]['tokens'][x]['word']
		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if(tmp['dep']=='nsubj'):
				x1 = tmp['dependent']
				x2 = tmp['governor']
				if ((data[0]['tokens'][x1-1]['pos'] in check_list) and (data[0]['tokens'][x2-1]['pos'] in check_list)):
					idx.add(x2)
		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if((tmp['governor']) in idx and tmp['dep']=='amod'):
				s1 = tmp['dependentGloss'] + "_" + tmp['governorGloss']
				noun_list.append(s1)
		print noun_list

	except Exception as err:
		print ("Oops! Error Occured"), err

if __name__=="__main__" :
	try:
		text = "The managing person is a good person"
		#text = "The managing director was humble person"
		res = dependencyAnalysis(text)
		if res != None:
			print res

	except Exception as err:
		print ("Error Occured"), err