# Spam-filter

Using naive bayes classifier technique applied on given training data-set, program is able to filter spam-emails.

## Structure

`corpus.py`  
- contains the `Corpus` class of generator which yields name and content of emails from path-specific folder
  
`utils.py`
- contains the `read_classification_from_file` method which transforms the file of classification (<file_name> <spam/ham>) into dictionary preserving the same information

<b>`naive-bayes-filter.py`</b>  
- contains the `NaiveBaysFilter` class which takes a pattern (can be regular expression) that is applied in it's methods to determine from the training data-set characteristics of spam-emails based on the pattern (and it's "instances") 
  - together with it's methods `train` (concerning the training data-set) and `classify` (concerning the test data-set)
  
<b>`filter.py`</b> 
- contains the `Filter` class which 
  - creates <b>instances of `NaiveBayesFilter` class</b> in it's constructor using a regular-expression pattern for each of an instance (one can be for IP links, other for words written in lower-case...)
  - `train` these instances (via `train` method in `NaiveBayesFilter` and `test` them (via `classify` above)

`confmat.py`  

`quality.py`  






  
