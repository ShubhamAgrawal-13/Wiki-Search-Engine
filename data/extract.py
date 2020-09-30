import os

for i in range(1, 35):
	filename = "xml_" + str(i) + ".bz2"
	command = "bzip2 -dk " + filename
	os.system(command)
	print(i, "Done")
