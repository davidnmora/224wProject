from snap import *

egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

networks = [TUNGraph.New() for x in egos]
overallNet = TUNGraph.New()
overallNet = LoadEdgeList(PUNGraph, "facebook/total.edges", 0 ,1)
for i in range(len(egos)):
	filename = "facebook/" + str(egos[i])+ ".edges"
	graph = networks[i]
	graph = LoadEdgeList(PUNGraph, filename, 0, 1)
	if not overallNet.IsNode(egos[i]):
		overallNet.AddNode(egos[i])
	for node in graph.Nodes():
		overallNet.AddEdge(egos[i], node.GetId())
	print str(graph.GetNodes()) + " " + str(graph.GetEdges())

print overallNet.GetNodes()



