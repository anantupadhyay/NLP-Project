import re
import itertools

def cleaner_function(text):

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
	print (text)
	print('-'*100)
	return text

def load_doc(filename):
	# open the file as read only
	file = open(filename, 'r')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text
 
emojis = [(':-J', ' '), ('=^_^=', ' '), (':-o', ' '), ('=-D', ' '), ('>_<', ' '), ('(*_*)', ' '), 
		('>_<*', ' '), ('=)', ' '), ('=(', ' '), (':-p', ' '), (':p', ' '), ('=D', ' '),(':-/', ' '),
		(':/', ' '), ('>-:o', ' '), ('>:o', ' '), ('B)', ' '), ('B-)', ' '), ('8-|', ' '), ('8|', ' '),
		('O:)', ' '), ('O:-)', ' '), ('<3', ' '), (':)', ' '), (':D', ' '), (':(', ' '), (':-)', ' '),
		(':-(', ' '), (':P', ' ')]


filename = 'sample.txt'
text = load_doc(filename)
print type(text)
clean_text = cleaner_function(text)
print type(clean_text)
