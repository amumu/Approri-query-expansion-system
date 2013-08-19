#encoding=utf-8
import jieba, re, string
testDict = "C:/dataset/dict/dict.txt.big"jieba.load_userdict(testDict)
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#jieba.set_dictionary(testDict)
import jieba.posseg as pseg


############# give the list of CT per query, output: [segC1,segC2, segC3, segt1.....etc ] ####################
def segmentCTListPerQuerys(list_CT_Query):
	segCTStringInAQuery= []
	allLinePerQuery = []
	for line in list_CT_Query:
		out1 = re.sub('[a-zA-Z]+', '', line)       
		out1 = re.sub('[%s]' % re.escape(string.punctuation), '', out1)
		segline = pseg.cut(out1.decode("utf-8"))
		allLinePerQuery.append(segline)
	for line in allLinePerQuery:
		seglinePerQuery = []
		for z in line:
			if z.flag == "n" or z.flag == "ns" or z.flag == "v" or z.flag == "a" or z.flag == "nr" or z.flag == "nz" or z.flag == "i":
				seglinePerQuery.append(z.word)
		seglineString = ' '.join(e for e in seglinePerQuery)
		segCTStringInAQuery.append(seglineString)
	return segCTStringInAQuery def segmentToListPerQuery(queryString):
	listPerQuery = []
	segedList = []
	out1 = re.sub('[a-zA-Z]+', '', queryString)       
	out1 = re.sub('[%s]' % re.escape(string.punctuation), '', out1)
	#segString = pseg.cut(queryString.decode("utf-8"))
	segString = pseg.cut(queryString)
	#segString = jieba.cut(queryString,cut_all=False)
	#print ".. ".join(segString)
	#for i in segString:
	#	listPerQuery.append(i)

	for z in segString:
		#print z.word + "\n"
		#if z.flag == "n" or z.flag == "ns" or z.flag == "v" or z.flag == "t" or z.flag == "a" or z.flag == "nr" or z.flag == "nz" or z.flag == "i" or z.flag == "m":
		if z.flag != "x":
			#segedList.append(z.word.encode("utf-8"))
			segedList.append(z.word)
	return segedList

############# input: referenceFileName, folder contains webqueery result files ####################def segementThroughFile(refFileName, testfolder):

	fp7=open(refFileName,"r")
	data_list = [word.strip() for word in fp7]
	data_list
	for i in data_list:
		print "==== current processed file ===="
		print i
		query = i
		testFile1 = testfolder + str(query).decode("utf-8") + ".all"

		a = []  
		for line in open(testFile1):
			out = re.sub('[a-zA-Z]+', '', line)
			out = re.sub('[%s]' % re.escape(string.punctuation), '', out)
			words = jieba.cut(out.decode("utf-8"))
			a.append(words)
		b= []
		for line1 in open(testFile1):
			out1 = re.sub('[a-zA-Z]+', '', line1)       
			out1 = re.sub('[%s]' % re.escape(string.punctuation), '', out1)
			words1 = pseg.cut(out1.decode("utf-8"))
			b.append(words1)
		f = []
		for line2 in open(testFile1):
			out2 = re.sub('[a-zA-Z]+', '', line2)
			out2 = re.sub('[%s]' % re.escape(string.punctuation), '', out2)
			words2 = pseg.cut(out2.decode("utf-8"))
			f.append(words2)
        
		output = testfolder + str(query).decode("utf-8") + ".output1" 
		output_file_1 = open(output, 'w')
		output1 = testfolder + str(query).decode("utf-8") + ".output2"    
		output_file_2 = open(output1, 'w')
		output2 = testfolder + str(query).decode("utf-8") + ".output3"    
		output_file_3 = open(output2, 'w')

    
		for i in a:
			for j in i:
				output_file_1.write(j.encode("utf-8") + " ")
		output_file_1.close()
	
		for c in b:
			for z in c:
        #output_file_2.write(z.encode("utf-8") + " ")
        #if z.flag != "uj" or "ud" or "x" or "c" or "m" or "y":
        #if "n" or "ns" or "v" or "t" or "a" in z.flag:
				if z.flag == "n" or z.flag == "ns" or z.flag == "v" or z.flag == "t" or z.flag == "a" or z.flag == "nr" or z.flag == "nz" or z.flag == "i" or z.flag == "m":
        #if z.flag != "uj" or z.flag != "ud" or z.flag != "x" or z.flag != "c" or z.flag != "m" or z.flag != "y":
					output_file_2.write(z.word.encode("utf-8") + " ")
			output_file_2.write('\n')
		output_file_2.close()
    
		for e in f:
			for h in e:
				output_file_3.write(h.encode("utf-8") + " ")
        #if z.flag != "uj" or "ud" or "x" or "c" or "m" or "y":
        #if "n" or "ns" or "v" or "t" or "a" in z.flag:
        #if z.flag == "n" or z.flag == "ns" or z.flag == "v" or z.flag == "t" or z.flag == "a" or z.flag == "nr" or z.flag == "nz" or z.flag == "i":
        #if z.flag != "uj" or z.flag != "ud" or z.flag != "x" or z.flag != "c" or z.flag != "m" or z.flag != "y":
            #output_file_3.write(z.word.encode("utf-8") + " ")
    #output_file_2.write('\n')
		output_file_3.close()

	fp7.close()




