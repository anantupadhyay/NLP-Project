from gingerit.gingerit import GingerIt

text = "The plac is vary far frm ind"
corr_spell = ""

parser = GingerIt()
print parser.parse(text)['result']

print text
