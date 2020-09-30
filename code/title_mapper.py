
import timeit

title_file_name = "title_mapping.txt"
title_file = open(title_file_name, 'r')
titles = {}
num_of_docs=0
threshold = 100000
mypath = "title/"
title_file_no = 0
multi_level={}

def write_title(data):
	global title_file_no, multi_level
	title_file_no +=1
	first = 1
	ff = open(mypath+'title_'+str(title_file_no), "w")
	for i in range(len(data)):
		temp = data[i].split(" ")
		if(first == 1):
			multi_level[int(temp[0])] = title_file_no
			first=0
		ff.write(str(data[i]) + "\n")
	ff.close()
	print("Done", title_file_no)

start_time = timeit.default_timer()

list_docs=[]
while(1):
	data = title_file.readline()
	if not data:
		break
	data = data.strip()
	list_docs.append(data)
	num_of_docs += 1

	if(num_of_docs%threshold == 0):
		write_title(list_docs)
		list_docs=[]


write_title(list_docs)
list_docs=[]
title_file.close()
print("No. of documents/titles : ", num_of_docs)
print("No. of title files : ", title_file_no)

fm = open(mypath+'multi_level', "w")

for i in sorted(multi_level):
	data = str(i)+" "+str(multi_level[i])+"\n"
	fm.write(data)

fm.close()
print("Done Titles Slicing ")

stop_time = timeit.default_timer()

print("Time Taken(seconds) : ", stop_time - start_time)



# import pickle
# title_file_name = "title_mapping.pkl"
# title_file = open(title_file_name, 'wb')

# for k, v in titles.items():
# 	pickle.dump([k, v], title_file)

# title_file.close()


# title_file = open(title_file_name, 'rb')
# c=0
# while(1):
# 	try:
# 		data = pickle.load(title_file)
# 		c+=1
# 		if(c==100000):
# 			print(data)
# 	except:
# 		break

# print(c)

