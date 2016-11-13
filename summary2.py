from snap import *

egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

networks = [TUNGraph.New() for x in egos]
overallNet = TUNGraph.New()
overallNet = LoadEdgeList(PUNGraph, "facebook/total.edges", 0 ,1)
for i in range(len(egos)):
  filename = "facebook/" + str(egos[i])+ ".edges"
  networks[i] = LoadEdgeList(PUNGraph, filename, 0, 1)
  if not overallNet.IsNode(egos[i]):
    overallNet.AddNode(egos[i])
  for node in networks[i].Nodes():
    overallNet.AddEdge(egos[i], node.GetId())
  #print str(networks[i].GetNodes()) + " " + str(networks[i].GetEdges())
networks.append(overallNet)
#print overallNet.GetNodes()

for i in networks:
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


