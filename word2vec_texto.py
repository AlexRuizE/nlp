""" Perform distributed word2vec using Spark. Input for word2vec are sentences,
so text is partitioned into sentences using regular expressions. Nomenclature and
dictionary keys come from get_content_classes.py."""

import json
import re


# Paths
WK_DIR = '/path/to/working/dir/'
FILE_NAME = 'balsas.json'
with open(WK_DIR+file_name, 'r') as f:
	t = json.load(f)

# Eliminate \xa0
for k in t:
    if isinstance(t[k], dict):
        texto = t[k]['cuerpo_nota']
        t[k]['cuerpo_nota'] = ' '.join(texto.split())

# Clean text and process for word2vec as new line separated full sentences
sentences = [''.join(s) for s in [''.join(t[k]['cuerpo_nota']) for k in t if isinstance(t[k], dict)]]
sentences = ' '.join(sentences) # Single string with all articles
sentences = ''.join([c for c in sentences if c.encode()!=b'\xe2\x80\x9c']) # Eliminate “
punctuation = ',;¿?"~¡!@#$%^&*()_-\\'
sentences = ''.join([c if c not in punctuation else ' ' for c in sentences])
sentences = re.sub('\w+(:) ', '', sentences) # Remove colon that are not time (preserve HH:MM).
sentences = re.sub('  +', ' ', sentences) 
sentences = re.sub(r'(?<=[a-z])(\. )', r'@*@', sentences) # Find all sentence beginnings and substitute for obvious marker.
sentences = sentences.split('@*@')

# Save processed text for distributed ingestion
with open(WK_DIR+'balsas_sentences', 'w') as f:
	for sentence in sentences:
		f.write('{}\n'.format(sentence))

# Word2Vec Distributed Embedding
t = sc.textFile(WK_DIR+'balsas_sentences').map(lambda row: row.split(' '))
word2vec = Word2Vec()
model = word2vec.fit(t)


# # Parameters to fine-tune the vector embedding process:
# word2vec.setLearningRate
# word2vec.setMinCount
# word2vec.setNumIterations
# word2vec.setNumPartitions
# word2vec.setSeed
# word2vec.setVectorSize
# word2vec.setWindowSize