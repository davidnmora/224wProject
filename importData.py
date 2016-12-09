from snap import *

egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

networks = [TUNGraph.New() for x in egos]
overallNet = TUNGraph.New()
overallNet = LoadEdgeList(PUNGraph, "fb_data/facebook_combined.txt", 0 ,1)
for i in range(len(egos)):
  filename = "fb_data/facebook/" + str(egos[i])+ ".edges"
  networks[i] = LoadEdgeList(PUNGraph, filename, 0, 1)
  if not overallNet.IsNode(egos[i]):
    overallNet.AddNode(egos[i])
  for node in networks[i].Nodes():
    overallNet.AddEdge(egos[i], node.GetId())
  #print str(networks[i].GetNodes()) + " " + str(networks[i].GetEdges())
networks.append(overallNet)
# print overallNet.GetNodes()

print "clustering coefficient"
clusteringCo = []
for i in networks:
  clusteringCo.append(GetClustCf(i, -1))
print clusteringCo

print "mean degree"
meanDeg = []
for i in networks:
  meanDeg.append(i.GetEdges()/float(i.GetNodes()))
print meanDeg

print "degree Distribution"
degDistributions = []
for i in networks:
  degDist = TIntPrV()
  GetDegCnt(i, degDist)
  tempDict = dict()
  for item in degDist:
    tempDict[item.GetVal1()] = item.GetVal2()
  degDistributions.append(tempDict)
  print tempDict



