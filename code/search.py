'''
    Author : Shubham Agrawal
    Roll no: 2019201085
    Institute: IIIT-Hyderabad
'''

from sys import argv
import pickle
import timeit
import os
import re
import string
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def remove_punctuation(line):
	return line.translate(str.maketrans('','',string.punctuation))

def isFieldQuery(query_string):
	for ch in query_string:
		if(ch==":"):
			return True
	return False

import timeit
def binary_search(fast_index, word):
	l = -1
	r = len(fast_index)

	while(1+l<r):
		mid = (l+r)//2
		if(fast_index[mid][0] <= word):
			l=mid
		else:
			r=mid

	return l

def binary_search_title(title_index, doc_id):
	l = -1
	r = len(title_index)
	doc_id = int(doc_id)

	while(l+1<r):
		mid = (l+r)//2
		if(title_index[mid][0] <= doc_id):
			l=mid
		else:
			r=mid

	return l


def find_title(title_index, doc_id):
	index = binary_search_title(title_index, doc_id)+1
	f = open('title/title_'+str(index), 'r')
	while(1):
		data = f.readline()
		if not data:
			break
		data = data.strip()
		data = data.split(" ")
		if(data[0]==doc_id):
			#print(word[0], len(data))
			title = " ".join(data[1:-1])
			f.close()
			return title

	f.close()
	# print(index)
	return "Error in fetching document title"

import math
num_of_docs = 9829059

def calculate_tf_idf(tf, df):
	global num_of_docs
	#print(num_of_docs)
	tf = math.log(1+tf)
	idf = math.log(num_of_docs * 1.0 /(1+df))
	return tf*idf
	


# start_time = timeit.default_timer()

multi_level_file = open("index/multi_level","r")
fast_index=[]
while(1):
	data = multi_level_file.readline()
	if not data:
		break
	data = data.strip()
	data = data.split(" ")
	fast_index.append(data)
	# print(data)
multi_level_file.close()

multi_level_title = open("title/multi_level","r")
title_index=[]
while(1):
	data = multi_level_title.readline()
	if not data:
		break
	data = data.strip()
	data = data.split(" ")
	data[0] = int(data[0])
	title_index.append(data)
	# print(data)
multi_level_title.close()


# title_file_name = "title_mapping.txt"
# title_file = open(title_file_name, 'r')
# titles = {}
# while(1):
# 	data = title_file.readline()
# 	if not data:
# 		break
# 	data = data.strip()
# 	data = data.split(" ")
# 	titles[data[0]] = data[1:]
# 	num_of_docs += 1
# title_file.close()
# print("No. of documents : ", num_of_docs)
# print(dump[60000:60005])
# print(len(titles['3']))
# import pickle
# title_file_name = "title_mapping.pkl"
# title_file = open(title_file_name, 'rb')
# titles = {}
# while(1):
# 	try:
# 		data = pickle.load(title_file)
# 		titles[data[0]] = data[1]
# 		num_of_docs += 1
# 	except:
# 		break

# title_file.close()
# print("No. of documents : ", num_of_docs)




#print(calculate_tf_idf(10, 5))
# query = "World Cup Cricket"
# query = "Sachin Ramesh Tendulkar"
# query="t:World Cup i:2019 c:Cricket"
# s="t:the two towers i:1954"
# s="t:shubham agrawal 2099 i:3993 39423 kjshhdf c:d fssfd dsf r:sad wefr ed 10 e:sd saf as"

input_file = argv[1]
fin = open(argv[1], 'r')
fout = open("queries_op.txt", 'w')



while(1):
	line = fin.readline()
	if not line:
		break
	start_time = timeit.default_timer()
	line = line.strip()
	line = line.split(",")
	print(line)

	query = line[1].strip()
	K=int(line[0].strip())

	if(isFieldQuery(query)):
		# print("field_queries")
		data = query.strip().split(" ")
		k={}
		p=-1
		for i in data:
		  item = i.split(":")
		  if(len(item)==2):
		    k[item[0]]=[item[1]]
		    p=item[0]
		  elif(len(item)==1):
		    k[p].append(item[0])
		# print(k)
		words = []
		for k, values in k.items():
			for v in values:
				words.append([v.lower(), k])
		#print(words)
		Inverted_Index={}
		words = [[ stemmer.stem(i[0]), i[1] ]for i in words if i[0] not in stop_words and i[0]!=""]
		print(words)
		for word in words:
			index = binary_search(fast_index, word[0])+1
			f = open('index/index_'+str(index), 'r')
			while(1):
				data = f.readline()
				if not data:
					break
				data = data.strip()
				data = data.split(" ")
				if(data[0]==word[0]):
					#print(word[0], len(data))
					data[0] = word[1]
					Inverted_Index[word[0]] = data
					break

		union = {}
		intersection = {}
		for word in words:
			if word[0] in Inverted_Index:
				type_ = Inverted_Index[word[0]][0]
				for i in range(1, len(Inverted_Index[word[0]])):
					temp = Inverted_Index[word[0]][i].split("|")
					count=0
					df = 0
					for j in temp[1:]:
						if(j[0] == type_ and type_ == 't'):
							cc = j[1:]
							df += 1
							count += int(cc) * 1000

						if(j[0] == type_ and type_ == 'i'):
							cc = j[1:]
							df += 1
							count += int(cc) * 70

						if(j[0] == type_ and type_ == 'c'):
							cc = j[1:]
							df += 1
							count += int(cc) * 70

						if(j[0] == type_ and type_ == 'r'):
							cc = j[1:]
							df += 1
							count += int(cc) * 30

						if(j[0] == type_ and type_ == 'e'):
							cc = j[1:]
							df += 1
							count += int(cc) * 30

						if(j[0] == type_ and type_ == 'b'):
							cc = j[1:]
							df += 1
							count += int(cc) * 10
						
					
					tf_idf = calculate_tf_idf(count, df)
					if temp[0] in union:
						union[temp[0]].append(tf_idf)
					else:
						union[temp[0]] = [tf_idf]


		for doc in union:
			if(len(union[doc]) == len(words)) :
				intersection[doc] = 0
				for v in union[doc]: 
					intersection[doc] += v

		for doc in union:
			values=union[doc]
			union[doc]=0
			for v in values: 
				union[doc] += v

		# print(len(union))
		# print(len(intersection))


		sort_union = sorted(union.items(), key=lambda x: x[1], reverse=True)
		
		sort_intersection = sorted(intersection.items(), key=lambda x: x[1], reverse=True)
		c=0
		for i in sort_intersection:
			# print(i[0], i[1])
			# title = titles[i[0]]
			# title = " ".join(title[:-1])
			# title = find_title(title_index, i[0])
			# title=title.lower()
			# print(i[0],end=", ")
			# print(title, i[1])
			title = find_title(title_index, i[0])
			# title = " ".join(title[:-1])
			title=title.lower()
			fout.write(str(i[0])+", "+str(title)+"\n")
			#print()
			c+=1
			if(c==K):
				break
				# pass

		if(c<K):
			for i in sort_union:
				# print(i[0], i[1])
				# title = find_title(title_index, i[0])
				# title=title.lower()
				# print(i[0],end=", ")
				# print(title, i[1])
				# fout.write(str(i[0])+", "+str(title)+"\n")
				title = find_title(title_index, i[0])
				# title = " ".join(title[:-1])
				title=title.lower()
				fout.write(str(i[0])+", "+str(title)+"\n")
				#print()
				c+=1
				if(c==K):
					break


	else:
		query = query.lower()
		Inverted_Index = {}
		words = [stemmer.stem(i) for i in query.split() if i not in stop_words and i!=""]
		print(words)
		for word in words:
			index = binary_search(fast_index, word)+1
			f = open('index/index_'+str(index), 'r')
			while(1):
				data = f.readline()
				if not data:
					break
				data = data.strip()
				data = data.split(" ")
				if(data[0]==word):
					Inverted_Index[data[0]] = data[1:]
					# print(data[0], len(data))
					break 

		# print(Inverted_Index)
		union = {}
		intersection = {}
		for word in words:
			if word in Inverted_Index:
				for posting_list in Inverted_Index[word]:
					temp = posting_list.split("|")
					count=0
					for j in temp[1:]:
						if(j[0] == "t"):
							cc = j[1:]
							count += int(cc) * 10
						elif(j[0] == "i"):
							cc = j[1:]
							count += int(cc) * 7
						elif(j[0] == "c"):
							cc = j[1:]
							count += int(cc) * 7
						elif(j[0] == "r"):
							cc = j[1:]
							count += int(cc) * 1
						else:
							cc = j[1:]
							count += int(cc) * 1
					df = len(temp) - 1
					tf_idf = calculate_tf_idf(count, df)
					if temp[0] in union:
						union[temp[0]].append(tf_idf)
					else:
						union[temp[0]] = [tf_idf]


		for doc in union:
			if(len(union[doc]) == len(words)) :
				intersection[doc] = 0
				for v in union[doc]: 
					intersection[doc] += v

		for doc in union:
			values=union[doc]
			union[doc]=0
			for v in values: 
				union[doc] += v

		

		# print(union)
		# print(len(union))
		# print(intersection)
		# print(len(union))
		# print(len(intersection))

		sort_intersection = sorted(intersection.items(), key=lambda x: x[1], reverse=True)
		c=0
		for i in sort_intersection:
			# print(i[0], i[1])
			# title = find_title(title_index, i[0])
			# title=title.lower()
			# print(i[0],end=", ")
			# print(title, i[1])
			title = find_title(title_index, i[0])
			# title = " ".join(title[:-1])
			title=title.lower()
			fout.write(str(i[0])+", "+str(title)+"\n")
			# print()
			c+=1
			if(c==K):
				break
				# pass

		sort_union = sorted(union.items(), key=lambda x: x[1], reverse=True)
		
		if(c<K):
			for i in sort_union:
				#print(i[0], i[1])
				# title = find_title(title_index, i[0])
				# title=title.lower()
				# print(i[0],end=", ")
				# print(title, i[1])
				title = find_title(title_index, i[0])
				# title = " ".join(title[:-1])
				title=title.lower()
				fout.write(str(i[0])+", "+str(title)+"\n")
				# print()
				c+=1
				if(c==K):
					break

	stop_time = timeit.default_timer()
	time_taken = stop_time - start_time
	print("Time Taken(seconds) : ", time_taken)
	time_taken = round(time_taken,2)
	fout.write(str(time_taken)+", "+str(round(time_taken/K,2))+"\n")
	fout.write("\n")
	Inverted_Index.clear()

fin.close()
fout.close()



# title_file_name = "title_mapping.txt"
# title_file = open(title_file_name, 'r')
# titles = {}
# dump=[]
# while(1):
# 	data = title_file.readline()
# 	if not data:
# 		break
# 	data = data.strip()
# 	# print(data[0])
# 	data = data.split(" ")
# 	dump.append(data[0])
# 	num_of_docs += 1
# 	# titles.append(data)
# 	# if(len(data)>=3):
# 	titles[data[0]] = data[1:]
# 	# if(int(data[0]) % 100000 == 0):
# 	# 	print(data)
# title_file.close()
# print("No. of documents : ", num_of_docs)
# print(dump[60000:60005])
# print(len(titles['3']))






