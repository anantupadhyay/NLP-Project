# from pycorenlp import StanfordCoreNLP
# import json

# def dependencyAnalysis(text):
# 	try:
# 		output = StanfordCoreNLP('http://13.127.253.52:9000/').annotate(text, properties={'annotators': "tokenize,ssplit,pos,depparse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
# 		wjson = json.dumps(output['sentences'])
# 		data = json.loads(wjson)
# 		noun = dict() # Maps nouns with their indexs
# 		idx = set() # Stores index of all nouns which are related by nsubj
# 		noun_list = list() # final list of output
# 		check_list = ['NN', 'NNP', 'NNS']
# 		for x in range(len(data[0]['tokens'])):
# 			if(data[0]['tokens'][x]['pos'] in check_list):
# 				noun[data[0]['tokens'][x]['index']] = data[0]['tokens'][x]['word']
# 		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
# 			tmp = data[0]['enhancedPlusPlusDependencies'][x]
# 			if(tmp['dep']=='nsubj'):
# 				x1 = tmp['dependent']
# 				x2 = tmp['governor']
# 				if ((data[0]['tokens'][x1-1]['pos'] in check_list) and (data[0]['tokens'][x2-1]['pos'] in check_list)):
# 					idx.add(x2)
# 		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
# 			tmp = data[0]['enhancedPlusPlusDependencies'][x]
# 			if((tmp['governor']) in idx and tmp['dep']=='amod'):
# 				s1 = tmp['dependentGloss'] + "_" + tmp['governorGloss']
# 				noun_list.append(s1)
# 		print noun_list

# 	except Exception as err:
# 		print ("Oops! Error Occured"), err

# if __name__=="__main__" :
# 	try:
# 		text = "The managing person is a good person"
# 		text = "more staff should be at reception"
# 		res = dependencyAnalysis(text)
# 		if res != None:
# 			print res

# 	except Exception as err:
# 		print ("Error Occured"), err

from pycorenlp import StanfordCoreNLP
import json
from collections import defaultdict
def dependencyAnalysis(text):
	try:
		output = StanfordCoreNLP('http://13.127.253.52:9000/').annotate(text, properties={'annotators': "tokenize,ssplit,pos,depparse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		wjson = json.dumps(output['sentences'])
		data = json.loads(wjson)
		noun = dict() # Maps nouns with their indexs
		idx = defaultdict(list) # Stores index of all nouns relations
		noun_list = list() # final list of output
		check_list = ['NN', 'NNP', 'NNS', 'PRP']
		for x in range(len(data[0]['tokens'])):
			if(data[0]['tokens'][x]['pos'] in check_list):
				noun[data[0]['tokens'][x]['index']] = data[0]['tokens'][x]['word']
		print noun
		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if tmp['dep']=='nsubj':
				idx[tmp['dependent']].append(tmp['governor'])

		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if tmp['governor'] in noun.keys() and tmp['governor'] not in idx.keys() and tmp['dep']=='amod':
				s = tmp['dependentGloss'] + "_" + tmp['governorGloss']
				noun[tmp['governor']] = s
			elif tmp['governor'] in noun.keys() and tmp['governor'] in idx.keys() and tmp['dep']!='det':
				idx[tmp['governor']].append(tmp['dependent'])
		sen = text.split()
		for k,v in idx.items():
			for val in v:
				if val in noun.keys():
					noun_list.append((noun[k],noun[val]))
				else:
					noun_list.append((noun[k],sen[val-1]))

		print noun_list

	except Exception as err:
		print ("Oops! Error Occured"), err

if __name__=="__main__" :
	try:
		text = "The managing person is a good person"
		text = "more staff should be at reception"
		res = dependencyAnalysis(text)
		if res != None:
			print res

	except Exception as err:
		print ("Error Occured"), err