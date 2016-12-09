from snap import *
from operator import *
import numpy as np
import csv
import random as random

#FUNCTIONS______________________________
def purgeSelfEdges(rewireList):
  hasSelfEdge = True 
  while hasSelfEdge: 
    hasSelfEdge = False
    for i in range(len(rewireList)/2):  
      n1 = rewireList[i*2]
      n2 = rewireList[(i*2)+1]
      if n1 == n2:
        print i
        hasSelfEdge = True
        #swap with element ahead of it
        n3 = rewireList[(i*2)+2]
        rewireList[(i*2)+1] = n3
        rewireList[(i*2)+2] = n2
        # random.shuffle(rewireList)
        # break
  return rewireList
def addEdgePairs(rewireList, G):
  existingNodes = set()
  for i in range(len(rewireList)/2):  
    n1 = rewireList[i*2]
    n2 = rewireList[(i*2)+1]
    if n1 not in existingNodes: 
      G.AddNode(n1)
    if n2 not in existingNodes: 
      G.AddNode(n2)
    G.AddEdge(n1, n2)
    existingNodes.add(n1)
    existingNodes.add(n2)




# Number of Nodes
# Number of Edges
# Clustering Coefficient
# Mean Degree
# Max Centrality
# Max Betweenness
# Max Closeness


  # print "ConfigModel: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges())
def getCCForStubMatch(iterations, G): 
  sumOfAvgCC = 0;
  sumOfMeanDeg = 0;
  sumOfMaxCentrality = 0;
  sumOfMaxBetwenness = 0;
  sumOfMaxCloseness = 0;
  for i in range(iterations): 
    #generate list with a n_i for each degree of n_i
    rewireList = []
    for stub in G.Nodes():
      for halfEdge in range(stub.GetDeg()):
        rewireList.append(stub.GetId())

    #generate config model graph
    random.shuffle(rewireList)
    rewireList = purgeSelfEdges(rewireList)
    configModelG = TNGraph.New()
    addEdgePairs(rewireList, configModelG)

    # add to sum of avg clustering coeff for all graphs   
    sumOfAvgCC += GetClustCf(configModelG, -1)
    sumOfMeanDeg += G.GetEdges()/G.GetNodes()
    
  print sumOfAvgCC/iterations
  print sumOfMeanDeg/iterations
  print sumOfMaxCentrality/iterations
  print sumOfMaxBetwenness/iterations
  print sumOfMaxCloseness/iterations

def getStats(Graph):
  i = Graph
  print i
  maxi = 0
  maxId = 0
  for node in i.Nodes():
    degCentr = GetDegreeCentr(i, node.GetId())
    if degCentr > maxi:
      maxi = degCentr
      maxId = node.GetId()
  print "Centrality: id " + str(maxId) + " " + str(maxi)

  dgBetween = []
  idBetween = []
  nodesB = TIntFltH()
  edgesB = TIntPrFltH()
  GetBetweennessCentr(i, nodesB, edgesB, 1.0)
  maxi = 0
  maxID = 0
  for node in nodesB:
    if nodesB[node] > maxi:
      maxi = nodesB[node]
      maxId = node
  print "Betweenness: id " + str(maxId) + " " + str(maxi)

  maxi = 0
  maxId = 0
  for node in i.Nodes():
    degCentr = GetClosenessCentr(i, node.GetId())
    if degCentr > maxi:
      maxi = degCentr
      maxId = node.GetId()
  print "Closeness: id " + str(maxId) + " " + str(maxi)

#RUN PROGRAM______________________________
G = LoadEdgeList(PUNGraph, "fb_data/facebook_combined.txt", 0, 1)
print "G: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges())

getCCForStubMatch(1, G) 
# getStats(G)





