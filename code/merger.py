'''
    Author : Shubham Agrawal
    Roll no: 2019201085
    Institute: IIIT-Hyderabad
'''

import xml.sax
import re
import string
import timeit
import os
from os.path import isfile, join
import sys
from heapq import heapify, heappush, heappop

token_count=0

title_file_name = "title_mapping.txt"
title_file = open(title_file_name, 'r')
title_file.close()

mypath = "index/"
files = os.listdir(mypath)
num_of_files = len(files)

Inverted_Index={}
file_pointer = {}
current_row = {}
words = {}
done=[1]*num_of_files
heap_list = list()
threshold = 100000
multi_level = {}

start_time = timeit.default_timer()

for i in range(num_of_files):
	file_pointer[i] = open(mypath+'inverted_index_'+str(i+1), 'r')
	
	current_row[i] =  file_pointer[i].readline().strip()
	words[i] = current_row[i].split(" ")
	print(words[i][0], words[i][1])
	if words[i][0] not in heap_list:
		heappush(heap_list,words[i][0])



index_file = 0
def write_index():
	global index_file, Inverted_Index, multi_level
	index_file +=1
	first = 1
	ff = open(mypath+'index_'+str(index_file), "w")
	for i in sorted(Inverted_Index):
		if(first == 1):
			multi_level[i] = index_file
			first=0
		data = str(i) + " " + str(Inverted_Index[i]) + "\n"
		ff.write(data)
	ff.close()
	print("Done", index_file)

	


counter=0
while(1):
	if done.count(0) == num_of_files:
		break

	counter+=1
	word = heappop(heap_list)
	for i in range(num_of_files):
		if(done[i] and words[i][0] == word):
			if word in Inverted_Index:
				Inverted_Index[word] += " " + " ".join(words[i][1:])
			else:
				Inverted_Index[word] = " ".join(words[i][1:])


			if(counter == threshold):
				counter=0
				token_count += threshold
				write_index()
				Inverted_Index.clear()

			current_row[i] =  file_pointer[i].readline().strip()

			if not current_row[i]:
				done[i]=0
				file_pointer[i].close()


			else:
				words[i] = current_row[i].split(" ")
				if words[i][0] not in heap_list:
					heappush(heap_list,words[i][0])



write_index()
token_count += counter
print(token_count)
print(counter)
Inverted_Index.clear()
print(index_file)


fm = open(mypath+'multi_level', "w")

for i in sorted(multi_level):
	data = str(i)+" "+str(multi_level[i])+"\n"
	fm.write(data)

fm.close()
print("Done Indexing and Merging")

stop_time = timeit.default_timer()

print("Time Taken(seconds) : ", stop_time - start_time)


#to remove files

for i in range(num_of_files):
	os.remove("index/inverted_index_"+str(i+1))














