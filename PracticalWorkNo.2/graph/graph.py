import copy


class UndirectedGraph:
    def __init__(self, numberOfVertices, numberOfEdges):
        """
        Initialization of the graph
        :param numberOfVertices: the number of vertices
        :param numberOfEdges: the number of edges
        """
        self._numberOfVertices = numberOfVertices
        self._numberOfEdges = numberOfEdges
        self._dictionaryBound = {}
        self._vertices = []
        for index in range(numberOfVertices):
            self._dictionaryBound[index] = []  # create an empty list for every vertex
            self._vertices.append(index)

    @property
    def vertices(self):
        return self._vertices  # getter for vertices

    @property
    def dictionaryBound(self):  # getter for the list of bound vertices
        return self._dictionaryBound

    @property
    def numberOfVertices(self):  # getter for the number of vertices
        return self._numberOfVertices

    @property
    def numberOfEdges(self):  # getter for the number of edges
        return self._numberOfEdges

    @numberOfEdges.setter
    def numberOfEdges(self, value):  # setter for the number of edges
        self._numberOfEdges = value

    def parseVertices(self):  # iterator for the vertices
        for v in self._vertices:
            yield v

    def parseBound(self, x):  # iterator for the bound vertices
        for y in self._dictionaryBound[x]:
            yield y

    def addVertex(self, x):
        """
        Add a vertex to the graph if it doesn't already exist
        :param x: the vertex to be added
        :return: True if it didn't exist, False otherwise
        """
        if x in self._vertices:
            return False
        self._vertices.append(x)  # add the vertex to the list of vertices
        self._dictionaryBound[x] = []  # initialize the list of bound vertices for x
        self._numberOfVertices += 1  # increase the number of vertices
        return True

    def removeVertex(self, x):
        """
        Remove a vertex from the graph; it must already exist
        :param x: the vertex to be removed
        :return: True if it is removed, False if it doesn't exist
        """
        if x not in self._vertices or x not in self._dictionaryBound.keys():
            return False
        self._vertices.remove(x)  # remove from the list of vertices
        self._dictionaryBound.pop(x)  # remove the key x
        self._numberOfVertices -= 1  # decrease the number of vertices
        for key in self._dictionaryBound.keys():  # remove all occurrences in the bound dictionary
            if x in self._dictionaryBound[key]:
                self._dictionaryBound[key].remove(x)
                self._numberOfEdges -= 1  # decrease the number of edges
        return True

    def degree(self, x):
        """
        Get the degree of a vertex if it exists
        :param x: the vertex for which we get the degree
        :return: the number of bound vertices or -1 if the vertex does not exist
        """
        if x not in self._dictionaryBound.keys():
            return -1
        return len(self._dictionaryBound[x])

    def addEdge(self, x, y):
        """
        Add an edge if it is valid: the vertices exist and the edge does not exist
        :param x: First vertex
        :param y: Second vertex
        :return: False if it can't be added, True otherwise
        """
        if x not in self._vertices or y not in self._vertices:
            return False
        if x == y:
            return False
        if x in self._dictionaryBound[y] and y in self._dictionaryBound[x]:
            return False
        self._dictionaryBound[y].append(x)  # add x to the list of bound vertices for y
        self._dictionaryBound[x].append(y)  # add y to the list of bound vertices for x
        self._numberOfEdges += 1  # increase the number of edges
        return True

    def removeEdge(self, x, y):
        """
        Remove an edge if the vertices exist and the edge exists too
        :param x: First vertex
        :param y: Second vertex
        :return: True if it is removed, False if the vertices don't exist or the edge does not exist
        """
        if x not in self._vertices or y not in self._vertices:
            return False
        if x not in self._dictionaryBound[y] or y not in self.dictionaryBound[x]:
            return False
        self._dictionaryBound[y].remove(x)  # remove x from the bound vertices of y
        self._dictionaryBound[x].remove(y)  # remove y from the bound vertices of x
        self._numberOfEdges -= 1  # decrease the number of edges
        return True

    def findIfEdge(self, x, y):
        """
        Check if there is an edge between two edges
        :param x: the first vertex
        :param y: the second vertex
        :return: False if the vertices don't exist or the edge does not exist, True if the edge exists
        """
        if x not in self._vertices or y not in self._vertices:
            return False
        if x in self._dictionaryBound[y] and y in self._dictionaryBound[x]:
            return True
        return False

    def makeCopy(self):
        """
        Make a copy of the current graph
        :return: the copy
        """
        return copy.deepcopy(self)

    def breathFirstTraversal(self, vertex, visited):
        """
        Traverse the graph with a breath-first algorithm for a given vertex
        :param vertex: the starting vertex
        :param visited: a map to mark the visited vertices
        :return: the connected component with the given vertex as a starting vertex
        """
        queueList = []  # queue for BFS
        connected = []  # this list will contain the connected components
        queueList.append(vertex)  # Add the starting vertex to the queue
        visited[vertex] = True  # Mark the starting vertex as visited
        while queueList:
            x = queueList.pop(0)  # pop the first element from the queue and add it to the list of connected components
            connected.append(x)
            for i in self.dictionaryBound[x]:  # get all the adjacent vertices of the vertex x that are not visited yet
                # mark them and add them to the queue
                if visited[i] is False:
                    queueList.append(i)
                    visited[i] = True
        return connected  # return the connected components

    def findConnectedComponents(self):
        visited = {}
        connected = []  # list of connected comp
        allConnected = []  # all the connected comp
        for vertex in self._vertices:
            visited[vertex] = False  # create a dict used as a map to mark if a vertex is visited
        for vertex in self._vertices:  # find the connected components of the graph by calling BFS for every vertex
            # that is not yet visited
            if visited[vertex] is False:
                connected = self.breathFirstTraversal(vertex, visited)
                allConnected.append(connected)
        return allConnected


def writeGraphToFile(graph, file):
    """
    Write the given graph to a file
    :param graph: the graph to be written
    :param file: the name of the file
    :return: -
    """
    file = open(file, "w")
    firstLine = str(graph.numberOfVertices) + ' ' + str(graph.numberOfEdges) + '\n'
    file.write(firstLine)
    if len(graph.vertices) == 0 and len(graph.dictionaryBound) == 0:
        raise ValueError("There is nothing that can be written!")  # check if there is anything to be written
    edges = []
    for vertex in graph.vertices:  # get the edges, making sure that there are no duplicates
        if len(graph.dictionaryBound[vertex]) != 0:
            for secondVertex in graph.dictionaryBound[vertex]:
                edge = (vertex, secondVertex)
                if (vertex, secondVertex) not in edges and (secondVertex, vertex) not in edges:
                    edges.append(edge)
        else:
            newLine = "{}\n".format(vertex)
            file.write(newLine)
    for edge in edges:  # write the edges to the file
        newLine = "{} {}\n".format(edge[0], edge[1])
        file.write(newLine)
    file.close()


def readGraphFromFile(filename):
    """
    Read a graph from a given file
    :param filename: The name of the file from which the graph will be read
    :return: the new graph
    """
    file = open(filename, "r")
    line = file.readline()
    line = line.strip()
    vertices, edges = line.split(' ')
    graph = UndirectedGraph(int(vertices), 0)  # initialize a new graph
    line = file.readline().strip()
    while len(line) > 0:  # add the edges to the graph, line by line
        line = line.split(' ')
        if len(line) != 1 and int(line[0]) != int(line[1]):  # if the line contains 2 different vertices
            # we can have an edge
            if int(line[0]) not in graph.dictionaryBound[int(line[1])]:
                graph.numberOfEdges += 1
                graph.dictionaryBound[int(line[1])].append(int(line[0]))  # add the edge to the graph
            if int(line[1]) not in graph.dictionaryBound[int(line[0])]:
                graph.dictionaryBound[int(line[0])].append(int(line[1]))  # add the edge to the graph
        line = file.readline().strip()
    file.close()
    return graph
