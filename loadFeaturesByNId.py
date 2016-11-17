#FILE DESCRIPTION: Load features, storing in dicts both by
#node Id and by feature Id.
#Because features are represented by integer ids, this file
#creates a dict key to convert between integers and string
#human-readable descriptions ie 77 -> 'education;year;id'

#TO DO:
#1. figure out how to use it as a module/call it from other files

#RACHEL'S GOAL: look at properties of a networks/cirlces of people
#who all share certain attributes
#what we'll need to do that: 
# find most populous features

from snap import *

#GLOBAL DATA STRUCTURES
featByNId = dict()
nIdsByFeatId = dict()
nIdsByFeatDescript = dict()
globIdToDescriptKey = dict()
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]


#FUNCTIONS_______________________________________________

#INITIALIZATION:
#Must be called first. Populates all data structures.
def loadAllFeat():
	for ego in egos: 
		locToGlobFeatKey = loadlocToGlobFeatKey(ego)
		featByNode = loadAnEgoFeat(ego)
		for nodeFeatStr in featByNode:
			parseANodesFeat(nodeFeatStr, locToGlobFeatKey)
	loadNIdsByFeatDescript()

#BUILT FOR RACHEL W/ <3 *****************
# These functions get a set() of all node Ids which...
# a. ...share an specified featureId
def nIdsWithFeatId(featId, optSetOfNIds=set()):
	#if optSetOfNIds specified, filter it
	if optSetOfNIds:
		result = set()
		for nId in optSetOfNIds:
			if nId in nIdsByFeatId[featId]:
				result.add(nId)
	else:
		result = nIdsByFeatId[featId]
	return result
# b. ...share a specified featureDescript, either exactly ("education"->"education") or in part ("education" -> education;type")
def nIdsWithFeatDescript(featDescript, optSetOfNIds=set()):
	result = set()
	#search all description keys of dict, if return the ones containing AT LEAST the input string
	for featDescriptKey in nIdsByFeatDescript:
		#check if featDescript matches the featDescript key, in whole or in part
		
		if featDescript in featDescriptKey:
			#if there's a specififed set, only add things in the specified set
			if optSetOfNIds:
				intersection = optSetOfNIds.intersection(nIdsByFeatDescript[featDescriptKey])
				result = result.union(intersection) 

			#add set of all nodes who have that featDescript
			else:
			
			
				result = result.union(nIdsByFeatDescript[featDescriptKey])


	return result

#"PUBLIC" CLIENT-SIDE FUNCTIONS***********
#returns a boolean based on whether a node has a given feature (IS THIS USEFUL?)
def nodeHasFeat(nId, featId):
	
	return featId in featByNId[nId]
#returns a set() of all featIds of a given nId
def featIdsOfNId(nId):
	return featByNId[nId]




#"PRIVATE" HELPER FUNCTIONS***************
def loadAnEgoFeat(ego):
	filename = "fb_data/facebook/"+ str(ego) + ".feat"
	with open(filename, "r") as document:
		feat = document.readlines()
	return feat
def parseANodesFeat(nodeFeatStr, locToGlobFeatKey):
	global featByNId
	global nIdsByFeatId
	global nIdsByFeatDescript
	global globIdToDescriptKey
	
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
		featDescript = feat[1][0 : feat[1].rfind(';')]
		globIdToDescriptKey[globId] = featDescript
	return locToGlobFeatKey
#creates a dict of key: feat description string, val: nIds with that feature
def loadNIdsByFeatDescript():
	global nIdsByFeatDescript
	loaded = False
	#loop through every featId, [nId, nId...] pair, recalling that multiple featId will match
	for featId in nIdsByFeatId:
		
		#descript = "education;year;id"
		descript = globIdToDescriptKey[featId] 
		#if we've already stored a list with some nodes...
		if descript in nIdsByFeatDescript:
			#add in the new nodes stored at this featId
			nIdsByFeatDescript[descript].union(nIdsByFeatId[featId])
		else:
			#... create a new key for this descript, store nId list there
			nIdsByFeatDescript[descript] = nIdsByFeatId[featId]






#PROGRAM_________________________________________________
loadAllFeat()


#DEMO:
# featId = 144
# nId = 122
# print featIdsOfNId(nId)
# print "Set of Node Ids who have a given featId: "
# print "nId has featId (boolean 0 or 1): %d" % nodeHasFeat(nId, featId)

mySet = set([1, 2, 163, 100, 3586, 3718])

featId = 52
descriptKey = globIdToDescriptKey[featId]
# print descriptKey
# print nIdsByFeatId[featId]
# print "nodes based off featId list: "
# print nIdsByFeatId[featId]


byDescript = nIdsWithFeatDescript(descriptKey)
print len(nIdsWithFeatDescript(descriptKey))
print len(nIdsWithFeatId(featId))
print nIdsWithFeatDescript("work", mySet)
