from circleSummaryStats import * #NOTE: importing any function runs entire file
from loadFeaturesByNId import * #NOTE: importing any function runs entire file


egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]


features = ["work;from", "location", "work;projects", "work;location", "locale", "work;employer", "religion", "hometown", "education;concentration", "education;type", "education;classes", "education;year",  "education;school", "education;degree", "languages", "gender"]

#FUNCTIONS
def getHist(DATA):
  histData = list()
  for data in getListOfAll(DATA):
    histData.append(data)
  plt.hist(histData)
  plt.xlabel(DATA)
  plt.ylabel("Count")
def getXYPlot(NODES_SET, Y):
  x = list()
  y = list()
  for data in getListOfAll(NODES_SET):
    x.append(len(data))
  for data in getListOfAll(Y):
    y.append(data)
  plt.scatter(x,y)
  plt.xlabel("Nodes in the circle")
  plt.ylabel(Y)

# #SUMMARY STATS HIST
plt.subplot(131)
getHist(AVG_CC)
plt.subplot(132)
getHist(AVG_DEG)
plt.subplot(133)
getHist(DIAM)

plt.show()

# #isSubset
# histData = list()
# for data in getListOfAll(IS_SUBSET_OF):
#   histData.append(len(data))
# plt.hist(histData)
# plt.xlabel(IS_SUBSET_OF)
# plt.ylabel("Count")
# plt.show()

# #HISTOGRAM of circle size
# histData = list()
# for nodesSet in getListOfAll(NODES_SET):
#   histData.append(len(nodesSet))
# plt.hist(histData, log=True)
# plt.show()

#PLOT of nodeNum in a circle, Y
plt.subplot(311)
getXYPlot(NODES_SET, AVG_DEG)
plt.subplot(312)
getXYPlot(NODES_SET, AVG_CC)
plt.subplot(313)
getXYPlot(NODES_SET, DIAM)
plt.show()





