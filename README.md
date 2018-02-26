# Natural Language Processing.

This repository holds code to perform natural language processing tasks on documents and other text sources. It contains the following files:

* __preprocess_text.py__: Suite of functions to pre-process text (cleaning html, tokenizing, tfidf, etc) for higher-level NLP processing. It is intended to be imported as a module. User will have to add the *\_\_init\_\_.py* file accordingly to make the module callable. Most of these functions are available in existing NLP packages and can be used by students to understand the logic underlying these modules.

* **get_content_classes.py**: Classes to obtain, process and classify local newspapers in Mexico. Specific publications are all sub-classes of the main class GetText, which should not be used on its own but only as a master template.

* **process_content_classes.py**: Classes to process text obtained with *get_content_classes.py*.

* **word2vec_texto.py**: Perform distributed word2vec using Spark.
