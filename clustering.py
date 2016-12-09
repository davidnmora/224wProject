from snap import *
import random

egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

def removeEdge(graph):
    nodesCent = TIntFltH()
    edgesCent = TIntPrFltH()
    GetBetweennessCentr(graph, nodesCent, edgesCent, 1.0)
    maxN = 0
    src = 0
    dest = 0 
    for edge in edgesCent:
	if edgesCent[edge] > maxN:
            maxN = edgesCent[edge]
            src = edge.GetVal1()
            dest = edge.GetVal2()
    graph.DelEdge(src, dest)

def formClusters(graph):
    numComponents = 1
    while numComponents < graph.GetNodes()/5:
        removeEdge(graph)
        Components = TCnComV()
        GetWccs(graph, Components)
        numComponents = len(Components)

def loadNetworks():
    bigNetworks = []
    overallNet = TUNGraph.New()
    for i in range(len(egos)):
        filename = "fb_data/facebook/" + str(egos[i])+ ".edges"
        egoI = TUNGraph.New()
        egoI = LoadEdgeList(PUNGraph, filename, 0, 1)
        if not overallNet.IsNode(egos[i]):
            overallNet.AddNode(egos[i])
        for node in egoI.Nodes():
            if not overallNet.IsNode(node.GetId()):
                overallNet.AddNode(node.GetId())
            overallNet.AddEdge(egos[i], node.GetId())
        for edge in egoI.Edges():
            overallNet.AddEdge(edge.GetSrcNId(), edge.GetDstNId())
    bigNetworks.append(overallNet)
    bigNetworks.append(GenConfModel(overallNet))
    in_degree = TIntV()
    out_degree = TIntV()
    GetDegSeqV(overallNet, in_degree, out_degree)
    in_degree.Sort(False) 
    bigNetworks.append(GenDegSeq(in_degree))
    degree = overallNet.GetEdges() *2 / overallNet.GetNodes()
    bigNetworks.append(GenPrefAttach(overallNet.GetNodes(), degree))
    bigNetworks.append(GenRewire(overallNet, 100))
    bigNetworks.append(GenRndGnm(PUNGraph, overallNet.GetNodes(), overallNet.GetEdges(), False))
    bigNetworks.append(GenSmallWorld(overallNet.GetNodes(), degree, .2))
    print "finished generating"
    return bigNetworks
    
def createEgos(all_networks):
    egonets = [[] for x in range(len(all_networks))]
    for k in range(len(all_networks)):
        net = all_networks[k]
        for i in range(20):
            num = net.GetRndNId()
            node = net.GetNI(num)
            neighbors = TIntV()
            for i in range(node.GetOutDeg()):
              neighbors.Add(node.GetNbrNId(i))
            egonets[k].append(ConvertSubGraph(PUNGraph, net, neighbors))
    print "created egos"
    return egonets

def createSubGraph(graph, nodes):
    temp = TUNGraph.New()
    for i in nodes:
        temp.AddNode(i)
    for i in range(len(nodes)-1):
        for j in range(1, len(nodes)):
            if graph.IsEdge(nodes[i],nodes[j]) or graph.IsEdge(nodes[j],nodes[i]):
                temp.AddEdge(nodes[i],nodes[j])
    return temp

networks = loadNetworks()
egos = createEgos(networks)
for j in egos:
    numElements = []
    numEdges = []
    clusteringCoefficient = []
    for i in j:
        formClusters(i)
        Components = TCnComV()
        GetSccs(i, Components)
        for cnCom in Components:
            #newTInt = TIntV()
            #for m in cnCom:
            #    newTInt.Add(i)
            #temp = ConvertSubGraph(PUNGraph, i, newTInt)
            #print temp.GetNodes()
            temp = createSubGraph(i, [x for x in cnCom])
            numElements.append(temp.GetNodes())
            numEdges.append(temp.GetEdges())
            clusteringCoefficient.append(GetClustCf(temp))
    print "number of Nodes: ", numElements, "number of edges: ", numEdges, "Clustering Coefficient: ", clusteringCoefficient

