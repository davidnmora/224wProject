#FILE DESCRIPTION: Load features

#plan
# goal: have a dict with key = featureName :  val = set of ids 
# also have a dict with key=nId : val = set of featureNames
# STEPS TO COMPLETE:
# 2. already arranged by nId, to dict, adding index to array when
# ever a 1 is encountered (after deleting first instance)
# 3. create a dictionary of int featurenames keyed to human-readable
# anonymized features

from snap import *
import numpy as np
import matplotlib.pyplot as plt



featuresByNId = dict()
#list of all ego node ids
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]


#FUNCTIONS________________________________
def loadAnEgoFeat(ego):
	filename = "fb_data/facebook/"+ str(ego) + ".feat"
	with open(filename, "r") as document:
		feat = document.readlines()
	return feat

def parseANodesFeat(featStr):
	global featuresByNId
	featList = featStr.split(' ') 
	featList[len(featList)-1] = featList[len(featList)-1].rstrip('\n')
	nId = int(featList[0])
	del featList[0]
	featSet = set()
	for featIndex in range(len(featList)):		
		if featList[featIndex] == '1':
			featSet.add(featIndex)
	featuresByNId[nId] = featSet

def loadGlobalFeatKey(ego):
	filename = "fb_data/facebook/"+ str(ego) + ".featnames"
	with open(filename, "r") as document:
		featNames = document.readlines()
	return featNames

def loadAllFeat():
	for ego in egos: 
		globalFeatKey = loadGlobalFeatKey(ego)
		featByNode = loadAnEgoFeat(ego)
		for featStr in featByNode:
			parseANodesFeat(featStr)


#RUN PROGRAM 
loadAllFeat()
		