from pycorenlp import StanfordCoreNLP

def namedEntityRecognisition(text):
	nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
	output = nlp.annotate(text, properties={'annotators': 'kbp','outputFormat':'json'})
	for x in range(len(output['sentences'][0]['entitymentions'])):
		tmp = output['sentences'][0]['entitymentions'][x]['text']
		fin = '-'.join(tmp.split())
		text = text.replace(tmp, fin)
	return text

text = "Narendra Modi is the prime minister of India"
print namedEntityRecognisition(text)