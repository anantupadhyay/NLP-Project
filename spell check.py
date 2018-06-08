# # -*- coding: utf-8 -*-

# from gingerit.gingerit import GingerIt

# text = "the got busi working .the got busi working. the got busi working. the got busi working . the got busi working .the got busi working. the got busi working. the got busi working ."
# #text = "Klüft skräms inför på fédéral électoral große"

# parser = GingerIt()
# print parser.parse(text)['result'], '\n'

# #print text


# from googletrans import Translator
# translator = Translator()

# txt = "Klüft skräms inför på fédéral électoral große stüff"
# spell = translator.translate(txt, dest='en')
# op = (spell.text).encode("utf-8")
# print op
from enchant.checker import SpellChecker
chkr = SpellChecker("en_US")
op = "this is sample staf"
chkr.set_text(op)
for err in chkr:
    sug = err.suggest()[0]
    err.replace(sug)

c = chkr.get_text()#returns corrected text
print c

from googletrans import Translator
translator = Translator()
spell = translator.translate(op, dest='en')
opt = (spell.text).encode("utf-8")
print opt