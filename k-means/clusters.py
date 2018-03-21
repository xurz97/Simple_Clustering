from math import sqrt
def readfile(filename):
    fp = open(filename, "r",encoding="utf-8")
    lines = [line for line in fp.readlines()]
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data
def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0
    return 1.0 - num / den
def juli(v1,v2):
    ret=0
    for i in range(len(v1)):
        ret+=pow(v1[i]-v2[i],2)
    return ret
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
import random
def kcluster(rows,k,distance=juli):
    ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
    clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]
    lastmatches=None
    for t in range(100):
        #print ('Iteration %d' % t)
        bestmatches=[[] for i in range(k)]
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            for i in range(k):
                d=distance(clusters[i],row)
                if d<distance(clusters[bestmatch],row): bestmatch=i
            bestmatches[bestmatch].append(j)
        if bestmatches==lastmatches: break
        lastmatches=bestmatches
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs
    return bestmatches
def scaledown(data, distance=pearson, rate=0.01):
    n = len(data)
    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)]
                for i in range(0, n)]
    # Randomly initialize the starting points of the locations in 2D
    loc = [[random.random(), random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                           for x in range(len(loc[i]))]))
        # Move points
        grad = [[0.0, 0.0] for i in range(n)]
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                # The error is percent difference between the distances
                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]
                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * errorterm
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * errorterm
                # Keep track of the total error
                totalerror += abs(errorterm)
        #print(totalerror)
        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror
        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]
    return loc