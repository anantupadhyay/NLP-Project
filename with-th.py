from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree, Tree
from nltk.parse.stanford import StanfordParser
import difflib
import json
import coreference_resolution as cr 
import threading
import re
import itertools
import string

# Defining the global list that would contain the final key value pair of sentences
finalDic = list()

def getCoreNLPAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators': "tokenize,ssplit,ner,regexner,depparse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		#'annotators': 'tokenize,ssplit,pos,depparse,parse,dcoref'
		#print output
		#exit()
		return output

	except Exception as er:
		print er
		return 'Failure\n'

# =================================================================================
'''
	DEFINING THE CLEANER FUNCTION TO PREPROCESS THE TEXT
'''
# =================================================================================

def cleaner_function(text):
	emojis = [(':-J', ' '), ('=^_^=', ' '), (':-o', ' '), ('=-D', ' '), ('>_<', ' '), ('(*_*)', ' '), 
		('>_<*', ' '), ('=)', ' '), ('=(', ' '), (':-p', ' '), (':p', ' '), ('=D', ' '),(':-/', ' '),
		(':/', ' '), ('>-:o', ' '), ('>:o', ' '), ('B)', ' '), ('B-)', ' '), ('8-|', ' '), ('8|', ' '),
		('O:)', ' '), ('O:-)', ' '), ('<3', ' '), (':)', ' '), (':D', ' '), (':(', ' '), (':-)', ' '),
		(':-(', ' '), (':P', ' ')]


	emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  							# emoticons
        u"\U0001F300-\U0001F5FF"  							# symbols & pictographs
        u"\U0001F680-\U0001F6FF"  							# transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  							# flags (iOS)
                           "]+", flags=re.UNICODE)

	text = re.sub(r"\b([A-Za-z]+)'re\b", '\\1 are', text)	# changing "'re" to 'are'
	text = re.sub(r"\b([A-Za-z]+)isn't\b", '\\1 is not', text)	# changing "sn't" to 'is not'
	text = re.sub(r"\b([A-Za-z]+)'s\b", '\\1 is', text)		# changing "'s" to 'is'
	text = re.sub(r"\b([A-Za-z]+)'m\b", '\\1 am', text)		# changing "'am" to 'am'
	text = re.sub(r"\b([A-Za-z]+)'ve\b", '\\1 have', text)	# changing "'ve" to 'have'
	text = re.sub(r"\b([A-Za-z]+)'ll\b", '\\1 will', text)	# changing "'ll" to 'will'
	text = re.sub(r"\b([A-Za-z]+)n't\b", '\\1 not', text)	# changing "n't" to 'not'
	text = re.sub(r"\b([A-Za-z]+)'d\b", '\\1 had', text)	# changing "'d" to 'had'

	text = text.replace(" n ", " and ")						# Replacing 'n' with 'and'
	text = text.replace(" bcz ", " because ")				# replacing 'bcz' with 'because'
	text = text.replace(" ur ", " your ")					# replacing 'ur' with 'your'
	text = text.replace(" u` ", " you ")					# replacing 'ur' with 'your'
	text = text.replace(" b4 ", " before ")					# relpacing 'b4' with 'before'
	text = text.replace(" awsm ", " awesome ")				# replacing 'awsm' with 'awesome'
	
	text = re.sub(r'\.+', ".", text)						# replacing '...*' with '.'
	text = re.sub(r'\?+', "?", text)						# replacing '???*' with '?'

	text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))		# replacing 'testtttt' with 'testt'
	text = (emoji_pattern.sub(r'', text))					# remove emoji pattern in text

	for k,v in emojis:
		text = text.replace(k, v)

	print('-'*100)
	print "Cleaned text is\n", text
	print('-'*100)
	return text

'''
	CLEANING OF TEXT ENDS HERE
'''

# ---------------------------------------------------------------------------------------------

'''
	EXTRACTION BASED ON POS AND DEPENDENCY BEGINS HERE !
'''
def getDependencyAnalysis(output, text):
	try:
		#print(output['sentences'])
		wjson = json.dumps(output['sentences'])
		wjdata = json.loads(wjson)


# The code below deals with extracting noun and pronouns from the sentence and storing them in a dictionary (index:word)	
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		noun = dict()
		rel = dict()

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

		#print rel
		return rel
		

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
		if child.label() == 'DT':
			x = child[0].lower()
			if x=='no' or x=='not':
				atrb.append(x)

		elif child.label() == 'IN':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'NP':
			tmp = noun_phrase_attrb(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

	return atrb

def noun_phrase_attrb(node):
	atrb = []
	for child in node:
		if child.label() == 'DT':
			x = child[0].lower()
			if x=='no' or x=='not':
				atrb.append(x)

		elif child.label().startswith('NN'):
			atrb.append(' '.join(child.flatten()))

		elif child.label().startswith('JJ'):
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'NP':
			tmp = noun_phrase_attrb(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'VP':
			tmp = verb_phrase_attrb(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'ADJP':
			tmp = adjective_phrase_attrb(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'ADVP':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'CD':
			atrb.append(' '.join(child.flatten()))

	return atrb


def adjective_phrase_attrb(node):
	atrb = []
	for child in node:
		if child.label().startswith('JJ'):
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'VP':
			tmp = verb_phrase_attrb(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'NP':
			tmp = noun_phrase_attrb(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'PP':
			tmp = second_level_pp(child)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif child.label() == 'ADVP':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'RB':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'CD':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'MD':
			atrb.append(' '.join(child.flatten()))

	return atrb

def verb_phrase_attrb(node):
	atrb = []

	for cousin in node:
		#print cousin.label()
		if cousin.label() == 'ADJP':
			tmp = adjective_phrase_attrb(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)
		#print ch[0]
		elif cousin.label() == 'ADVP':
			atrb.append(' '.join(cousin.flatten()))

		elif ((cousin.label() == 'VBN') or (cousin.label() == 'VBG') or (cousin.label() == 'RB') or (cousin.label() == 'VBP') or (cousin.label() == 'VBZ')):
			tmp = ' '.join(cousin.flatten())
			if tmp.lower() != "is":
				atrb.append(tmp)

			#print "here", atrb, node
		# the leaves() method returns a list of node
		elif cousin.label() == 'VP':
			tmp = verb_phrase_attrb(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)
		# if cousin is a noun phrase
		elif (cousin.label() == 'NP'):
			tmp = noun_phrase_attrb(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif cousin.label() == 'RB':
			atrb.append(' '.join(cousin.flatten()))

		elif cousin.label() == 'CD':
			atrb.append(' '.join(cousin.flatten()))

		elif cousin.label() == 'MD':
			atrb.append(' '.join(cousin.flatten()))

		elif cousin.label() == 'VB':
			atrb.append(' '.join(cousin.flatten()))

	return atrb

def ucp_phrase(node):
	atrb = []

	for cousin in node:
		#print cousin.label()
		if cousin.label() == 'ADJP':
			tmp = adjective_phrase_attrb(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)
		#print ch[0]
		elif cousin.label() == 'ADVP':
			atrb.append(' '.join(cousin.flatten()))

		elif ((cousin.label() == 'VBN') or (cousin.label() == 'VBG') or (cousin.label() == 'RB') or (cousin.label() == 'VBP') or (cousin.label() == 'VBZ')):
			tmp = (' '.join(cousin.flatten()))
			if tmp.lower() != "is":
				atrb.append(tmp)

		elif cousin.label() == 'VP':
			tmp = verb_phrase_attrb(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif cousin.label() == 'UCP':
			tmp = ucp_phrase(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)
		# if cousin is a noun phrase
		elif (cousin.label() == 'NP'):
			tmp = noun_phrase_attrb(cousin)
			if len(tmp) > 0:
				for word in tmp:
					atrb.append(word)

		elif cousin.label() == 'RB':
			atrb.append(' '.join(cousin.flatten()))

		elif cousin.label() == 'CD':
			atrb.append(' '.join(cousin.flatten()))

		elif cousin.label() == 'MD':
			atrb.append(' '.join(cousin.flatten()))

		elif cousin.label() == 'VB':
			atrb.append(' '.join(cousin.flatten()))

	return atrb



def find_attributes(node):
	attrs = []
	dad = node.parent()
	gdad = dad.parent()
	#print node, dad, gdad
	#print node[0]
	# Searching all the siblings of the node
	for sibling in dad:
		if ((sibling.label().startswith('JJ')) or (sibling.label() == 'RB') or (sibling.label() == 'CD')):
			attrs.append(sibling[0])

		elif sibling.label() == 'ADJP':
			tmp = adjective_phrase_attrb(sibling)
			if len(tmp) > 0:
				for word in tmp:
					attrs.append(word)

		elif sibling.label() == 'DT':
			x = sibling[0].lower()
			if x=='no' or x=='not':
				attrs.append(x)

		elif sibling.label() == 'VBG':
			tmp = sibling[0].lower()
			if tmp != "is":
				attrs.append(tmp)
		#print sibling[0][0]

	# Searching all the uncles of the node
	for uncle in gdad:
		if gdad == None:
			break
		if(uncle == dad):
			continue
		# Checking if directly a adverb is present, then append it to attribute list
		if((uncle.label() == 'RB')):
			attrs.append(uncle[0])

		elif uncle.label() == 'VB' or uncle.label()=='VBN':
			attrs.append(' '.join(uncle.flatten()))

		elif uncle.label() == 'UCP':
			tmp = ucp_phrase(uncle)
			if len(tmp) > 0:
				for word in tmp:
					attrs.append(word)
		
		# If it is a verb phrase, then check all the children of the VP
		elif (uncle.label() == 'VP'):
			#print uncle[0][0]
			tmp = verb_phrase_attrb(uncle)
			if len(tmp) > 0:
				for word in tmp:
					attrs.append(word)

		elif uncle.label() == 'ADJP':
			tmp = adjective_phrase_attrb(uncle)
			if len(tmp) > 0:
				for word in tmp:
					attrs.append(word)

		elif uncle.label() == 'NP':
			tmp = noun_phrase_attrb(uncle)
			if len(tmp) > 0:
				for word in tmp:
					attrs.append(word)

		elif uncle.label() == 'S':
			for child in uncle:
				if child.label() == 'VP':
					tmp = verb_phrase_attrb(child)
					if len(tmp) > 0:
						for word in tmp:
							attrs.append(word)

		elif uncle.label() == 'PP':
			tmp = second_level_pp(uncle)
			if len(tmp) > 0:
				for word in tmp:
					attrs.append(word)

	# Searching all the sibling of grand-parent of the node
	# Here we are looking for verb phrase and its children only
	#print attrs
	if ((gdad.parent()!=None) and (len(attrs)==0 or gdad.parent().label()=='S' or gdad.parent().label()=='FRAG' or gdad.parent().label()=='VP')):
		ggdad = gdad.parent()
		
		if(ggdad.label() != 'ROOT'):
			for s in ggdad:
				if s==gdad:
					continue
				#print s
				if s.label() == 'VP':
					#print "here"
					tmp = verb_phrase_attrb(s)
					if len(tmp) > 0:
						for word in tmp:
							attrs.append(word)

				elif s.label() == 'VB':
					attrs.append(' '.join(s.flatten()))

				elif s.label() == 'NP':
					tmp = noun_phrase_attrb(s)
					if len(tmp) > 0:
						for word in tmp:
							attrs.append(word)

				elif s.label() == 'RB':
					attrs.append(' '.join(s.flatten()))

				elif s.label() == 'ADJP':
					tmp = adjective_phrase_attrb(s)
					if len(tmp) > 0:
						for word in tmp:
							attrs.append(word)

				elif s.label() == 'ADVP':
					attrs.append(' '.join(s.flatten()))



	return attrs

def parsetreeAnalysis(text):
	try:
		#print text
		#print output
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators': "parse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		parse_tree = output['sentences'][0]['parse']
 		#print parse_tree
		tree = ParentedTree.convert(Tree.fromstring(parse_tree))
		#tree.pretty_print()

		np = dict()
		rel2 = dict()
		# FINDING THE NP AND ITS CORRESPONDING NOUN OR PRONOUN
		for s in tree.subtrees(lambda tree: tree.label() == 'NP'):
			'''
				This part deals with the problem that the child of ROOT comes as NP,
				and hence, each noun was counted twice.
			'''
			for n in s.subtrees(lambda n: n.label().startswith('NN') or n.label()=='PRP'):
				#print "here"
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
		print ('\n')
		for key, val in rel2.items():
			st = ' '.join(val)
			rel2[key] = st

		#print rel2
		return rel2

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
			#print new_val
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

# -----------------------------------------------------------------------------
'''
	THIS PART CONTAINS THE FUNCTION FOR RUNNING THREADS
'''
# -----------------------------------------------------------------------------

def run_thread(op, sent, lock):
	sen = sent.translate(None, string.punctuation)
	#print sen
	#res = (getDependencyAnalysis(op, sen))
	res = {}
	res2 = (parsetreeAnalysis(sen))
	#print res2
	kvp = dict()
	if res and res2 and type(res)!=tuple and type(res2)!=tuple:
		kvp = merge_dictionaries(res, res2)
	elif res:
		kvp = res
	elif res2:
		kvp = res2
	#print "\nThe final key value pairs are"
	#print kvp
	#print ('*'*100)
	#global xx
	lock.acquire()
	finalDic.append(kvp)
	lock.release()

# -----------------------------------------------------------------------------
'''
	THREAD FUNCTION ENDS HERE
'''
# -----------------------------------------------------------------------------

# =============================================================================
'''
	THIS PART DEALS WITH REMOVING STOPWORDS FROM FINAL LIST OF KEY-VALUE-PAIRS
'''
# =============================================================================
	
def remove_stop_words(stopwordList):
	try:
		#print stopwordList
		for x in range(len(finalDic)):
			for k,v in finalDic[x].items():
				for word in v.split():
					#print word
					if word in stopwordList:
						v = v.replace(word, '')

				finalDic[x][k] = v

		print '\n\n'
		print finalDic

	except:
		return "An error occured"

# =============================================================================
'''
	---------------------STOPWORD REMOVAL ENDS HERE----------------------------
'''
# =============================================================================

# =============================================================================
'''
	---------------------NAMED ENTITY RECOGNISITION----------------------------
'''
# =============================================================================

def namedEntityRecognisition(output, text):
	rep = []
	sen = ""
	org = ""
	for x in range(len(output['sentences'][0]['tokens'])):
		tmp = output['sentences'][0]['tokens'][x]['ner']
		if tmp != 'O':	
			word = output['sentences'][0]['tokens'][x]['originalText']
			org += word + " "
			sen += word + "-"
		else:
			if len(sen) > 1:
				#print sen
				sen = sen[:-1]
				org = org[:-1]
				text = text.replace(org, sen)
				sen = ""
				org = ""

	return text

# =============================================================================
'''
	----------------NAMED ENTITY RECOGNISITION ENDS HERE-----------------------
'''
# =============================================================================


#-----------------------------------------------
'''
	MAIN FUNCTION STARTS HERE
'''
#-----------------------------------------------

if __name__=="__main__" :
	text = "I was not provided blanket at night"
	text = "the fan above the bed is dirty"
	text = "Very limited snacks and food items available."
	text = "The restaurant serves very reasonably priced and quality cuisine."
	text = "The bar is decently stocked."
	text = "Courteous staff and overall a value for money."
	text = "The room was good but the ac stop working"
	text = "Staff is quite good and managing person is really good person I ever meet in my life (hotel)"
	text = "smell of cigarettes smoking was there when I entered  rooms should be smelling good and fresh"
	text = "Food was cold but it was good it should be eaten raw"
	text = "Staff is quite good and the managing person is a really good person I have ever meet in my life (hotel)"
	
	print "Original Text is -> ", text

	# op = cr.correct_spell(text)
	# op = op.encode("utf-8")
	# print op
	# print type(op)
	clean_txt = cleaner_function(text)
	txt = cr.resolve_coreference_in_text(clean_txt)
	#print txt
	lock = threading.Lock()
	t = [None]*len(txt)
	x = 0
	for sent in txt:
		#print sent
		# print type(sen)
		sen = sent.encode("utf-8")
		op = getCoreNLPAnalysis(sen)
		sen = namedEntityRecognisition(op, sen)
		print "Individual sentence is -> ", sen.encode("utf-8")
		#print op
		sen = sen.replace("-LRB-", "(")
		sen = sen.replace("-RRB-", ")")
		#print sen
		inp = sen.encode("utf-8")
		#print type(inp)
		t[x] = threading.Thread(target=run_thread, args=(op, inp, lock,))
		t[x].start()
		x += 1
		#t.join()

	for x in range(len(txt)):
		t[x].join()

	
	print finalDic

	stopwordList = set(line.strip() for line in open('stopwords.txt'))
	print('-'*110)
	print ("Removing stop words, Final KVP are")
	print remove_stop_words(stopwordList)
	print('-'*100)

	# with open('outputfile.txt', 'w') as fout:
	# 	for x in xrange(len(finalDic)):
	# 		for k,v in finalDic[x].items():
	# 			fout.write(k)
	# 			fout.write(": "+v)
	# 			fout.write('\n')
# ------------------------------------------------------
'''
	CONGRATS! YOU HAVE ARRIVED AT THE END OF CODE...
'''
# ------------------------------------------------------
