import numpy as np
class NodeImporter:
	def __init__(self, filename):
		self.filename = filename

	def importNode(self):
		file = open(self.filename, "r")
		Data = []
		node = []
		filename = self.filename.split(".")
		if (filename[-1] == "lis" or filename[-1] == "txt"):
			node = self.AnsysImportNode(Data, file)
		elif (filename[-1] == "bdf"):
			node = self.NastranImportNode(Data, file)
		return node

	def AnsysImportNode(self,Data1,file1):
		for line in file1:
			Data1.append(line.split())
		del Data1[0:5]
		Xnode = []
		Ynode = []
		for item in Data1:
			if item==[]:
				a= (Data1.index(item))
				del Data1[a]
		for item in Data1:
			if item[0]=='NODE':
				Data1.remove(item)
		for item in Data1:
			Xnode.append(float(item[1]))
			Ynode.append(float(item[2]))
				#else: print (item)
		Node=np.array([Xnode,Ynode]).T
		return Node

	def NastranImportNode(self,Data1,file1):
		start=0
		end=0
		ilist=[]
		Xnode = []
		Ynode = []
		for line in file1:
			Data1.append(line.split())
		del Data1[0:53]
		#print (len(Data1[-2]))
		for i in range(len(Data1)):
			if (len(Data1[i])<2):
				Data1[i].append(0)
		for item in Data1:
			if item[1]=="Element":
				end=Data1.index(item)
			#print (item)
		for i in range (start,end-1):
			if (Data1[i][0]!="$"):
				Xnode.append(float(Data1[i][3]))
				Ynode.append(float(Data1[i][4]))
		Node=np.array([Xnode,Ynode]).T
		return Node

class ElementImporter:
	def __init__(self, filename):
		self.filename = filename

	def importElement(self):
		file = open(self.filename, "r")
		# fileNode=open("_NodeData.txt","w")
		# a=file.read()
		Data = []
		Element = []
		filename = self.filename.split(".")
		if (filename[-1] == "lis" or filename[-1] == "txt"):
			Element=self.AnsysImportElement(Data, file)
		elif (filename[-1] == "bdf"):
			Element=self.NastranImportElement(Data, file)
		return Element

	def AnsysImportElement(self, Data1, file1):
		for line in file1:
			Data1.append(line.split())
		del Data1[0:5]
		Element = []
		for item in Data1:
			if item == []:
				a = (Data1.index(item))
				del Data1[a]
		for item in Data1:
			if item[0] == 'ELEM':
				Data1.remove(item)
		for item in Data1:
			Element.append([int(item[6]) - 1, int(item[7]) - 1, int(item[8]) - 1, int(item[9]) - 1])
		el = np.zeros((len(Element), 4))
		for i in range(len(Element)):
			for j in range(4):
				el[i, 0] = Element[i][0]
				el[i, 1] = Element[i][1]
				el[i, 2] = Element[i][2]
				el[i, 3] = Element[i][3]
		element = el.astype(int)
		return element

	def NastranImportElement(self, Data1, file1):
		start = 0
		end = 0
		ilist = []
		Element = []
		for line in file1:
			Data1.append(line.split())
		del Data1[0:50]
		# print (len(Data1[-2]))
		for i in range(len(Data1)):
			if (len(Data1[i]) < 2):
				Data1[i].append(0)
		for item in Data1:
			if item[1] == "Element":
				start = Data1.index(item)
			if item[1] == "Property":
				end = Data1.index(item)
		# print (item)
		for i in range(start + 3, end - 1):
			if Data1[i][0] != "$":
				Element.append(
					[int(Data1[i][3]) - 1, int(Data1[i][4]) - 1, int(Data1[i][5]) - 1, int(Data1[i][6]) - 1])
		el = np.zeros((len(Element),4))
		for i in range(len(Element)):
			el[i,:]=Element[i]
		element = el.astype(int)
		return element