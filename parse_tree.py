from pycorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree, Tree
import json

def getCoreNLPAnalysis(text):
	try:
		nlp = StanfordCoreNLP('http://13.127.253.52:9000/').annotate(text, properties={'annotators': "parse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		return nlp
	except Exception as err:
		print "Error Occured->",err

def add_to_list(atrb, data):
	for word in data:
		atrb.append(word)
	return atrb 

def check_for_recursion(node, lvl):
	li = ['S', 'SBAR', 'FRAG', 'ROOT', 'PP']
	if lvl==3 or node.label() in li or node.parent().label()=='ROOT' or (lvl==3 and node.label()=='VP'):
		return False
	return True

def commons(node):
	li = []
	vb_check = ['VBN', 'VBP', 'VBZ', 'VBG']
	labels = ['RB', 'RBR', 'CD', 'MD', 'ADVP', 'VB']
	if node.label().startswith('JJ') or node.label() in labels:
		li.append(' '.join(node.flatten()))
	elif node.parent().label()=='VP' or node.parent().label()=='UCP':
		if node.label() in vb_check:
			wrd = (' '.join(node.flatten()))
			li.append(wrd) and wrd.lower()!="is"
	return li

def getfeatures(node):
	atrb = []
	for child in node:
		var = commons(child)
		atrb = add_to_list(atrb, var)
		if child.label() in ['NP', 'VP', 'ADJP', 'QP']:
			var = getfeatures(child)
			atrb = add_to_list(atrb, var)
		elif child.parent().label()=='NP':
			# if(child.label().startswith('NN')):
			# 	atrb.append(' '.join(child.flatten()))
			if child.label()=='DT' and child[0].lower() in ['no', 'not']:
				atrb.append(child[0])
		elif child.parent().label()=='ADJP':
			if child.label() in ['DT', 'IN'] and child.flatten().lower() in ['no', 'not']:
				atrb.append(' '.join(child.flatten()))
	return atrb

def find_attributes(node, lvl, atrb):
	dad = node.parent()
	for sibling in dad:
		if sibling==node:
			continue
		var = commons(sibling)
		atrb = add_to_list(atrb, var)
		if sibling.label() in ['NP', 'VP', 'ADJP', 'QP']:
			var = getfeatures(sibling)
			atrb = add_to_list(atrb, var)
	if check_for_recursion(dad, lvl):
		find_attributes(dad, lvl+1, atrb)

	return atrb

def getParseTreeAnalysis(output):
	parse_tree = output['sentences'][0]['parse']
	tree = ParentedTree.convert(Tree.fromstring(parse_tree))
	#tree.pretty_print()
	rel2 = dict()
	nouns = list()
	for s in tree.subtrees(lambda tree: tree.label().startswith('NN') or tree.label()=='PRP'):
		rel2.setdefault(s[0], [])
		nouns.append(s)
	for s in nouns:
		values = find_attributes(s, 1, [])
		rel2[s[0]] = values
	print rel2

text = "The room is clean"
text = "The fan above bed is dirty"
text = "I was not provided blanket at night"
text = "We were only given one towel initially"
text = "Very limited snacks and food items available"
text = "The restaurant serves very reasonably priced and quality cuisine."
text = "The food is not good"
text = "the bar is decently stocked"
text = "the room is good but the service is poor"
text = "Courteous staff and overall a value for money"
text = "The room was good but the ac was not working"
text = "Staff is quite good and managing_person is really good person I ever meet in my life (hotel)"
text = "smell of cigarettes smoking was there when I entered  rooms should be smelling good and fresh"
text = "Food was cold but the food was good."
text = "the room was clean, beautiful, spacious and good"
text = "food should be there"
text = "there was only one napkin"
text = "Only one bedsheet was there"
text = "drinks should be cold"
text = "there should be more staff at reception"
getParseTreeAnalysis(getCoreNLPAnalysis(text))