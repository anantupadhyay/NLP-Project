from pycorenlp import StanfordCoreNLP
import json

def getStanfordAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators': 'dcoref','outputFormat':'json'})
		#'annotators': 'tokenize,ssplit,pos,depparse,parse,dcoref'
		#print(output['sentences'])
		
		
		wjson = json.dumps(output['sentences'])
		wjdata = json.loads(wjson)


# The code below deals with extracting noun and pronouns from the sentence and storing them in a dictionary (index:word)	
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		noun = dict()

		for x in range(len(wjdata[0]['tokens'])):
			if((wjdata[0]['tokens'][x]['pos'] == 'NN') or (wjdata[0]['tokens'][x]['pos'] == 'NNP') or (wjdata[0]['tokens'][x]['pos'] == 'NNS') or (wjdata[0]['tokens'][x]['pos'] == 'PRP')):
				noun[wjdata[0]['tokens'][x]['index']] = wjdata[0]['tokens'][x]['word']

		print ("The extracted nouns from the sentence are", noun)
		print ('#'*100)

# Code for extracting noun ends here!		
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		
# The Code here deals with extracting the dependencies of noun with adjectives and verbs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		rel = dict()
		#Buddy Check token also
		for x in range(len(wjdata[0]['enhancedPlusPlusDependencies'])):
			if((wjdata[0]['enhancedPlusPlusDependencies'][x]['dependent']) in noun.keys()):
				#getting the index of the governor
				#print ("here")
				idx = wjdata[0]['enhancedPlusPlusDependencies'][x]['governor']
				#print (idx)
				# If it is related to ROOT, then no need to add it to dictionary
				if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] == 'ROOT'):
					continue
				#print (idx)
				if((wjdata[0]['tokens'][idx-1]['pos'] == 'JJ') or (wjdata[0]['tokens'][idx-1]['pos'] == 'JJS') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBN') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBG') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'RB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'CD') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBZ')):
					#print ("not here")
					#print (wjdata[0]['tokens'][idx]['word'])
					if(noun[(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependent'])] not in rel.keys()):
						rel.setdefault(noun[(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependent'])], [])

					rel[noun[(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependent'])]].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

			elif((wjdata[0]['enhancedPlusPlusDependencies'][x]['governor']) in noun.keys()):
				#getting the index of the dependent
				idx = wjdata[0]['enhancedPlusPlusDependencies'][x]['dependent']
				# If it is related to ROOT, then no need to add it to dictionary
				if(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] == 'ROOT'):
					continue
				if((wjdata[0]['tokens'][idx-1]['pos'] == 'JJ') or (wjdata[0]['tokens'][idx-1]['pos'] == 'JJS') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBN') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBG') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'CD') or (wjdata[0]['tokens'][idx-1]['pos'] == 'RB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBZ')):
					#print("here")
					if(noun[(wjdata[0]['enhancedPlusPlusDependencies'][x]['governor'])] not in rel.keys()):
						rel.setdefault(noun[(wjdata[0]['enhancedPlusPlusDependencies'][x]['governor'])], [])
					rel[noun[(wjdata[0]['enhancedPlusPlusDependencies'][x]['governor'])]].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'])
		
# The part dealing with extracting adjective and verb dependencies from noun ends here!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		



# The following part deals with extracting negative and compound relations from the sentence
# ============================================================================================================================================================================================================================================================================================================================================================
		for x in range(len(wjdata[0]['enhancedPlusPlusDependencies'])):
			if((wjdata[0]['enhancedPlusPlusDependencies'][x]['dep'] == 'neg')):
				for key, val in rel.items():
					#print ("Reached here")
					if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] in val):	
						#print ('here')
						rel[key].insert(0, wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'])
					elif(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] in val):
						#print ("here")
						rel[key].insert(0, wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

			if((wjdata[0]['enhancedPlusPlusDependencies'][x]['dep'] == 'xcomp')):
				for key, val in rel.items():
					#print ("Reached here")
					if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] in val):	
						#print ('here')
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] != key):
							rel[key].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'])
					elif(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] in val):
						#print ("here")
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] != key):
							rel[key].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

			if((wjdata[0]['enhancedPlusPlusDependencies'][x]['dep'] == 'dobj')):
				for key, val in rel.items():
					if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] in val):	
						#print ('here')
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] != key):
							rel[key].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'])
					elif(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] in val):
						#print ("here")
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] != key):
							rel[key].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

			if((wjdata[0]['enhancedPlusPlusDependencies'][x]['dep'] == 'compound')):
				for key, val in rel.items():
					if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] in val):	
						#print ('here')
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] != key):
							rel[key].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'])
					elif(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] in val):
						#print ("here")
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] != key):
							rel[key].append(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

			if((wjdata[0]['enhancedPlusPlusDependencies'][x]['dep'] == 'advmod')):
				for key, val in rel.items():
					if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] in val):	
						#print ('here')
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] != key):
							rel[key].insert(0, wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'])
					elif(wjdata[0]['enhancedPlusPlusDependencies'][x]['dependentGloss'] in val):
						#print ("here")
						if(wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'] != key):
							rel[key].insert(0, wjdata[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

# This part ends here! 
# =========================================================================================================================================================================================================================================

# This part prints the final key value pair

		print ("Here are the final key value pairs\n")
		for key, val in rel.items():
			print (key, val)

# The part reports error, if any, occured in the code

	except Exception as e:
		#print e
		return 'failure',"An error has occured, Failed to Analyse Data, 9000 down"

#The text analysis function ends here
#.........................................................................................................................................................
#*********************************************************************************************************************************************************

if __name__=="__main__" :
	text = "The restaurant had only Indian cuisine"
	print (text)

	res = (getStanfordAnalysis(text))
	if(res != None):
		print res