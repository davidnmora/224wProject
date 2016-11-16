#FILE DESCRIPTION: Load features, storing in dicts both by
#node Id and by feature Id.
#Because features are represented by integer ids, this file
#creates a dict key to convert between integers and string
#human-readable descriptions ie 77 -> 'education;year;id'

#TO DO:
#1. figure out how to use it as a module/call it from other files
#2. robust way to filter nodes by feature categories
	# get nodes who...
	# a. share a featureId (DONE)
	# b. share a featureDescript (TODO: build descr->id dict)
	# c. share a root category (ie education, work) (TODO: use b., then filter using split)


#RACHEL'S GOAL: look at properties of a networks/cirlces of people
#who all share certain attributes
#what we'll need to do that: 
# load a query for all nodes sharing a certain category of feat 

from snap import *
import numpy as np
import matplotlib.pyplot as plt

#GLOBAL DATA STRUCTURES
featByNId = dict()
nIdsByFeatId = dict()
globIdToDescriptionKey = dict()
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]


#FUNCTIONS________________________________
def loadAnEgoFeat(ego):
	filename = "fb_data/facebook/"+ str(ego) + ".feat"
	with open(filename, "r") as document:
		feat = document.readlines()
	return feat

def parseANodesFeat(nodeFeatStr, locToGlobFeatKey):
	global featByNId
	global nIdsByFeatId
	global globIdToDescriptionKey
	featList = nodeFeatStr.split(' ') 
	featList[len(featList)-1] = featList[len(featList)-1].rstrip('\n')
	nId = int(featList[0])
	del featList[0]
	featSet = set()
	for featIndex in range(len(featList)):		
		if featList[featIndex] == '1':
			featId = locToGlobFeatKey[featIndex]
			featSet.add(featId)
			if featId in nIdsByFeatId:
				nIdsByFeatId[featId].add(nId)
			else:
				nIdSet = set()
				nIdsByFeatId[featId] = nIdSet
	featByNId[nId] = featSet

def loadlocToGlobFeatKey(ego):
	locToGlobFeatKey = dict()
	filename = "fb_data/facebook/"+ str(ego) + ".featnames"
	with open(filename, "r") as document:
		featNames = document.readlines()
	for feat in featNames:
		feat = feat.split(' ')
		locId = int(feat[0])
		globId = int(feat[len(feat)-1].rstrip('\n'))
		locToGlobFeatKey[locId] = globId
		#get feature description string
		featDescript = feat[1][0 : feat[1].rfind(';')]#.split(';')
		globIdToDescriptionKey[globId] = featDescript
	return locToGlobFeatKey

def loadAllFeat():
	for ego in egos: 
		locToGlobFeatKey = loadlocToGlobFeatKey(ego)
		featByNode = loadAnEgoFeat(ego)
		for nodeFeatStr in featByNode:
			parseANodesFeat(nodeFeatStr, locToGlobFeatKey)

def getNodeFeatDescripts(nId):
	nodeFeats = set()
	for featId in featByNId[nId]:
		# print featId
		nodeFeats.add(globIdToDescriptionKey[featId])
		# for featStr in globIdToDescriptionKey[featId]:
		# 	nodeFeats.add(featStr)
	return nodeFeats

def nodeHasFeat(nId, featId):
	
	return featId in featByNId[nId]


loadAllFeat()

#DEMO:
featId = 144
nId = 122
print getNodeFeatDescripts(nId)
print "Feature Ids belonging to node nId: "
print featByNId[nId]
print "Node Ids who have feature featId: "
print nIdsByFeatId[featId]
print "nId has featId (boolean 0 or 1): %d" % nodeHasFeat(nId, featId)
