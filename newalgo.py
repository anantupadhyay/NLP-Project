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
		output = nlp.annotate(text, properties={'annotators': 'dcoref','outputFormat':'json', 'pipelineLanguage': 'en'})
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
#-----------------------	-------------------------------------------------------------------------------------------------------------------------------------------------------------------
		
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
				if((wjdata[0]['tokens'][idx-1]['pos'] == 'JJ') or (wjdata[0]['tokens'][idx-1]['pos'] == 'JJS') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBN') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBG') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'RB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'CD') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBZ')  or (wjdata[0]['tokens'][idx-1]['pos'] == 'JJR')):
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
				if((wjdata[0]['tokens'][idx-1]['pos'] == 'JJ') or (wjdata[0]['tokens'][idx-1]['pos'] == 'JJS') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBN') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBG') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'RB') or (wjdata[0]['tokens'][idx-1]['pos'] == 'CD') or (wjdata[0]['tokens'][idx-1]['pos'] == 'VBZ')  or (wjdata[0]['tokens'][idx-1]['pos'] == 'JJR')):
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
		
		# for key, val in rel.items():
		# 	st = ""
		# 	for word in text.split():
		# 		#print word
		# 		if word in val:
		# 			st += word + " "
		# 	rel[key] = st

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

def second_level_pp(node):
	atrb = []
	for child in node:
		if child.label()=='NP':
			tmp = noun_phrase_attr(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label()=='IN':
			x = child[0].lower()
			if x != 'in':
				atrb.append(x)

	return atrb

def noun_phrase_attr(node):
	atrb = []
	for ch in node:
		if(ch.label().startswith('NN') or ch.label().startswith('PRP')):
			atrb.append(' '.join(ch.flatten()))
		elif ch.label().startswith('JJ'):
			atrb.append(' '.join(ch.flatten()))
		elif ch.label()=='DT':
			x = ch[0].lower()
			if x=='no' or x=='not':
				atrb.append(x)
		elif ch.label()=='NP':
			tmp = noun_phrase_attr(ch)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

	return atrb

def adjective_phrase_attr(node):
	atrb = list()
	#print node
	for child in node:
		if child.label().startswith('JJ'):
			atrb.append(' '.join(child.flatten()))
		elif child.label()=='RB':
			atrb.append(' '.join(child.flatten()))
		elif child.label()=='VP':
			tmp = verb_phrase_attr(child)
			if len(tmp) > 0:
				for word in tmp:
					#print word
					atrb.append(word)
		elif child.label() == 'NP':
			tmp = noun_phrase_attr(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'ADJP':
			tmp = adjective_phrase_attr(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'ADVP':
			atrb.append(' '.join(child.flatten()))

	return atrb

def verb_phrase_attr(node):
	#print node
	atrb = list()
	#atrb.append('test')
	for child in node:
		if(child.label() == 'VP'):
			tmp = verb_phrase_attr(child)
			if len(tmp)>0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'ADVP':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'RB':
			atrb.append(' '.join(child.flatten()))

		elif child.label().startswith('JJ'):
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'ADJP':
			temp = adjective_phrase_attr(child)
			if len(temp) > 0:
				for word in temp:
					atrb.append(word)

		elif child.label()=='VBZ' or child.label()=='VBN' or child.label()=='VBP' or child.label()=='VBN' or child.label()=='VBG':
			atrb.append(' '.join(child.flatten()))

		elif child.label()=='NP':
			tmp = noun_phrase_attr(child)
			for word in tmp:
				atrb.append(word)

		elif child.label()=='S':
			for ch in child:
				if ch.label()=='ADJP':
					#print "I am here"
					tmp = adjective_phrase_attr(ch)
					#print tmp
					if len(tmp) > 0:
						for word in tmp:
							atrb.append(word)
				elif ch.label()=='VP':
					tmp = verb_phrase_attr(ch)
					if len(tmp) > 0:
						for word in tmp:
							atrb.append(word)

				elif ch.label()=='RB':
					atrb.append(' '.join(ch.flatten()))
				elif ch.label().startswith('JJ'):
					atrb.append(' '.join(ch.flatten()))

	#print atrb
	return atrb


def find_attributes(node):
	attrs = []
	dad = node.parent()
	gdad = dad.parent()
	#print node, dad, gdad
	#print node
	# Searching all the siblings of the node
	for sibling in dad:
		if ((sibling.label() == 'JJ') or (sibling.label() == 'JJS') or (sibling.label() == 'RB') or (sibling.label() == 'CD')):
			attrs.append(' '.join(sibling.flatten()))

		elif sibling.label()=='DT':
			x = sibling[0].lower()
			if x=='no' or x=='not':
				attrs.append(x)

		#print sibling[0][0]

	# Searching all the uncles of the node
	for uncle in gdad:
		if(uncle == dad):
			continue
		#print uncle.label(), node[0]
		# Checking if directly a adverb is present, then append it to attribute list
		if((uncle.label() == 'RB')):
			attrs.append(' '.join(uncle.flatten()))
		
		# If it is a verb phrase, then check all the children of the VP
		elif (uncle.label() == 'VP'):
			#print uncle[0][0]
			tmp_attr = verb_phrase_attr(uncle)
			if len(tmp_attr) > 0:
				for word in tmp_attr:
					attrs.append(word)

		elif uncle.label() == 'VBD':
			attrs.append(' '.join(uncle.flatten()))
		elif uncle.label() == 'VB':
			attrs.append(' '.join(uncle.flatten()))
		elif uncle.label() == 'S':
			for uch in uncle:
				if uch.label()=='VP':
					tmp = verb_phrase_attr(uch)
					if len(tmp) > 0:
						for word in tmp:
							attrs.append(word)

		# elif uncle.label()=='PP':
		# 	tmp = second_level_pp(uncle)
		# 	if len(tmp) > 0:
		# 		for word in tmp:
		# 			attrs.append(word)

	# Searching all the sibling of grand-parent of the node
	# Here we are looking for verb phrase and its children only
	#print attrs
	if len(attrs)==0 or gdad.parent().label()=='S':
		ggdad = gdad.parent()
		if(ggdad.label() != 'ROOT'):
			for s in ggdad:
				if s==gdad:
					continue
				if s.label() == 'VP':
					tmp = verb_phrase_attr(s)
					#print len(tmp)
					if len(tmp) > 0:
						for word in tmp:
							attrs.append(word)

				elif s.label() == 'VB':
					attrs.append(' '.join(s.flatten()))

				elif s.label() == 'NP':
					for ch in s:
						if ch.label().startswith('NN'):
							attrs.append(' '.join(ch.flatten()))
						# Explicitly checking if 'no' or 'not' is tagged as determiner
						elif ch.label()=='DT':
							x = ch[0].lower()
							if x=='no' or x=='not':
								attrs.append(x)



	return attrs

def parsetreeAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
 		output = nlp.annotate(text, properties={'annotators': 'dcoref','outputFormat':'json', 'pipelineLanguage': 'en'})
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
			for n in s.subtrees(lambda n: n.label().startswith('NN') or n.label()=='PRP'):
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

		#print np
		#print rel2
		print ('\n')
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

#****************************************************************************************************

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
			print new_val
			fin_rel[key] = new_val
		else:
			#pass
			fin_rel[key] = val

	for key, val in rel2.items():
		if key not in (fin_rel.keys()):
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
	text = "the bed was like sleeping on a coroners table"
	print (text)

	res = (getStanfordAnalysis(text))
	if(res != None):
		print res

	res2 = (parsetreeAnalysis(text))
	if(res2 != None):
		print res2

	# kvp = merge_dictionaries(rel, rel2)
	# print "\nThe final key value pairs are"
	# print kvp

# ------------------------------------------------------
'''
	CONGRATS! YOU HAVE ARRIVED AT THE END OF CODE...
'''
# ------------------------------------------------------
