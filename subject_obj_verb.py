import os
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree, Tree
from pycorenlp import StanfordCoreNLP
import json

def find_subject(t):    
    for s in t.subtrees(lambda t: t.label() == 'NP'):
        for n in s.subtrees(lambda n: n.label().startswith('NN')):
            return (n[0], find_attrs(n))
            
def find_predicate(t):    
    v = None
    
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label().startswith('VB')):
            v = n
        return (v[0], find_attrs(v))
    
def find_object(t):    
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
            if n.label() in ['NP', 'PP']:
                for c in n.subtrees(lambda c: c.label().startswith('NN')):
                    return (c[0], find_attrs(c))
            else:
                for c in n.subtrees(lambda c: c.label().startswith('JJ')):
                    return (c[0], find_attrs(c))
                
def find_attrs(node):
    attrs = []
    p = node.parent()
    
    # Search siblings
    if node.label().startswith('JJ'):
        for s in p:
            if s.label() == 'RB':
                attrs.append(s[0])
                
    elif node.label().startswith('NN'):
        for s in p:
            if s.label() in ['DT','PRP$','POS','JJ','CD','ADJP','QP','NP']:
                attrs.append(' '.join(s.flatten()))
    
    elif node.label().startswith('VB'):
        for s in p:
            if s.label() == 'ADVP':
                attrs.append(' '.join(s.flatten()))
                
    # Search uncles
    if node.label().startswith('JJ') or node.label().startswith('NN'):
        for s in p.parent():
            if s != p and s.label() == 'PP':
                attrs.append(' '.join(s.flatten()))
                
    elif node.label().startswith('VB'):
        for s in p.parent():
            if s != p and s.label().startswith('VB'):
                attrs.append(s[0])
                
    return attrs

def main(sentence):
    print find_subject(sentence)
    print find_predicate(sentence)
    print find_object(sentence)

if __name__=="__main__" :
    import sys   
    # Parse the example sentence
    sent = 'The dinner is not prepared with precision'
    nlp = StanfordCoreNLP('http://13.127.253.52:9000/')
    output = nlp.annotate(sent, properties={'annotators': 'dcoref','outputFormat':'json'})
    parseTree = output['sentences'][0]['parse']
    parseTree = ParentedTree.convert(Tree.fromstring(parseTree))
    #parseTree.pretty_print()
    main(parseTree)