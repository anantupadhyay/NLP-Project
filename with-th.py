from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree, Tree
from nltk.parse.stanford import StanfordParser
import json
import coreference_resolution as cr 
import threading
import re
import itertools
import string
from replace_common_words import split_words

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
	text = text.replace(" u ", " you ")						# replacing 'ur' with 'your'
	text = text.replace(" b4 ", " before ")					# relpacing 'b4' with 'before'
	text = text.replace(" awsm ", " awesome ")				# replacing 'awsm' with 'awesome'
	
	text = re.sub(r'\.+', ".", text)						# replacing '...*' with '.'
	text = re.sub(r'\?+', "?", text)						# replacing '???*' with '?'

	#text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))		# replacing 'testtttt' with 'testt'
	text = (emoji_pattern.sub(r'', text))					# remove emoji pattern in text

	for k,v in emojis:
		text = text.replace(k, v)

	pattern = re.compile(r'\b(' + '|'.join(split_words.keys()) + r')\b')
	result = pattern.sub(lambda x: split_words[x.group()], text)

	print('-'*100)
	print "Cleaned text is\n", result
	print('-'*100)
	return result

# ---------------------------------------------------------------------------------------------

'''
	EXTRACTION BASED ON POS AND DEPENDENCY BEGINS HERE !
'''
def getDependencyAnalysis(output, text):
	try:
		#print(output['sentences'])
		wjson = json.dumps(output['sentences'])
		data = json.loads(wjson)
		# The code below deals with extracting noun and pronouns from the sentence and storing them in a dictionary (index:word)	
		noun = dict()
		nlist = ['NN', 'NNP', 'NNS', 'PRP']
		rel = dict()
		for x in range(len(data[0]['tokens'])):
			if((data[0]['tokens'][x]['pos']) in nlist):
				noun[data[0]['tokens'][x]['index']] = data[0]['tokens'][x]['word']
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		# The Code here deals with extracting the dependencies of noun with adjectives and verbs
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if((tmp['dependent']) in noun.keys()):
				idx = tmp['governor']
				# If it is related to ROOT, then no need to add it to dictionary
				if(tmp['governorGloss'] == 'ROOT'):
					continue
				if(((data[0]['tokens'][idx-1]['pos'] == 'JJ') or (data[0]['tokens'][idx-1]['pos'] == 'JJS') or (data[0]['tokens'][idx-1]['pos'] == 'VBN') or (data[0]['tokens'][idx-1]['pos'] == 'VBG') or (data[0]['tokens'][idx-1]['pos'] == 'VB') or (data[0]['tokens'][idx-1]['pos'] == 'RB') or (data[0]['tokens'][idx-1]['pos'] == 'CD') or (data[0]['tokens'][idx-1]['pos'] == 'VBZ') or data[0]['tokens'][idx-1]['pos'] == 'NN') and tmp['dep']=='nsubj'):
					if(noun[(tmp['dependent'])] not in rel.keys()):
						rel.setdefault(noun[(tmp['dependent'])], [])
					rel[noun[(tmp['dependent'])]].append(data[0]['enhancedPlusPlusDependencies'][x]['governorGloss'])

			elif((tmp['governor']) in noun.keys()):
				#getting the index of the dependent
				idx = tmp['dependent']
				# If it is related to ROOT, then no need to add it to dictionary
				if(tmp['dependentGloss'] == 'ROOT'):
					continue
				if((data[0]['tokens'][idx-1]['pos'] == 'JJ') or (data[0]['tokens'][idx-1]['pos'] == 'JJS') or (data[0]['tokens'][idx-1]['pos'] == 'VBN') or (data[0]['tokens'][idx-1]['pos'] == 'VBG') or (data[0]['tokens'][idx-1]['pos'] == 'VB') or (data[0]['tokens'][idx-1]['pos'] == 'CD') or (data[0]['tokens'][idx-1]['pos'] == 'RB') or (data[0]['tokens'][idx-1]['pos'] == 'VBZ')  or (data[0]['tokens'][idx-1]['pos'] == 'RBR')):
					if(noun[(tmp['governor'])] not in rel.keys()):
						rel.setdefault(noun[tmp['governor']], [])
					rel[noun[tmp['governor']]].append(tmp['dependentGloss'])
		# The part dealing with extracting adjective and verb dependencies from noun ends here!
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		

		# The following part deals with extracting negative and compound relations from the sentence
		# ============================================================================================================================================================================================================================================================================================================================================================
		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			tmp = data[0]['enhancedPlusPlusDependencies'][x]
			if((tmp['dep'] == 'neg')):
				for key, val in rel.items():
					if(tmp['governorGloss'] in val):
						rel[key].insert(0, tmp['dependentGloss'])
					elif(tmp['dependentGloss'] in val):
						rel[key].insert(0, tmp['governorGloss'])

			elif tmp['dep'].startswith('nmod'):
				if tmp['governorGloss'] in rel.values() and tmp['dependentGloss'] not in rel.values():
					key = rel.get(tmp['governorGloss'])
					rel[key].append(tmp['dependentGloss'])
			elif tmp['dep'].startswith('acl'):
				if tmp['governorGloss'] in key and tmp['dependentGloss'] not in rel[tmp['governorGloss']]:
					rel[tmp['governorGloss']].append(tmp['dependentGloss'])

			elif((tmp['dep']=='xcomp') or (tmp['dep']=='dobj') or (tmp['dep']=='compound') or (tmp['dep']=='advmod')or tmp['dep']=='nsubjpass'):
				for key, val in rel.items():
					if(tmp['governorGloss'] in val and tmp['dependentGloss'] != key):
						rel[key].append(tmp['dependentGloss'])
					elif(tmp['dependentGloss'] in val and tmp['governorGloss'] != key):
						rel[key].append(tmp['governorGloss'])

			elif(tmp['dep']=='nsubj'):
				if tmp['governorGloss'] in rel.keys():
					rel[tmp['governorGloss']].append(tmp['dependentGloss'])
					if(tmp['dependentGloss'] in rel.keys()):
						x = rel[tmp['dependentGloss']]
						rel[tmp['governorGloss']].extend(x)

		# This part ends here! 
		# =============================================================================================================
		for key, val in rel.items():
			st = ' '.join(val)
			rel[key] = st
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

def add_to_list(atrb, data):
	if len(data) > 0:
		for word in data:
			atrb.append(word)
	return atrb

def check_for_not(atrb, node):
	if node[0].lower=="no" or node[0].lower=="not":
		atrb.append(node[0])
	return atrb

def common_check(child):
	atrb = []
	vb_check = ['VBN', 'VBP', 'VBZ', 'VBG']
	#print child.parent().label(), child[0]
	if child.label().startswith('JJ') or child.label()=='RB':
		atrb.append(' '.join(child.flatten()))

	elif child.label()=='CD' or child.label()=='MD':
		atrb.append(' '.join(child.flatten()))

	elif child.label()=='ADVP':
		atrb.append(' '.join(child.flatten()))

	elif child.label()=='VB':
		atrb.append(' '.join(child.flatten()))

	elif child.parent().label()=='VP' or child.parent().label()=='UCP':
		if child.label() in vb_check:
			wrd = (' '.join(child.flatten()))
			atrb.append(wrd) and wrd.lower()!="is"

	#print(atrb)
	return atrb

def noun_verb_adj_attr(node):
	atrb = []
	for child in node:
		#print child.label()
		if child.label()=='ADJP':
			tmp = adjective_phrase_attrb(child)
			atrb = add_to_list(atrb, tmp)

		elif child.label()=='VP':
			tmp = verb_phrase_attrb(child)
			atrb = add_to_list(atrb, tmp)

		elif child.label()=='NP':
			tmp = noun_phrase_attrb(child)
			atrb = add_to_list(atrb, tmp)

		else:
			tmp = common_check(child)
			atrb = add_to_list(atrb, tmp)

	return atrb

def second_level_pp(node):
	atrb = []
	for child in node:
		if child.label() == 'DT':
			atrb = check_for_not(atrb, child)

		elif child.label() == 'IN':
			atrb.append(' '.join(child.flatten()))

		elif child.label() == 'NP':
			tmp = noun_phrase_attrb(child)
			atrb = add_to_list(atrb, tmp)

	return atrb

def noun_phrase_attrb(node):
	atrb = []
	for child in node:
		if child.label() == 'DT':
			atrb = check_for_not(atrb, child)

		elif child.label().startswith('NN'):
			atrb.append(' '.join(child.flatten()))

		elif child.label()=='NP' or child.label()=='VP' or child.label()=='ADJP':
			tmp = noun_verb_adj_attr(child)
			atrb = add_to_list(atrb, tmp)

		else:
			tmp = common_check(child)
			atrb = add_to_list(atrb, tmp)
		
	return atrb

def adjective_phrase_attrb(node):
	atrb = []
	for child in node:
		if child.label() == 'PP':
			tmp = second_level_pp(child)
			atrb = add_to_list(atrb, tmp)

		elif child.label()=='NP' or child.label()=='VP' or child.label()=='ADJP':
			tmp = noun_verb_adj_attr(child)
			atrb = add_to_list(atrb, tmp)

		else:
			tmp = common_check(child)
			atrb = add_to_list(atrb, tmp)

	return atrb

def verb_phrase_attrb(node):
	atrb = []

	for cousin in node:
		#print cousin.label()
		if cousin.label()=='NP' or cousin.label()=='VP' or cousin.label()=='ADJP':
			#print "HERE inside"
			tmp = noun_verb_adj_attr(cousin)
			atrb = add_to_list(atrb, tmp)

		else:
			tmp = common_check(cousin)
			atrb = add_to_list(atrb, tmp)

	return atrb

def ucp_phrase(node):
	atrb = []

	for cousin in node:
		#print cousin.label()
		if cousin.label()=='UCP':
			tmp = ucp_phrase(cousin)
			atrb = add_to_list(atrb, tmp)

		elif cousin.label()=='NP' or cousin.label()=='VP' or cousin.label()=='ADJP':
			tmp = noun_verb_adj_attr(cousin)
			atrb = add_to_list(atrb, tmp)

		else:
			tmp = common_check(cousin)
			atrb = add_to_list(atrb, tmp)

	return atrb

def check_uplevel_cond(gdad, attrs):
	return (gdad.parent()!=None and gdad.parent().label()!='ROOT') and (gdad.label()!='FRAG' and gdad.label()!='SBAR') and (len(attrs)==0 or gdad.parent().label()=='S' or gdad.parent().label()=='FRAG' or gdad.parent().label()=='VP')

def find_attributes(node, rel2, lock):
	#print node[0]
	attrs = []
	dad = node.parent()
	gdad = dad.parent()

	for sibling in dad:
		if sibling == dad:
			continue
		if sibling.label() == 'ADJP' or sibling.label()=='NP':
			tmp = noun_verb_adj_attr(sibling)
			attrs = add_to_list(attrs, tmp)
	
		elif sibling.label() == 'DT':
			attrs = check_for_not(attrs, sibling)

		else:
			tmp = common_check(sibling)
			attrs = add_to_list(attrs, tmp)

	# Searching all the uncles of the node
	if gdad != None:
		for uncle in gdad:
			if(uncle == dad):
				continue

			elif uncle.label()=='UCP':
				tmp = ucp_phrase(uncle)
				attrs = add_to_list(attrs, tmp)
			
			# If it is a verb phrase, then check all the children of the VP
			elif ((uncle.label()=='VP') or (uncle.label()=='NP') or (uncle.label()=='ADJP')):
				tmp = noun_verb_adj_attr(uncle)
				attrs = add_to_list(attrs, tmp)

			elif uncle.label() == 'S':
				for child in uncle:
					if child.label() == 'VP':
						tmp = verb_phrase_attrb(child)
						attrs = add_to_list(attrs, tmp)

			elif uncle.label() == 'PP':
				tmp = second_level_pp(uncle)
				attrs = add_to_list(attrs, tmp)

			else:
				tmp = common_check(uncle)
				attrs = add_to_list(attrs, tmp)

	# Going one level up
	if (check_uplevel_cond(gdad, attrs)):
		ggdad = gdad.parent()
		for s in ggdad:
			if s==gdad:
				continue
			if s.label()=='VP' or s.label()=='NP' or s.label()=='ADJP':
				#print "here"
				tmp = noun_verb_adj_attr(s)
				attrs = add_to_list(attrs, tmp)

			elif s.label()=='VB' or s.label()=='RB' or s.label()=='ADVP' or s.label()=='MD':
				attrs.append(' '.join(s.flatten()))

	lock.acquire()
	rel2[node[0]] = list(set().union(rel2[node[0]],attrs))
	lock.release()

def parsetreeAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
		output = nlp.annotate(text, properties={'annotators': "parse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		parse_tree = output['sentences'][0]['parse']
		tree = ParentedTree.convert(Tree.fromstring(parse_tree))
		#tree.pretty_print()
		rel2 = dict()
		nouns = list()
		# FINDING THE NP AND ITS CORRESPONDING NOUN OR PRONOUN
		for s in tree.subtrees(lambda tree: tree.label().startswith('NN')):
			rel2.setdefault(s[0], [])
			nouns.append(s)
		lck = threading.Lock()
		th = [None]*len(nouns)
		x = 0
		for s in nouns:
			th[x] = threading.Thread(target=find_attributes, args=(s, rel2, lck,))
			th[x].start()
			x += 1

		for x in range(len(nouns)):
			th[x].join()

		lck.acquire()
		print ('\n')
		for key, val in rel2.items():
			if len(val)==0:
				rel2.pop(key, 0)
				continue
			st = ' '.join(val)
			rel2[key] = st
		lck.release()
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
#	THIS PART MERGES THE TWO DICTIONARIES INTO ONE
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def merge_dictionaries(x, y):
	kvp = {key: ' '.join(list(set().union(x[key].split(),y[key].split()))) for key in x if key in y}
	kvp.update({ k : y[k] for k in set(y) - set(x) })
	kvp.update({ k : x[k] for k in set(x) - set(y) })
	return kvp
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#	CODE FOR MERGING ENDS HERE
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------
'''
	THIS PART CONTAINS THE FUNCTION FOR RUNNING THREADS
'''
# -----------------------------------------------------------------------------

def run_thread(op, sent, lock):
	#sen = sent.translate(None, string.punctuation)
	res = (getDependencyAnalysis(op, sent))
	#res = {}
	res2 = (parsetreeAnalysis(sent))
	#res2 = {}
	kvp = dict()
	if res and res2 and type(res)!=tuple and type(res2)!=tuple:
		kvp = merge_dictionaries(res, res2)
	elif res:
		kvp = res
	elif res2:
		kvp = res2
	
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
		for x in range(len(finalDic)):
			for k,v in finalDic[x].items():
				for word in v.split():
					if word in stopwordList:
						v = re.sub(r"\b%s\b" % word , '', v)

				finalDic[x][k] = v

		print '\n'
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
				sen = sen[:-1]
				org = org[:-1]
				text = re.sub(r"\b%s\b" % org , sen, text)
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
	#text = "The fan above the bed was dirty"
	#text = "I was not provided blanket at night :("
	#text = "We were only given one towel initially"
	#text = "the fan above the bed is dirty"
	#text = "Very limited snacks and food items available."
	#text = "The restaurant serves very reasonably priced and quality cuisine."
	#text = "The food is not good"
	#text = "The bar is decently stocked."
	#text = "The room is good but the service is poor"
	#text = "Courteous staff and overall a value for money."
	#text = "The room was good but the ac was not working"
	#text = "Staff is quite good and managing person is really good person I ever meet in my life (hotel)"
	#text = "smell of cigarettes smoking was there when I entered  rooms should be smelling good and fresh"
	#text = "Staff is quite good and the managing person is a really good person I have ever meet in my life (hotel)"
	#text = "Food was cold but food was good. it should be eaten raw."
	#text = "Food was cold but it was good"
	#text = "the room was clean, beautiful, spacious and good"
	#text = "The room was dirty. New day. Looking for bugs in this part. A regular one."
	#text = "food should be there"
	#text = "there was only one napkin"
	#text = "Only one bedsheet was there"
	#text = "drinks should be cold"
	#text = "More staff should be at reception"
	#text = "There can be extra staff"
	#text = "when I explained to the hotel receptionist about my previous bitter experience, he acknowledged it and gave me a better room in the new wing which was quite good"
	#text = "Helpful office to print materials such as boarding passes and all the front office staff were attentive and got the job done"
	#text = "Lobby was too cluttered and always crowded, Airport-pick-up was not sent by the hotel, inspite of confirmation"
	#text = "The hotel was fully-booked"
	#text = "The room snack just had a 11110/- rupee oreo, 10/- rupee bourbon biscuit, 10/- rupee cashew nut packet for which they billed us 1000/- + taxes which was very shocking."
	#text = "Limitation on free wifi access. Wifi was the worst ever. I could not even make Skype calls. The wifi was very spotty, and as a business traveller, that's my number 1 priority"
	#text = "when i came the 28 % price was more expensive and did not knew that i pay more money for high tax "
	#text = "wifi is as important as having the bed in the room"
	#text = "Free wifi should be available in public areas other than private rooms"
	text = "It took 15 hours to check me in"
	print "Original Text is -> ", text
	clean_txt = cleaner_function(text)
	txt = cr.resolve_coreference_in_text(clean_txt)
	lock = threading.Lock()
	t = [None]*len(txt)
	x = 0
	for sent in txt:
		sen = sent.encode("utf-8")
		op = getCoreNLPAnalysis(sen)
		sen = namedEntityRecognisition(op, sen)
		print "Individual sentence is -> ", sen.encode("utf-8")
		sen = sen.replace("-LRB-", "(")
		sen = sen.replace("-RRB-", ")")
		inp = sen.encode("utf-8")
		t[x] = threading.Thread(target=run_thread, args=(op, inp, lock,))
		t[x].start()
		x += 1

	for x in range(len(txt)):
		t[x].join()
	
	print finalDic

	stopwordList = set(line.strip() for line in open('stopwords.txt'))
	print('-'*110)
	print ("Removing stop words, Final KVP are")
	print remove_stop_words(stopwordList)
	print('-'*100)
# ------------------------------------------------------
'''
	CONGRATS! YOU HAVE ARRIVED AT THE END OF CODE...
'''
# ------------------------------------------------------