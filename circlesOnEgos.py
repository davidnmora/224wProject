from snap import *
import numpy
from circleSummaryStats import loadEachEgosCircles
from circleSummaryStats import getDataAt
from loadFeaturesByNId import *

def analysis(network_array):
  print "number of nodes"
  numNodes = []
  for i in network_array:
    numNodes.append(i.GetNodes())
  #print numNodes
  print "standard deviation: " + str(numpy.std(numNodes))
  print "mean: " + str(sum(numNodes)/float(len(numNodes)))
  print "range: " + str(max(numNodes) - min(numNodes))

  print "number of edges"
  numEdges = []
  for i in network_array:
    numEdges.append(i.GetEdges())
  #print numEdges
  print "standard deviation: " + str(numpy.std(numEdges))
  print "mean: " + str(sum(numEdges)/float(len(numEdges)))
  print "range: " + str(max(numEdges) - min(numEdges))

  print "clustering coefficient"
  clusteringCo = []
  for i in network_array:
    clusteringCo.append(GetClustCf(i, -1))
  #print clusteringCo
  print "standard deviation: " + str(numpy.std(clusteringCo))
  print "mean: " + str(sum(clusteringCo)/float(len(clusteringCo)))
  print "range: " + str(max(clusteringCo) - min(clusteringCo))

  print "mean degree"
  meanDeg = []
  for i in network_array:
    meanDeg.append(i.GetEdges()/float(i.GetNodes()))
  #print meanDeg
  print "standard deviation: " + str(numpy.std(meanDeg))
  print "mean: " + str(sum(meanDeg)/float(len(meanDeg)))
  print "range: " + str(max(meanDeg) - min(meanDeg))

  #print "degree Distribution"
  #degDistributions = []
  #for i in network_array:
  #  degDist = TIntPrV()
  #  GetDegCnt(i, degDist)
  #  tempDict = dict()
  #  for item in degDist:
  #    tempDict[item.GetVal1()] = item.GetVal2()
  #  degDistributions.append(tempDict)
  #  print tempDict


loadEachEgosCircles()
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]
'''
for ego in egos:
  print "EGO "+ str(ego)
  circles = getDataAt(ego)
  print "num circles: " + str(len(circles))
  subgraphs = []
  for i in range(len(circles)):
    subgraphs.append(getDataAt(ego, i, "SUB_GRAPH"))
  analysis(subgraphs)
'''

loadAllFeat()
features = ["work;from", "location", "work;projects", "work;location", "locale", "education;concentration", "work;employer", "religion", "hometown", "education;type", "education;classes", "education;year", "languages", "education;school", "gender", "education;degree"]
for feat in features:
  print "-----------FEATURE " + feat
  subgraphs = []
  for ego in egos:
    circles = getDataAt(ego)
    for i in range(len(circles)):
      setOfNodes = set(getDataAt(ego, i, "NODES_VECTOR"))
      if len(nIdsWithFeatDescript(feat, setOfNodes)) > len(getDataAt(ego, i, "NODES_VECTOR")) * .8:
        subgraphs.append(getDataAt(ego, i, "SUB_GRAPH"))
  if len(subgraphs) > 0:
    print "number of circles: " + str(len(subgraphs))
    analysis(subgraphs)
  


