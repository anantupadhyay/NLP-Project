import re

def replace_escape_characters(foo):
	idx = 1
	while(idx!=-1):
		idx = foo.find('\n')
		#print foo[idx-1]
		if((foo[idx-1]==' ' and foo[idx-2] == '.') or foo[idx-1]=='.'):
			foo = foo.replace('\n', ' ')
		if(foo[idx-1]==' ' and foo[idx-2]!='.'):
			foo = foo.replace(' \n', '. ')
		elif(foo[idx-1]!=' ' and foo[idx-1]!='.'):
			foo = foo.replace('\n', '. ')
	idx = 1
	while(idx != -1):
		#print idx
		idx = foo.find('\t')
		foo = foo.replace('\t', ' ')

	#print (foo)

	#foo = re.sub('\. .', ". ", foo)
	foo = re.sub(' +',' ', foo)
	foo = foo.replace(" .", ".")
	foo = re.sub(r'\.+', ".", foo)						# replacing '...*' with '.'
	foo = re.sub(r'\?+', "?", foo)						# replacing '???*' with '?'
	foo = re.sub(r'\!+', "!", foo)						# replacing '!*' with '!'
	#foo = re.sub(r'\ .', ".", foo)
	#print foo	
	return foo

# import nltk

# text = nltk.word_tokenize("The fan above the bed is dirty")
# tagged_review = []
# tagged_review.append(nltk.pos_tag(text))

# grammar = "NP: {<DT|PP|CD>?<JJ||JJR|JJS>*<NN|NNS|PRP|NNP|IN|PRP\$>+<VBD|VBZ|VBN|VBP|IN>*<JJ|RB>*<PRP|NN|NNS>*}"

# cp = nltk.RegexpParser(grammar)
# #print tagged_review[0]
# results = cp.parse(tagged_review[0])
# #results.draw()
# for result in results:
# 	if type(result) == nltk.tree.Tree:
# 		assoc = []
# 		for res in result:
# 			assoc.append(res[0])
# 		if len(assoc)>=2:
# 			print assoc