from pycorenlp import StanfordCoreNLP

def namedEntityRecognisition(text):
	nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
	output = nlp.annotate(text, properties={'annotators': 'ssplit','outputFormat':'json'})
	# for x in range(len(output['sentences'][0]['entitymentions'])):
	# 	tmp = output['sentences'][0]['entitymentions'][x]['text']
	# 	fin = '-'.join(tmp.split())
	# 	text = text.replace(tmp, fin)
	# return text
	print output['sentences'][0]

# def namedEntityRecognisition(text):
# 	nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
# 	output = nlp.annotate(text, properties={'annotators': "tokenize,ssplit,pos,ner,regexner,parse", 'pipelineLanguage': 'en', 'outputFormat':'json'})

# 	rep = []
# 	sen = ""
# 	org = ""
# 	for x in range(len(output['sentences'][0]['tokens'])):
# 		tmp = output['sentences'][0]['tokens'][x]['ner']
# 		if tmp != 'O':	
# 			word = output['sentences'][0]['tokens'][x]['originalText']
# 			org += word + " "
# 			sen += word + "-"
# 		else:
# 			if len(sen) > 1:
# 				#print sen
# 				sen = sen[:-1]
# 				org = org[:-1]
# 				text = text.replace(org, sen)
# 				sen = ""
# 				org = ""

# 	return text

text = "A very beautiful place located in north goa close to Anjuna Beach ."
text = "Narendra Modi is the prime minister of India"
print namedEntityRecognisition(text)