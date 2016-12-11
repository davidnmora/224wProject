from snap import *
import numpy
import copy

egos = [0, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

def communityStrength(graph, vec):
    nodes = [x for x in vec]
    inner = 0
    total = 0
    for nodeId in vec:
        node = graph.GetNI(nodeId)
        for i in range(node.GetOutDeg()):
            neighbor = node.GetNbrNId(i)
            total += 1
            if neighbor in nodes:
                inner += 1
    if total ==0:
        return 1
    else:
        return inner/float(total)

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
    if graph.IsNode(src) and graph.IsNode(dest):
        graph.DelEdge(src, dest)

def formClusters(graph):
    print "num nodes ", graph.GetNodes()
    numComponents = 1
    cluster = -1
    clusterN = -1
#    for i in range(50):
    i = 0
    while numComponents < 9:
#        if numComponents > 7:
#            break
#        if cluster < clusterN or numComponents > 8:
#            print i
#            break
        cluster = clusterN
        removeEdge(graph)
        Components = TCnComV()
        GetSccs(graph, Components)
        numComponents = len(Components)
        if i % 15 == 0:
            clusterN = 0
            for cnCom in Components:
                clusterN += communityStrength(graph, cnCom)
	print i, numComponents
        i += 1
    return graph

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
    print "finished generating"
    return bigNetworks
    
def createEgos(all_networks):
    egonets = [[] for x in range(len(all_networks))]
    for k in range(len(all_networks)):
        net = all_networks[k]
        for i in egos:
            node = net.GetNI(i)
            neighbors = TIntV()
            for i in range(node.GetOutDeg()):
              neighbors.Add(node.GetNbrNId(i))
            egonets[k].append(ConvertSubGraph(PUNGraph, net, neighbors))
            print len(neighbors)
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
    numClusters = []
    centrality = []
    betweenness = []
    closeness = []
    community = []
    for i in j:
        copyi = ConvertGraph(PUNGraph, i)
        formClusters(i)
        Components = TCnComV()
        GetSccs(i, Components)
        numClusters.append(len(Components))
        for cnCom in Components:
            temp = createSubGraph(i, [x for x in cnCom])
            numElements.append(temp.GetNodes())
            numEdges.append(temp.GetEdges())
            clusteringCoefficient.append(GetClustCf(temp))
            maxi = 0
            for node in i.Nodes():
                degCentr = GetDegreeCentr(i, node.GetId())
                if degCentr > maxi:
                    maxi = degCentr
            centrality.append(maxi)
            nodesB = TIntFltH()
            edgesB = TIntPrFltH()
            GetBetweennessCentr(i, nodesB, edgesB, 1.0)
            maxi = 0
            for node in nodesB:
                if nodesB[node] > maxi:
                    maxi = nodesB[node]
            betweenness.append(maxi)
            maxi = 0
            for node in i.Nodes():
                degCentr = GetClosenessCentr(i, node.GetId())
                if degCentr > maxi:
                    maxi = degCentr
            closeness.append(maxi)
            community.append(communityStrength(copyi, cnCom))
    print "number of circles", numpy.std(numClusters), numpy.mean(numClusters)
    print "number of elements: ", numpy.std(numElements), numpy.mean(numElements)
    print "Number of edges", numpy.std(numEdges), numpy.mean(numEdges)
    print "clustering Coefficient: ", numpy.std(clusteringCoefficient), numpy.mean(clusteringCoefficient)
    print "betweenness Coefficient: ", numpy.std(betweenness), numpy.mean(betweenness)
    print "centrality Coefficient: ", numpy.std(centrality), numpy.mean(centrality)
    print "closeness Coefficient: ", numpy.std(closeness), numpy.mean(closeness)
    print "community strenght: ", numpy.std(community), numpy.mean(community)
    print " "
#    print "number of Nodes: ", numElements, "number of edges: ", numEdges, "Clustering Coefficient: ", clusteringCoefficient

