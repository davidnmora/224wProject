from snap import *
from circleSummaryStats import *
import csv
egos = [0, 107, 1684, 1912, 3437, 348, 3980, 414, 686, 698]

#TO DO: wrap in "for each ego" loop
for egoId in egos:
  filename = 'ego' + str(egoId) + '.csv'
  with open(filename, 'wb') as csvfile:   
      nodesListCSV = csv.writer(csvfile, delimiter=' ')

      #add header
      nodesListCSV.writerow(["Id"] + ["Circle-Membership"])

      #add each circle to nodes list
      ego = getDataAt(egoId)
      seenNodes = set()
      for circleId in ego:
        for node in ego[circleId]["NODES_SET"]:
          if node not in seenNodes:
            nodesListCSV.writerow([str(node)] + [circleId])
            seenNodes.add(node)
    