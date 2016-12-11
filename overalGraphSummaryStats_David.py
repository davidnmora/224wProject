from snap import *
from gnuplot import *

egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

overallNet = LoadEdgeList(PUNGraph, "fb_data/facebook_combined.txt", 0 ,1)
PlotInDegDistr(overallNet, "example", "Directed graph - in-degree Distribution")
