from snap import *

#DATA STRUCTURES_________________________

#circle names mapped to a list of all the node ids in that circle
circlesDict = dict() #key: "circle13", val: [id1, id2, ...]
#list of all ego node ids
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

#ITERATE OVER EVERY EGO
for ego in egos: 
	#LOAD CIRCLES INTO A MAP
	
	with open("fb_data/facebook/0.circles", "r") as document:
		line = document.readlines()
		print len(line)
		for i in range(len(line)):
			print i
			#split, then erase trailing '/n'
			idList = line[i].split('\t') 
			idList[len(idList)-1] = idList[len(idList)-1].rstrip('\n')
			#set key (remove from array)
			key = idList[0]
			del idList[0]
			#store key and val (array)
			circlesDict[key] = idList
		print circlesDict




#CODE STORAGE BIN
# #LOAD AN EDGE LIST
# circleGraph = LoadEdgeList(PUNGraph, "facebook/0.edges", 0, 1)
# # G = LoadEdgeList(PUNGraph, "SMALL_imdb_actor_edges.tsv", 0, 1)
# print "G: Nodes %d, Edges %d" % (circleGraph.GetNodes(), circleGraph.GetEdges())
