#FILE DESCRIPTION: Loads and performs summary 
#statistics on each ego nodes circles.

from snap import *

#DATA STRUCTURES_________________________
# circlesByEgoId structured as 
# 	egoId: 
# 		circleId: 
# 			circleProps:
# 				NODES_VECTOR,
# 				NODES_SET,
# 				AVG_DEG,
# 				...

circlesByEgoId = dict()
#list of all ego node ids
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]


#CONSTANTS: KEYS FOR DICTS
	#circleProps
CIRCLE_ID = "CIRCLE_ID"
NODES_VECTOR = "NODES_VECTOR"
NODES_SET = "NODES_SET"
AVG_DEG = "AVG_DEG"
AVG_CC = "AVG_CC"
DIAM = "DIAM"
	#circleProps:
		#circleOverlap
CIRCLE_COMPARISON = "CIRCLE_COMPARISON"
IS_SUBSET_OF = "IS_SUBSET_OF"



#FUNCTIONS________________________________
def loadCircles(ego):
	#load circles from file
	filename = "fb_data/facebook/"+ str(ego) + ".circles"
	with open(filename, "r") as document:
		circles = document.readlines()
	return circles
def loadACirclesIds(circle, circles):
	circleNIds = circles[circle].split('\t') 
	circleNIds[len(circleNIds)-1] = circleNIds[len(circleNIds)-1].rstrip('\n')
	circleId = circleNIds[0]
	circleId = int(circleId[len(circleId)-1])
	del circleNIds[0]
	NIdV = TIntV()
	NIdSet = set()
	for strId in circleNIds:
		NIdV.Add(int(strId))
		NIdSet.add(int(strId))
	return (circleId, NIdV, NIdSet)
def loadEgoGraph(ego):
	filename = "fb_data/facebook/" + str(ego) + ".edges"
	egoGraph = LoadEdgeList(PNEANet, filename, 0, 1) #loaded WRONG graph type so ConvertSubGraph() works :P
	print "G: Nodes %d, Edges %d" % (egoGraph.GetNodes(), egoGraph.GetEdges())
	return egoGraph

def loadEachEgosCircles():
	for ego in egos: 
		egoGraph = loadEgoGraph(ego)
		circlesFromAnEgo = dict() 
		circles = loadCircles(ego)
		for circle in range(len(circles)):
			circleProps = dict()
			circleId, NIdV, NIdSet = loadACirclesIds(circle, circles)
			circleProps[CIRCLE_ID] = circleId 
			circleProps[NODES_VECTOR] = NIdV
			circleProps[NODES_SET] = NIdSet
			#GET AVERAGE DEGREE:
			avgDeg = 0
			circleGraph = ConvertSubGraph(PUNGraph, egoGraph, NIdV)
			nCount = circleGraph.GetNodes()
			for node in circleGraph.Nodes():
				avgDeg += node.GetDeg()
			circleProps[AVG_DEG] = avgDeg/float(nCount)
			circleProps[AVG_CC] = GetClustCf(circleGraph)
			circleProps[DIAM] = GetBfsFullDiam(circleGraph, nCount)
			print "avg deg,cc,diam : %d, %d, %d" % (circleProps[AVG_DEG], 100*circleProps[AVG_CC], circleProps[DIAM])

			#final step: store properties of circle in larger structure
			circlesFromAnEgo[circleId] = circleProps
		#calc overlap between circles (now that circles are loaded)
		for circleId in circlesFromAnEgo:
			circleProps = circlesFromAnEgo[circleId]
			circleComparison = dict()
			isSubsetOf = dict()
			for compCircleId in circlesFromAnEgo:
				#CHECK AGAINST EACH OTHER CIRCLE
				compCircleProps = circlesFromAnEgo[compCircleId]
				#is it a subset of another circle?
				isSubsetOf[compCircleId] = circleProps[NODES_SET].issubset(compCircleProps[NODES_SET])
				#TO DO: what's the intersection? percentage intersection?
			circleComparison[IS_SUBSET_OF] = isSubsetOf
			#TO DO: CHECK AGAINST ENTIRE EGO NETWORK
			#what percent of entire network is it?

			#store updated circleProps
			circleProps[CIRCLE_COMPARISON] = circleComparison
			circlesFromAnEgo[circleProps[CIRCLE_ID]] = circleProps

		circlesByEgoId[ego] = circlesFromAnEgo



loadEachEgosCircles() 
# print circlesByEgoId[0]



#CODE STORAGE BIN
