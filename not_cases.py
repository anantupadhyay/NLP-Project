from pycorenlp import StanfordCoreNLP
import json

def check_type(data, noun_id):
	nlist = ['NN', 'NNS', 'NNP', 'PRP']
	if data[0]['tokens'][noun_id-1]['pos'] in nlist:
		return True
	return False		

def get_val(data, id):
	li = list()
	extra = ""
	flag = False
	for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
		var = data[0]['enhancedPlusPlusDependencies'][x]
		if var['governor']==id and var['dep']=='neg':
			li.append(var['dependentGloss'])
			li.append(var['governorGloss'])
			flag = True
		elif var['governor']==id and var['dep']=='dobj':
			if (var['dependent']-2)>0 and data[0]['tokens'][var['dependent']-2]['pos'].startswith('JJ'):
				extra += data[0]['tokens'][var['dependent']-2]['word'] + " "
			extra += var['dependentGloss']
		elif var['governor']==id and (var['dep']=='advmod' or var['dep']=='amod'):
			extra += var['dependentGloss'] + ' '
	if flag:
		li.append(extra)
	return li
	
def negDependencyAnalysis(text):
	try:
		output = StanfordCoreNLP('http://13.127.253.52:9000/').annotate(text, properties={'annotators': "tokenize,ssplit,pos,depparse", 'pipelineLanguage': 'en', 'outputFormat':'json'})
		wjson = json.dumps(output['sentences'])
		data = json.loads(wjson)
		neg_dict = dict()
		for x in range(len(data[0]['enhancedPlusPlusDependencies'])):
			var = data[0]['enhancedPlusPlusDependencies'][x]
			if((var['dep'].startswith('nsubj')) and check_type(data, var['dependent'])):
				li = get_val(data, var['governor'])
				if len(li) > 0:
					neg_dict[var['dependentGloss']] = ' '.join(li)
		print neg_dict

	except Exception as err:
		print "Error Occured->", err

text = "I was not provided blanket at night"
text = "ac was not working"
text = "Beach was not that appealing"
text = "We did not like the location"
text = "We did not like the location but the service was good"
text = "bed was not very comfortable"
text = "staff did not provide us complimentary breakfast which was shocking"
text = "Hotel do not provide services like free wifi"
text = "I did not got any service issues while staying at the hotel"
text = "we did not receive frantic call from staff saying to pay"
text = "The hotel did not have sufficient sinage to direct where everything was"
text = "They do not provide things you need to win"
text = "blanket was not given during night saying that there is no staff"
text = "The was no one at the reception_desk"
text = "there is no point booking this hotel"
text = "The fan above the bed was dirty"
text = "I was not provided blanket at night"
text = "Very limited snacks and food items available."
text = "The restaurant serves very reasonably priced and quality cuisine."
text = "The food is not good"
text = "The room was good but the ac was not working"
text = "Food was not cold but food was good. it should be eaten raw."
text = "Food was cold but it was good"
text = "the room was clean, beautiful, spacious and good"
text = "The room was dirty. New day. Looking for bugs in this part. A regular one."
text = "food should not be there"
text = "food was not there"
text = "Lobby was too cluttered and always crowded, Airport-pick-up was not sent by the hotel, inspite of confirmation"
text = "The hotel was not fully-booked"
text = "The room snack just had a 11110/- rupee oreo, 10/- rupee bourbon biscuit, 10/- rupee cashew nut packet for which they billed us 1000/- + taxes which was very shocking."
text = "I could not even make calls."
text = "I did not knew the price when I came"
text = "They did not even give me Invoice for staying with them."
text = "Request was not completely upto the mark"
text = "Beach was not that appealing"
text = "hotel was not the standard of 4.5 star"
text = "bed was not very comfortable"
text = "food was not at all tasty"
text = "The managing person was not a good person"
txt = text.lower().split()
if 'not' in txt:
	negDependencyAnalysis(text)