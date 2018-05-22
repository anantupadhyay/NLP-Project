from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree, Tree
from nltk.parse.stanford import StanfordParser
import difflib
import json

# Defining the global dictionaries
rel = dict()
rel2 = dict()

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

		# print ("The extracted nouns from the sentence are", noun)
		# print ('#'*100)

# Code for extracting noun ends here!		
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		
# The Code here deals with extracting the dependencies of noun with adjectives and verbs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
		
		for key, val in rel.items():
			st = ""
			for word in text.split():
				#print word
				if word in val:
					st += word + " "
			rel[key] = st

		print rel

# The part reports error, if any, occured in the code

	except Exception as e:
		#print e
		return 'failure',"An error has occured, Failed to Analyse Data, 9000 down"

#The text analysis function ends here
#.........................................................................................................................................................
#*********************************************************************************************************************************************************



#------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
	CODE THAT UTILIZES THE PARSE TREE OF THE SENTENCE STARTS HERE
'''
#------------------------------------------------------------------------------------------------------------------------------------------------------------

def find_attributes(node):
	attrs = []
	dad = node.parent()
	gdad = dad.parent()
	#print node, dad, gdad
	#print node
	# Searching all the siblings of the node
	for sibling in dad:
		if ((sibling.label() == 'JJ') or (sibling.label() == 'RB') or (sibling.label() == 'CD')):
			attrs.append(sibling[0])
		#print sibling[0][0]

	# Searching all the uncles of the node
	for uncle in gdad:
		#print uncle
		# Checking if directly a adverb is present, then append it to attribute list
		if((uncle.label() == 'RB')):
			attrs.append(uncle[0])
		
		# If it is a verb phrase, then check all the children of the VP
		
		elif (uncle.label() == 'VP'):
			for cousin in uncle:
				#print cousin.label()
				if cousin.label() == 'ADJP':
					for ch in cousin:
						attrs.append(ch[0])
						#print ch[0]

				elif ((cousin.label() == 'VBN') or (cousin.label() == 'VBG') or (cousin.label() == 'RB') or (cousin.label() == 'VBP') or (cousin.label() == 'VBZ')):
					attrs.append(cousin[0])
				# the leaves() method returns a list of node
				elif cousin.label() == 'VP':
					for ch in cousin:
						ls = ch.leaves()
						#print ls
						fin_val = ""
						for word in ls:
							fin_val += (' '.join(ls))
						attrs.append(fin_val)
				# if cousin is a noun phrase
				elif (cousin.label() == 'NP'):
					attrs.append(cousin[0][0])


	# Searching all the sibling of grand-parent of the node
	# Here we are looking for verb phrase and its children only
	ggdad = gdad.parent()
	if(ggdad.label() != 'ROOT'):
		for s in ggdad:
			#print s
			if s.label() == 'VP':
				for uch in s:
					#print uch
					'''
						If the children are adjective or adverb
					'''
					if uch.label() == 'ADJP':
						for ch in uch:
							attrs.append(ch[0])

					elif uch.label() == 'ADVP':
						for ch in uch:
							attrs.append(ch[0])

					# Check if it is a verb participle, then append it
					elif uch.label() == 'VBP' or uch.label()=='VBZ' or uch.label()=='VBN' or uch.label()=='VBG':
						attrs.append(uch[0])

					elif uch.label() == 'NP':
						for ch in uch:
							#print ch[0]
							attrs.append(ch[0])



	return attrs

def parsetreeAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
 		output = nlp.annotate(text, properties={'annotators': 'dcoref','outputFormat':'json'})
 		parse_tree = output['sentences'][0]['parse']
		tree = ParentedTree.convert(Tree.fromstring(parse_tree))
		#tree.pretty_print()

		np = dict()
		# FINDING THE NP AND ITS CORRESPONDING NOUN OR PRONOUN
		for s in tree.subtrees(lambda tree: tree.label() == 'NP'):
			'''
				This part deals with the problem that the child of ROOT comes as NP,
				and hence, each noun was counted twice.
			'''
			for n in s.subtrees(lambda n: n.label().startswith('NN')):
				vis = np.get(n[0], 0)
				if(vis == 1):
					continue
				np[n[0]] = 1
				rel2.setdefault(n[0], [])

				attr = find_attributes(n)
				rel2[n[0]] = attr
				#print attr
				if len(attr)==0:
					rel2.pop(n[0])

		#print rel2
		for key, val in rel2.items():
			st = ' '.join(val)
			rel2[key] = st

		print rel2

	# THIS PART CHECKS FOR ERRORS, IF ANY, AND REPORTS THE FAILURE	
	except Exception as e:
 		print e
		return 'failure',"An error has occured, Failed to Analyse Data, 9000 down"
# ---------------------------------------------------------------------------------------------------
'''
	CODE FOR PARSE TREE ENDS HERE
'''
# ---------------------------------------------------------------------------------------------------

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
'''
	THIS PART MERGES THE TWO DICTIONARIES INTO ONE
'''
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def merge (l, r):
    m = difflib.SequenceMatcher(None, l, r)
    for o, i1, i2, j1, j2 in m.get_opcodes():
        if o == 'equal':
            yield l[i1:i2]
        elif o == 'delete':
            yield l[i1:i2]
        elif o == 'insert':
            yield r[j1:j2]
        elif o == 'replace':
            yield l[i1:i2]
            yield r[j1:j2]

def merge_dictionaries(rel, rel2):
	fin_rel = dict()
	for key, val in rel.items():
		if key in rel2.keys():
			val2 = rel2[key]
			merged = merge(val.lower().split(), val2.lower().split())
			new_val = ' '.join(' '.join(x) for x in merged)
			fin_rel[key] = new_val
		else:
			fin_rel = val

	for key, val in rel2.items():
		if key not in fin_rel.keys():
			fin_rel[key] = val


	return fin_rel
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
'''
	CODE FOR MERGING ENDS HERE
'''
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



#-----------------------------------------------
'''
	MAIN FUNCTION STARTS HERE
'''
#-----------------------------------------------
if __name__=="__main__" :
	text = "The tea is served hot here"
	print (text)

	res = (getStanfordAnalysis(text))
	if(res != None):
		print res

	res2 = (parsetreeAnalysis(text))
	if(res2 != None):
		print res2

	kvp = merge_dictionaries(rel, rel2)
	print "\nThe final key value pairs are"
	print kvp

# ------------------------------------------------------
'''
	CONGRATS! YOU HAVE ARRIVED AT THE END OF CODE...
'''
# ------------------------------------------------------
