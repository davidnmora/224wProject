#FILE DESCRIPTION: Loads each ego nodes circles, creating 
#nested dicts accessible by constants holding basic
#properties of the circles.

from snap import *
import numpy as np
import matplotlib.pyplot as plt

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
EGO_ID = "EGO_ID"
#circlesByEgoId:
	#circleProps
CIRCLE_ID = "CIRCLE_ID"
NODES_VECTOR = "NODES_VECTOR" #TIntV
NODES_SET = "NODES_SET"
AVG_DEG = "AVG_DEG"
AVG_CC = "AVG_CC"
DIAM = "DIAM"
SUB_GRAPH = "SUB_GRAPH"
#circlesByEgoId:
	#circleProps:
		#circleComparison
CIRCLE_COMPARISON = "CIRCLE_COMPARISON" #currently, just the key to get IS_SUBSET_OF (eventually, will house more entries)
IS_SUBSET_OF = "IS_SUBSET_OF" #set containing all local circle Ids of which given circle is a subset


#FUNCTIONS________________________________
#PUBLIC FUNCTIONS
#to initialize
def loadEachEgosCircles():
	print "LOADING ENTIRE NETWORK..."
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
                        circleProps[SUB_GRAPH] = circleGraph
			nCount = circleGraph.GetNodes()
			for node in circleGraph.Nodes():
				avgDeg += node.GetDeg()
			circleProps[AVG_DEG] = avgDeg/float(nCount)
			circleProps[AVG_CC] = GetClustCf(circleGraph)
			circleProps[DIAM] = GetBfsFullDiam(circleGraph, nCount)
			# print "avg deg,cc,diam : %d, %d, %d" % (circleProps[AVG_DEG], 100*circleProps[AVG_CC], circleProps[DIAM])

			#final step: store properties of circle in larger structure
			circlesFromAnEgo[circleId] = circleProps
		#calc overlap between circles (now that circles are loaded)
		for circleId in circlesFromAnEgo:
			circleProps = circlesFromAnEgo[circleId]
			circleComparison = dict()
			isSubsetOf = set()
			for compCircleId in circlesFromAnEgo:
				#CHECK AGAINST EACH OTHER CIRCLE
				compCircleProps = circlesFromAnEgo[compCircleId]
				#is it a subset of another circle?
				if circleProps[NODES_SET].issubset(compCircleProps[NODES_SET]):
					isSubsetOf.add(compCircleId)
				#TO DO: what's the intersection? percentage intersection?
			circleComparison[IS_SUBSET_OF] = isSubsetOf
			#TO DO: CHECK AGAINST ENTIRE EGO NETWORK
			#what percent of entire network is it?

			#store updated circleProps
			circleProps[CIRCLE_COMPARISON] = circleComparison
			circlesFromAnEgo[circleProps[CIRCLE_ID]] = circleProps

		circlesByEgoId[ego] = circlesFromAnEgo
	print "...LOAD COMPLETE"
	print " "
#for aggregating data
def getDataAt(ego = None, circle = None, circleProp = None, circleCompProp = None):
	result = circlesByEgoId
	if ego in result:
		result = circlesByEgoId[ego]
		if circle in result:
			result = circlesByEgoId[ego][circle]
			if circleProp in result:
				result =  circlesByEgoId[ego][circle][circleProp]
				if circleCompProp:
					result =  circlesByEgoId[ego][circle][circleProp][circleCompProp]
	return result
def getListOfAll(data):
	result = list()
	for egoId in egos:
		if data == EGO_ID:
			result.append(egoId)
		else:
			for circleId in circlesByEgoId[egoId]:
				if data == CIRCLE_ID:
					result.append(circleId)
				else:
					circleProps = circlesByEgoId[egoId][circleId]
					if data == NODES_VECTOR:
						result.append(circleProps[NODES_VECTOR])
					elif data == NODES_SET:
						result.append(circleProps[NODES_SET])
					elif data == AVG_DEG:
						result.append(circleProps[AVG_DEG])
					elif data == AVG_CC:
						result.append(circleProps[AVG_CC])
					elif data == DIAM:
						result.append(circleProps[DIAM])
					elif data == CIRCLE_COMPARISON:
						result.append(circleProps)
					else:
						if data == IS_SUBSET_OF:
							result.append(circleProps[CIRCLE_COMPARISON][IS_SUBSET_OF])
						#add more cirlceComparison props as they're created
	return result
#for aggregating nIds
def getNIdsSetAt(ego = None, circle = None):
	result = set()
	if ego in circlesByEgoId:
		#if circle specified
		if circle in circlesByEgoId[ego]:
			#get the nIds from just that circle
			result = circlesByEgoId[ego][circle][NODES_SET]
			return result
		else:
			#get nIds from every circle
			for circle in circlesByEgoId[ego]:
				result = result.union(circlesByEgoId[ego][circle][NODES_SET])
			return result
	
	#if no parameters are specified, return set of all nodes
	else:
		for ego in circlesByEgoId:
			for circle in circlesByEgoId[ego]:
				result = result.union(circlesByEgoId[ego][circle][NODES_SET])
		return result
def getNIdsTIntVAt(ego = None, circle = None):
	result = TIntV()
	if ego in circlesByEgoId:
		#if circle specified
		if circle in circlesByEgoId[ego]:
			#get the nIds from just that circle
			result = circlesByEgoId[ego][circle][NODES_VECTOR]
			return result
		else:
			#get nIds from every circle
			for circle in circlesByEgoId[ego]:
				result.Union(circlesByEgoId[ego][circle][NODES_VECTOR])
			return result
	
	#if no parameters are specified, return set of all nodes
	else:
		for ego in circlesByEgoId:
			for circle in circlesByEgoId[ego]:
				result.Union(circlesByEgoId[ego][circle][NODES_VECTOR])
		return result		


#PRIVATE HELPER FUNCTIONS
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
	# print "G: Nodes %d, Edges %d" % (egoGraph.GetNodes(), egoGraph.GetEdges())
	return egoGraph






loadEachEgosCircles() 

#DEMO


#DEMO OF DATA QUERYING FUNCTIONS:

#A. retrieve data within the data tree, stored as items in a list
#ie ego 0, circle 4, avg custering coefficient
#print getDataAt(0,3)
#print getDataAt(0, 3, CIRCLE_COMPARISON, IS_SUBSET_OF)
#print " "

#B. aggregates a list of all of one type of data for the entire graph
#ie all egoIds, all avgDeg, a list of all the nodeId vectors
#myData = getListOfAll(AVG_DEG)
#print myData
#print " "
#plt.hist(myData)
#plt.show()

#C. areggates a set/TINtV of all node Ids within a specified region of the graph
# ie passing in egoId, circleId returns all nodes in that circle in that ego
# NOTE: if no parameters are passed, returns all nodes in graph
#print getNIdsSetAt(107, 2)
#print len(getNIdsSetAt(107, 2))
#print getNIdsTIntVAt(107, 2).Len()
