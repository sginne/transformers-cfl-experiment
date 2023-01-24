grammar_file='/home/sginne/src/transformers.cfl.experiment/CFL.grammar.dataset.1/grammar.txt'
generate_max=5000
#padding_length=100

from nltk.parse.generate import generate
from nltk import CFG
import random
from itertools import chain, repeat, islice
from nltk.parse import RecursiveDescentParser
def generate_random_sentence(tokens,length):
    return_sentence=[]
    #length=length-2
    for i in range(length):
        return_sentence.append(random.choice(tokens))
        
    return return_sentence

def possible_tokens(sentences):
    possible_tokens=set()
    for sentence in sentences:
        for token in sentence:
            possible_tokens.add(token)
    #print("here",possible_tokens)
    return list(possible_tokens)    
def pad_sentences(sentences,padding_length,token='-1'):
    return [list(pad(sentence,padding_length,'-1')) for sentence in sentences]

def to_int_tokens(sentences):
    return_sentences=[]
    for sentence in sentences:
        return_sentence=[]
        #print ('here sent',sentence)
        for token in sentence:
            return_sentence.append(int(token))
        return_sentences.append(return_sentence)
    return return_sentences
def to_str_tokens(sentences):
    return_sentences=[]
    for sentence in sentences:
        return_sentence=[]
        #print ('here sent',sentence)
        for token in sentence:
            return_sentence.append(str(token))
        return_sentences.append(return_sentence)
    return return_sentences

def find_max_length(sentences):
    #print(lst)
    max_sentence_length=-1
    for sentence in sentences:
        if len(sentence)>max_sentence_length:
            max_sentence_length=len(sentence)
    return max_sentence_length

def pad_infinite(iterable, padding=None):
   return chain(iterable, repeat(padding))

def pad(iterable, size, padding=None):
   return islice(pad_infinite(iterable, padding), size)

text_file = open(grammar_file, "r")
grammar=CFG.fromstring(text_file.read())
#print (grammar)
sentences=list(generate(grammar, n=generate_max))
possible_sentences=len(sentences)
padding_length=find_max_length(sentences)

print (f'Grammar yields {len(sentences)} possible sentences, which are padded to {padding_length}')
print ('Some examples')
for example in random.choices(sentences, k=5):
    print(example)
random_sentence=random.choices(sentences, k=1)[0]
print (f'We will take sentence:{random_sentence}, which is parsed to:')
recursive_descent=RecursiveDescentParser(grammar)
for t in recursive_descent.parse(random_sentence):
    print(t)
shuffled_sentence=[token for token in random_sentence]
random.shuffle(shuffled_sentence)

print(f'For checks, after shuffle it gives {shuffled_sentence}, and it doesnt belong to grammar: {len(list(recursive_descent.parse(shuffled_sentence)))==0}')
print('Should be usually True, but shuffling might give valid sentence, and might be False, means we got randomly correct sentence')
available_tokens=possible_tokens(sentences)
#print("here str",available_tokens)
available_tokens=to_int_tokens([available_tokens])[0]
#print("here int",available_tokens)
available_tokens.sort()
#print("here sort",available_tokens)


available_tokens=to_str_tokens([available_tokens])[0]
print (f'And we have possible tokens: {available_tokens}')
print (f'Lets generate sample random sentence with 3 tokens {generate_random_sentence(available_tokens,3)}')
print (f'Ok, lets generate {possible_sentences} WRONG sentences according to grammar, with length 1-{padding_length}')
counter=0
bingo=0
wrong_sentences=[]
while counter<possible_sentences:
    candidate=generate_random_sentence(available_tokens,random.randrange(1, 1+padding_length))
    parsed_candidate=recursive_descent.parse(candidate)
    #print(list(parsed_candidate))
    if len(list(parsed_candidate))==0:
        wrong_sentences.append(candidate)
        counter=counter+1
    else:
        bingo=bingo+1
print (f'We managed to hit {bingo} proper sentences, and didnt take them')
print (f'Here is example of unparsable sentence generated{wrong_sentences[0]}')
#print (find_max_length(wrong_sentences))
padded_sentences=[list(pad(sentence,padding_length,'-1')) for sentence in sentences]
padded_wrong_sentences=[list(pad(sentence,padding_length,'-1')) for sentence in wrong_sentences]


padded_sentences=to_int_tokens(padded_sentences)
padded_wrong_sentences=to_int_tokens(padded_wrong_sentences)
print (f'Ok sentence {padded_sentences[0]}')
print (f'Not ok sentence {padded_wrong_sentences[0]}')