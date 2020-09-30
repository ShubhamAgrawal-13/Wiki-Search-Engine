# Wiki Search Engine


Author : Shubham Agrawal
Roll no: 2019201085
Institute: IIIT-Hyderabad


1. Index Creation:
-----------------

There are 2 file for index creation:
	1. indexer.py
	2. merger.py


I have run it for 10 xmls around 12.2 GB data.

xml_1 size ==> 684 MB
xml_2 size ==> 850 MB
xml_3 to xml_10 around ~1.3 GB

Index_size = 3.1 GB

Number of Index files = 50

each inverted_index file contains around 1 lakh words

Number of tokens(words in index file) = 4,919,324 ( 49*100,000 + 19,324)


Threshold for index creation is 10,000 documents
Threshold for merging and creating new file is 100,000 words

and also I have used your own doc ID scheme.
and created title_mappping.txt for mapping title to doc_id.

Total documents encountered for 12.2 gb data is 1545445.



2. Searching:
-------------
There is one file for Searching:
	1. search.py which takes queries.txt as 1st argument


Method for searching:

I have created secondary index (named multi_level.txt) for fast searching.
and I am using binary search on secondary index (named multi_level.txt) to speed up search.
 
and then, I am searching in the index file which I get from secondary index.

then, calculate tf-idf and then, take union of the result sorted in reverse order by tf-idf score.


Note:
-----
In the stats file, I have approxiated for the 46 gb data according to the 12.2 gb.





