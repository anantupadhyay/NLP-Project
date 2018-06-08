from pycorenlp import StanfordCoreNLP
import json

def getStanfordAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators': 'dcoref','outputFormat':'json'})#'annotators': 'tokenize,ssplit,pos,depparse,parse,dcoref'
		#print(output['sentences'][0]['parse'])
		#print(output['sentences'])
		#print getSentences(output['sentences'])
		#for i in range(0,len(output['sentences'])):
		# 	output['sentences'][i]['sentence']=getSentences(output['sentences'][i]['tokens'])
		# 	sentence_list.append(output['sentences'][i]['sentence'])

		# lock.acquire()
		# combine_dict['stanfordAnalysis'] =output
		# print 'sucess stanford'#,output
		# lock.release()
		
		wjson = json.dumps(output['sentences'])
		wjdata = json.loads(wjson)
		#print wjdata
		key = set()
		val = set()
		nmod = []
		case = dict()
		for x in range(len(wjdata[0]['basicDependencies'])):

			if (wjdata[0]['basicDependencies'][x]['dep'] == 'nummod'):
				key.add(wjdata[0]['basicDependencies'][x]['governorGloss'])
				val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
			
			
			if(wjdata[0]['basicDependencies'][x]['dep'] == 'advmod'):
				if((wjdata[0]['basicDependencies'][x]['dependentGloss']) not in key):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				
				if((wjdata[0]['basicDependencies'][x]['governorGloss']) not in val):
					key.add(wjdata[0]['basicDependencies'][x]['governorGloss'])
			
			if(wjdata[0]['basicDependencies'][x]['dep'] == 'amod'):
				if((wjdata[0]['basicDependencies'][x]['dependentGloss']) not in key):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				if((wjdata[0]['basicDependencies'][x]['governorGloss']) not in val):
					key.add(wjdata[0]['basicDependencies'][x]['governorGloss'])
			
			if(wjdata[0]['basicDependencies'][x]['dep'] == 'nsubj' or wjdata[0]['basicDependencies'][x]['dep'] == 'nsubjpass'):
				if((wjdata[0]['basicDependencies'][x]['dependentGloss']) not in val):
					key.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				if((wjdata[0]['basicDependencies'][x]['governorGloss']) not in key):
					val.add(wjdata[0]['basicDependencies'][x]['governorGloss'])
			
			if(wjdata[0]['basicDependencies'][x]['dep'] == 'nmod'):
				if((wjdata[0]['basicDependencies'][x]['governorGloss']) not in val):
					key.add(wjdata[0]['basicDependencies'][x]['governorGloss'])
				if((wjdata[0]['basicDependencies'][x]['dependentGloss'] not in key)):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
					nmod.append(wjdata[0]['basicDependencies'][x]['dependent'])

			if(wjdata[0]['basicDependencies'][x]['dep'] == 'conj'):
				if((wjdata[0]['basicDependencies'][x]['governorGloss']) not in val):
					key.add(wjdata[0]['basicDependencies'][x]['governorGloss'])
					if((wjdata[0]['basicDependencies'][x]['dependentGloss']) not in val):
						key.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				else:
					if((wjdata[0]['basicDependencies'][x]['dependentGloss']) not in val):
						val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])


			if(wjdata[0]['basicDependencies'][x]['dep'] == 'compound'):
				if(wjdata[0]['basicDependencies'][x]['governorGloss'] in key):
					key.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				elif(wjdata[0]['basicDependencies'][x]['governorGloss'] in val):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])

			if(wjdata[0]['basicDependencies'][x]['dep'] == 'dobj'):
				if(wjdata[0]['basicDependencies'][x]['governorGloss'] in key):
					key.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				elif(wjdata[0]['basicDependencies'][x]['governorGloss'] in val):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
			
			if(wjdata[0]['basicDependencies'][x]['dep'] == 'case'):
				case[wjdata[0]['basicDependencies'][x]['governorGloss']] = wjdata[0]['basicDependencies'][x]['governor']

			if(wjdata[0]['basicDependencies'][x]['dep'] == 'xcomp'):
				if(wjdata[0]['basicDependencies'][x]['governorGloss'] in key):
					key.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				elif(wjdata[0]['basicDependencies'][x]['governorGloss'] in val):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])

			if(wjdata[0]['basicDependencies'][x]['dep'] == 'neg'):
				if(wjdata[0]['basicDependencies'][x]['governorGloss'] in key):
					key.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
				elif(wjdata[0]['basicDependencies'][x]['governorGloss'] in val):
					val.add(wjdata[0]['basicDependencies'][x]['dependentGloss'])
			
		for x in range(len(wjdata[0]['tokens'])):
			if(wjdata[0]['tokens'][x]['pos'] == 'VB'):
				if(wjdata[0]['tokens'][x]['originalText']) not in val:
					key.add(wjdata[0]['tokens'][x]['originalText'])

			if(wjdata[0]['tokens'][x]['pos'] == 'JJ'):
				if(wjdata[0]['tokens'][x]['originalText']) not in key:
					val.add(wjdata[0]['tokens'][x]['originalText'])

			
			#if(wjdata[0]['tokens'][x]['pos'] == 'NN' or wjdata[0]['tokens'][x]['pos'] == 'NNS' or wjdata[0]['tokens'][x]['pos'] == 'NNP'):
			#	if(wjdata[0]['tokens'][x]['originalText']) not in val:
			#		key.add(wjdata[0]['tokens'][x]['originalText'])
			
		# print nmod
		# print case
		
		remove_word = set()
		for x in val:
			if (x in case.keys()) and (case[x] in nmod):
				remove_word.add(x)

		val = val.difference(remove_word)
		#print ("key are ", key)
		for word in text.split():
			if word in key:
				print word,
		print('\n')
		for word in text.split():
			if word in val:
				print word,
		
		print ("\n\n\nEnd of function")
	except Exception as e:
		#print e
		return 'failure',"Failed to Analyse Data, 9000 down"

text = "the ac stops working"
print (text)

print getStanfordAnalysis(text.lower())