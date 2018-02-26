"""Classes to process text obtained with get_content_classes.py."""

import os
import json

class ProcessText():
    def __init__(self):
        self.raw_lemmas = 'data/lemmatization-es.txt' # www.lexiconista.com/datasets/lemmatization/

    def load_raw_data(self, path_to_dict):
        """Load existing raw data, if exists."""
        if os.path.exists(path_to_dict):
            with open(path_to_dict, 'r') as f:
                return json.load(f)
        else:
            raise RuntimeError('File does not exist.')

    def load_processed_data(self, path_to_dict):
        """Load existing processed data, if exists."""
        if os.path.exists(path_to_dict):
            with open(path_to_dict, 'r') as f:
                return json.load(f)
        else:
            return {}

    def dump_text(self, content, file_path):
        """Move raw text from json to text file for processing."""
        with open(file_path,'w') as f:
            f.write(content)


    def remove_punctuation(self, a_string):
        """Completevely remove punctuation, make lowercase, etc."""
        good_punctuation = re.compile('\'')
        punctuation = re.sub(good_punctuation, '', string.punctuation) + u"\u2018" + u"\u2019" + u"\u201D" + u"\u201C"  + u"\u2014" + u"\u2013"
        a_string = re.sub('-',u' ', a_string) # Hyphenation
        a_string = re.sub('/',u' ', a_string)
        a_string = ''.join(char for char in a_string if char not in punctuation)
        a_string = re.sub('\s{2,}',u' ', a_string)
        a_string = re.sub('\'s',u'', a_string)
        return a_string

    def lemma_dict(self):
        with open(self.raw_lemmas, 'r') as f:
            lemmas = f.read()
        lemmas = lemmas.splitlines()
        lemmas = [lemma.split('\t') for lemma in lemmas]
        return {lemma[1]:lemma[0] for lemma in lemmas}

    def save_data(self, processed, path_processed):
        with open(path_processed, 'w') as f:
            json.dump(processed, f)
