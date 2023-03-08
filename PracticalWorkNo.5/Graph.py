import copy
from queue import PriorityQueue
from math import inf
import itertools


class Graph:
    def __init__(self, nr_of_vertices, nr_of_edges):
        self._number_of_vertices = nr_of_vertices
        self._number_of_edges = nr_of_edges
        self._dictionary_for_in = {}
        self._dictionary_for_out = {}
        self._dictionary_costs = {}
        for i in range(nr_of_vertices):
            self._dictionary_for_in[i] = []
            self._dictionary_for_out[i] = []

    @property
    def get_the_number_of_vertices(self):
        return self._number_of_vertices

    @property
    def get_the_number_of_edges(self):
        return self._number_of_edges

    @property
    def get_the_dictionary_for_in(self):
        return self._dictionary_for_in

    @property
    def get_the_dictionary_for_out(self):
        return self._dictionary_for_out

    @property
    def get_dictionary_costs(self):
        return self._dictionary_costs

    def parse_vertices(self):
        list_of_vertices = list(self._dictionary_for_in.keys())
        for vertex in list_of_vertices:
            yield vertex

    def add_given_edge(self, first, second, cost):
        if first in self._dictionary_for_in[second]:
            return False
        elif second in self._dictionary_for_out[first]:
            return False
        elif (first, second) in self._dictionary_costs.keys():
            return False
        self._dictionary_for_in[second].append(first)
        self._dictionary_for_out[first].append(second)
        self._dictionary_costs[(first, second)] = cost
        self._number_of_edges += 1
        return True

    def retrieve_cost(self, start, end):
        if self.check_if_edge_between_vertices(start, end):
            return self._dictionary_costs[(start, end)]

    def check_if_edge_between_vertices(self, first_one, second_one):
        if first_one > self._number_of_vertices or second_one > self._number_of_vertices:
            raise ValueError(" The vertices does not exist, please enter valid vertices. ")
        elif first_one in self._dictionary_for_in[second_one]:
            return self._dictionary_costs[(first_one, second_one)]
        elif second_one in self._dictionary_for_out[first_one]:
            return self._dictionary_costs[(first_one, second_one)]
        else:
            return False

    def parse_edges_outbound(self, given_vertex):
        for i in self._dictionary_for_out[given_vertex]:
            yield i

    def parse_edges_inbound(self, given_vertex):
        for i in self._dictionary_for_in[given_vertex]:
            yield i

    def get_vertex_in_degree(self, given_vertex):
        if given_vertex not in self._dictionary_for_in.keys():
            return False
        return len(self._dictionary_for_in[given_vertex])

    def get_vertex_out_degree(self, given_vertex):
        if given_vertex not in self._dictionary_for_out.keys():
            return False
        return len(self._dictionary_for_out[given_vertex])

    def parse_keys(self):
        """returns a copy of all the vertex keys"""
        return list(self._dictionary_for_out.keys())

    def modify_the_cost_of_given_edge(self, first_vertex, second_vertex, new_cost):
        if (first_vertex, second_vertex) not in self._dictionary_costs.keys():
            return False
        self._dictionary_costs[(first_vertex,second_vertex)] = new_cost
        return True

    def remove_an_edge(self, first, second):
        if first not in self._dictionary_for_in.keys():
            return False
        elif second not in self._dictionary_for_out.keys():
            return False
        elif (first, second) not in self._dictionary_costs.keys():
            return False
        elif first not in self._dictionary_for_in[second]:
            return False
        elif second not in self._dictionary_for_out[first]:
            return False
        self._dictionary_for_in[second].remove(first)
        self._dictionary_for_out[first].remove(second)
        self._dictionary_costs.pop((first, second))
        self._number_of_edges -= 1
        return True

    def add_vertex(self, given_vertex):
        if given_vertex in self._dictionary_for_in.keys() and given_vertex in self._dictionary_for_out.keys():
            return False
        self._dictionary_for_in[given_vertex] = []
        self._dictionary_for_out[given_vertex] = []
        self._number_of_vertices += 1
        return True

    def remove_vertex(self, given_vertex_to_be_removed):
        if given_vertex_to_be_removed not in self._dictionary_for_in.keys() or given_vertex_to_be_removed not in self._dictionary_for_out.keys():
            return False
        self._dictionary_for_in.pop(given_vertex_to_be_removed)
        self._dictionary_for_out.pop(given_vertex_to_be_removed)
        for key in self._dictionary_for_in.keys():
            if given_vertex_to_be_removed in self._dictionary_for_in[key]:
                self._dictionary_for_in[key].remove(given_vertex_to_be_removed)
            elif given_vertex_to_be_removed in self._dictionary_for_out[key]:
                self._dictionary_for_out[key].remove(given_vertex_to_be_removed)
        new_list = list(self._dictionary_costs.keys())
        for el in new_list:
            if el[0] == given_vertex_to_be_removed or el[1] == given_vertex_to_be_removed:
                self._dictionary_costs.pop(el)
                self._number_of_edges -= 1
        self._number_of_vertices -= 1
        return True

    def copy_the_graph(self):
        return copy.deepcopy(self)

    def find_shortest_path(self, starting_given_vertex, ending_given_vertex):
        """
        This function finds the shortest path between the given vertices, starting_index_vertex and ending_index_vertex
        in the current graph, and returns the list of vertices along the path, starting with the starting_given_vertex
        and ending with the ending_given_vertex. If the starting_given_vertex == ending_given_vertex
        it returns [starting_given_vertex]. If the given vertices are invalid it prints a corresponding message.
        :param starting_given_vertex: the vertex given by the user for the start of the path
        :param ending_given_vertex: the vertex given by the user for the end of the path
        :return: the list of vertices along the path, from the starting_given_vertex to the ending_given_vertex
        """
        if ending_given_vertex >= self._number_of_vertices or starting_given_vertex >= self._number_of_vertices:
            raise ValueError(" The inserted vertices are invalid! ")   # we check firstly if the inserted vertices are valid
        parents = self.breadth_first_search(starting_given_vertex)         # intialize the parents dictionary using bfs
        path = []
        vertex = ending_given_vertex
        while vertex != starting_given_vertex:
            path.append(vertex)
            if vertex not in parents.keys():
                raise ValueError("There is no possible path between the vertices. ")
            vertex = parents[vertex]
        path.append(starting_given_vertex)
        path.reverse()
        return path

    def breadth_first_search(self, start_vertex):
        """
        This function does a BFS parsing from the start vertex int the graph
        :param start_vertex: the given starting vertex for the path
        :return: a dictionary where the keys are the accessible vertices and the value is the parent in the BFS for each
                 vertex. Parent of the start_vertex should be None.
        """
        queue = list()
        parents = dict()
        queue.append(start_vertex)
        parents[start_vertex] = None     # the value of the starting vertex is None

        while len(queue)>0:
            current_vertex = queue.pop(0)
            nout = self.parse_edges_outbound(current_vertex)  # parsing the vertices outbound in order to take the values for the keys
            for vertex in nout:
                if vertex not in parents:                             # we take the vertices if they are not already in
                    queue.append(vertex)                                  # parents dictionary
                    parents[vertex] = current_vertex
        return parents                       # we return the parents dictionary in order to take the path from it

    def minimum_cost_path(self, vertex_begin, vertex_end):
        """
        Compute the minimum cost path of a graph from a vertex to another
        :param vertex_begin: first vertex
        :param vertex_end: second vertex
        :return: the cost of the minimum cost path and the path in reverse order
        """
        dist = {}  # dictionary that associates to each accessible vertex the cost of the minimum cost walk
        # from begin to end we know so far
        pred = {}  # dictionary that associates to each accessible vertex its predecessor on the path
        inf = float('inf')
        for vertex in self.parse_keys():
            dist[vertex] = inf  # initialise all the distances as infinite
            pred[vertex] = -1  # initialise all the predecessors on the path
        dist[vertex_begin] = 0  # initialise the starting vertex
        changed = True
        while changed:                        # the while stops when when we find the minimum distance for every current
            changed = False                   # edge
            for (x, y) in self._dictionary_costs.keys():  # for every edge, check if the distance is minimum
                # if it is, added to the path and update the distance to the vertex y from the starting vertex
                if dist[y] > dist[x] + self._dictionary_costs[(x, y)] and dist[x] != inf:
                    dist[y] = dist[x] + self._dictionary_costs[(x, y)]
                    pred[y] = x
                    changed = True
        # the algorithm stops when all the edges are checked and all the distances from the starting vertex are min

        # check for negative weight cycles
        # if we get a shorter path, then there is a cycle
        for (x, y) in self._dictionary_costs.keys():
            if dist[y] > dist[x] + self._dictionary_costs[(x, y)] and dist[x] != inf:
                raise ValueError("Graph contains a negative weight cycle!")

        # compute the path backwards from the end vertex
        path = []
        vertex = vertex_end
        path.append(vertex)  # append to the path the ending vertex
        while pred[vertex] != -1:
            path.append(pred[vertex])
            vertex = pred[vertex]
        return dist[vertex_end], path  # returns the total cost and the path

    def HamiltonianCycle(self):
        """
        this function determines the hamiltonian cycles(visits each node exactly once) that are in the graph and decides which one has the lowest cost
        :return: the hamiltonian cycle with the lowest cost
        """
        l = [x for x in self._dictionary_for_in.keys()]   # we take all the vertices that have edges and perform
        p = list(itertools.permutations(l))                      # permutations
        x = p[0][0]
        minimum_cost = inf
        sol = []
        for i in p:      # parse through all the permutations
            if i[0] != x:                 # if the current permutation does not start with the first vertex, break
                break

            aux_cost = 0
            ok = 1  # we suppose that there is a hamiltonian cycle
            for j in range(1, len(i)):
                n = i[j - 1]
                m = i[j]
                # checking to see if there is an edge between the two
                # in case there isn't, we break

                if self.check_if_edge_between_vertices(n, m) == 0:
                    ok = 0
                    break

                aux_cost += self.retrieve_cost(n, m)

            if ok == 0:
                continue

            if self.check_if_edge_between_vertices(i[0], i[len(i) - 1]) == 0:     # check if edge between first and last
                ok = 0
            else:
                aux_cost += self.retrieve_cost(i[0], i[len(i) - 1])             # add cost if exists

            if ok == 1:
                for k in i:                                # if found a solution print the existing sol
                    print(str(k) + " ", end="")
                print(str(i[0]) + " of cost: " + str(aux_cost))
                if aux_cost < minimum_cost:                     # check if the current cost smaller than min cost and
                    minimum_cost = aux_cost                       # take the current permutation as the main solution
                    sol = i

        return minimum_cost, sol


class UndirectedGraph:        # new class for the undirected graph
    def __init__(self, vertices):
        self.vertices = dict()
        for i in vertices:
            self.vertices[i] = set()

    def add_edge(self, x, y):
        self.vertices[x].add(y)
        self.vertices[y].add(x)

    def is_edge(self, x, y):
        return (y in self.vertices[x])

    def parse_vertices(self):
        vertices_list = list()
        for key in self.vertices:       # function to parse the vertices of the undirected graph
            vertices_list.append(key)
        return vertices_list

    def parse_n(self, x):
        n_vertices = list()     # function to get the vertices with which the given vertex forms an edge
        for y in self.vertices[x]:
            n_vertices.append(y)
        return n_vertices


def print_graph(g):         # prints the undirected graph on the screen
    print("Neighbors:")
    for x in g.parse_vertices():
        s = str(x) + ":"
        for y in g.parse_n(x):
            s = s + " " + str(y)
        print(s)


def create_graph_and_cost():
    """
    :return: this function creates an undirected graph
    """
    g = UndirectedGraph(range(1, 7))
    cost1 = {
        (1, 2): 1,
        (1, 3): 2,
        (1, 4): 3,
        (1, 6): 2,
        (2, 6): 1,
        (3, 4): 4,
        (3, 5): 3,
        (3, 6): 2,
        (4, 5): 1,
        (5, 6): 5,
    }
    # cost1 = {
    #     (1, 2): 3,
    #     (1, 3): 2,
    #     (1, 4): 4,
    #     (2, 3): 2,
    #     (2, 6): 1,
    #     (3, 4): 4,
    #     (3, 5): 3,
    #     (3, 6): 2,
    #     (4, 5): 5,
    #     (5, 6): 5,
    # }
    cost = {}
    for edge in cost1.keys():
        g.add_edge(edge[0], edge[1])   # adds the edge to the graph
        cost[edge] = cost1[edge]
        cost[(edge[1], edge[0])] = cost1[edge]
    return g, cost


class DisjointSets:
    def __init__(self, vertices):
        self.parents = {x: x for x in vertices}
        self.heights = {x: 0 for x in vertices}

    def checkAndJoin(self, x, y):
        """If x and y are in the same component, returns False. If they are in distinct components,
        joins the components and returns True
        """
        rootX = self.getRoot(x)     # we get each corresponding root for the given x and y
        rootY = self.getRoot(y)
        if rootX == rootY:                # if they are the same we return false
            return False
        else:
            if self.heights[rootX] < self.heights[rootY]:  # if the height corresponding to root x is less than the one
                self.parents[rootX] = rootY                 # to y we init the parent root x with root y
            elif self.heights[rootY] < self.heights[rootX]:  # if the height corresponding to root y is less than the
                self.parents[rootY] = rootX                  # one to x we init the parent root y with root x
            else:
                self.parents[rootX] = rootY                # otherwise we init the parent root x with root y
                self.heights[rootY] += 1                   # increment the height root y
            return True

    def getRoot(self, x):           # function to return the root corresponding to the list of parents for the given x
        foundParent = self.parents[x]
        while self.parents[foundParent] != foundParent:
            foundParent = self.parents[foundParent]
        return foundParent


def kruskal(g, cost):
    """Returns a list of edges forming a minimum spanning tree
     The idea is to start with a graph with all the vertices and no edges, and then to add edges that do not close
    cycles. This way, as the algorithm progresses, the graph will consist in small trees (it will be what is called a
    forest - a graph with no cycles, meaning that its connected components are trees), and those trees are joined
    together to form fewer and larger trees, until we have a single tree spanning all the vertices. In doing all the
    above, we use the edges in increasing order of their cost.
    """
    edges = list()  # we initialize the list of the edges
    disjointSets = DisjointSets(g.parse_vertices())  # we get the corresponding DisjointSets initialising by parsing
    for vertex in g.parse_vertices():                               # the vertices of the current undirected graph
        for neighbour in g.parse_n(vertex):                  # we also parse in the list of the vertices with which the
            edges.append((cost[vertex, neighbour], vertex, neighbour))   # current neighbour forms an edge and add it
    print(" Edges: ")                                                     # to the list of edges
    print(edges)                                                         # we print the found edges
    edges.sort()                                                         # we sort them
    tree = list()                                                        # we initialise the tree
    for c, x, y in edges:
        if disjointSets.checkAndJoin(x, y):                              # we check if there are no cycles and the given
            tree.append((c, x, y))                       # cost and the corresponding edges to the tree
    print(" The minimum spanning tree using the Kruskal's algorithm (the cost, first vertex, second vertex): ")
    return tree                                             # we return the obtained tree and print it on the screen




def read_a_graph_from_the_file(file_name):
    file = open(file_name, "r")
    line = file.readline()
    line = line.strip()
    vertices, edges = line.split(' ')
    graph = Graph(int(vertices), int(edges))
    line = file.readline().strip()
    while len(line) > 0:
        line = line.split(' ')
        if len(line) == 1:
            graph.get_the_dictionary_for_in[int(line[0])] = []
            graph.get_the_dictionary_for_out[int(line[0])] = []
        else:
            graph.get_the_dictionary_for_in[int(line[1])].append(int(line[0]))
            graph.get_the_dictionary_for_out[int(line[0])].append(int(line[1]))
            graph.get_dictionary_costs[(int(line[0]), int(line[1]))] = int(line[2])
        line = file.readline().strip()
    file.close()
    return graph


def write_graph_to_file(graph, output_file_name):
    file = open(output_file_name, "w")
    first_line = str(graph.get_the_number_of_vertices) + ' ' + str(graph.get_the_number_of_edges) + '\n'
    file.write(first_line)
    if len(graph.get_dictionary_costs) == 0 and len(graph.get_the_dictionary_for_in) == 0:
        raise ValueError("There is nothing that can be written!")
    for edge in graph.get_dictionary_costs.keys():
        new_line = "{} {} {}\n".format(edge[0], edge[1], graph.get_dictionary_costs[edge])
        file.write(new_line)
    for vertex in graph.get_the_dictionary_for_in.keys():
        if len(graph.get_the_dictionary_for_in[vertex]) == 0 and len(graph.get_the_dictionary_for_out[vertex]) == 0:
            new_line = "{}\n".format(vertex)
            file.write(new_line)
    file.close()
