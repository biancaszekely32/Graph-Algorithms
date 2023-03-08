from Graph import Graph,UndirectedGraph,kruskal,print_graph,create_graph_and_cost, read_a_graph_from_the_file, write_graph_to_file
from random import randint
from math import inf
import itertools


class UI:
    def __init__(self):
        self._list_of_graphs = []
        self._current_one = None

    def initialize_a_new_graph(self):
        if self._current_one is None:
            self._current_one = 0
        graph = Graph(0, 0)
        self._list_of_graphs.append(graph)
        self._current_one = len(self._list_of_graphs) - 1

    def get_number_of_vertices(self):
        string = "The number of vertices is "
        string = string + str(self._list_of_graphs[self._current_one].get_the_number_of_vertices)
        print(string)

    def parse_the_set_vertices_ui(self):
        for vertex in self._list_of_graphs[self._current_one].parse_vertices():
            print(str(vertex))

    def find_if_there_is_edge_between_two_given_vertices(self):
        first_vertex = int(input("Insert the first vertex: "))
        second_vertex = int(input("Insert the second vertex: "))
        is_there_edge = self._list_of_graphs[self._current_one].check_if_edge_between_vertices(first_vertex,second_vertex)
        if is_there_edge is False:
            print(" There is no edge between the vertices. ")
        else:
            print("There is an edge between the vertices and its cost is: " + str(is_there_edge))

    def parse_outbound_edges(self):
        given_vertex = int(input(" Enter the vertex: "))
        template = str(given_vertex) + " :"
        for el in self._list_of_graphs[self._current_one].parse_edges_outbound(given_vertex):
            template = template + " (" + str(given_vertex) + " , "+ str(el) + " ) "
        print(template)

    def parse_inbound_edges(self):
        given_vertex = int(input(" Enter the vertex: "))
        template = str(given_vertex) + " :"
        for el in self._list_of_graphs[self._current_one].parse_edges_inbound(given_vertex):
            template = template + " (" + str(given_vertex) + " , " + str(el) + " ) "
        print(template)

    def get_the_in_degree_of_a_vertex_ui(self):
        vertex_given_by_user = int(input(" Enter the vertex to find out its in degree: "))
        if not self._list_of_graphs[self._current_one].get_vertex_in_degree(vertex_given_by_user):
            print(" The given vertex does not exist. ")
        else:
            print(" The in degree of the given vertex is: " + str(self._list_of_graphs[self._current_one].get_vertex_in_degree(vertex_given_by_user)))

    def get_the_out_degree_of_a_vertex_ui(self):
        vertex_given_by_user = int(input(" Enter the vertex to find out its out degree: "))
        if not self._list_of_graphs[self._current_one].get_vertex_out_degree(vertex_given_by_user):
            print(" The given vertex does not exist. ")
        else:
            print(" The out degree of the given vertex is: " + str(self._list_of_graphs[self._current_one].get_vertex_out_degree(vertex_given_by_user)))

    def add_given_edge_ui(self):
        first = int(input(" Enter the first vertex: "))
        second = int(input(" Enter the second vertex: "))
        given_cost = int(input(" Enter the cost of the edge: "))
        is_edge_added = self._list_of_graphs[self._current_one].add_given_edge(first,second,given_cost)
        if not is_edge_added:
            print("Edge can't be added")
        else:
            print("Edge added successfully!")

    def modify_the_costs_ui(self):
        first_vertex = int(input(" Enter the first vertex of the edge: "))
        second_vertex = int(input(" Enter the second vertex of the edge: "))
        new_cost = int(input("Enter the new cost for the edge: "))
        is_cost_modified = self._list_of_graphs[self._current_one].modify_the_cost_of_given_edge(first_vertex,second_vertex,new_cost)
        if not is_cost_modified:
            print(" Cost couldn't be changed! ")
        else:
            print(" Cost was changed successfully! ")

    def remove_an_edge_ui(self):
        first_given_vertex = int(input(" Enter the first vertex of the edge: "))
        second_given_vertex = int(input(" Enter the second vertex of the edge: "))
        is_edge_removed = self._list_of_graphs[self._current_one].remove_an_edge(first_given_vertex, second_given_vertex)
        if not is_edge_removed:
            print(" Edge couldn't be removed! ")
        else:
            print(" Edge removed successfully! ")

    def add_a_vertex_ui(self):
        added_vertex = int(input(" Enter the vertex you want to add: "))
        is_vertex_added = self._list_of_graphs[self._current_one].add_vertex(added_vertex)
        if not is_vertex_added:
            print(" Vertex already present! ")
        else:
            print(" Vertex added successfully! ")

    def remove_a_vertex_ui(self):
        removed_vertex = int(input(" Enter the vertex you would like to delete: "))
        is_vertex_removed = self._list_of_graphs[self._current_one].remove_vertex(removed_vertex)
        if not is_vertex_removed:
            print(" Vertex does not exit and couldn't be removed!")
        else:
            print(" Vertex removed successfully! ")

    def copy_the_graph_ui(self):
        copied_graph = self._list_of_graphs[self._current_one].copy_the_graph()
        self._list_of_graphs.append(copied_graph)
        print(" Graph copied successfully! ")

    def read_graph_from_file_ui(self):
        name_of_the_file = input(" Enter the name of the file: ")
        if self._current_one is None:
            self._current_one = 0
        current_reading_graph = read_a_graph_from_the_file(name_of_the_file)
        self._list_of_graphs.append(current_reading_graph)
        self._current_one = len(self._list_of_graphs) - 1

    def write_graph_to_file_ui(self):
        graph_being_writen = self._list_of_graphs[self._current_one]
        output_file_name = "random_" + str(self._current_one) + ".txt"
        write_graph_to_file(graph_being_writen, output_file_name)

    def create_a_random_graph_ui(self):
        number_of_vertices = int(input(" Enter the number of vertices your graph would like to have: "))
        number_of_edges = int(input(" Enter the number of edges your graph would like to have: "))
        generated_graph = self.generate_randomly_the_graph(number_of_vertices, number_of_edges)
        if self._current_one is None:
            self._current_one = 0
        self._list_of_graphs.append(generated_graph)
        self._current_one = len(self._list_of_graphs) - 1

    def generate_randomly_the_graph(self, number_of_vertices, number_of_edges):
        if number_of_vertices*(number_of_vertices - 1 / 2) < number_of_edges:
            raise ValueError("The inserted number of edges is to large for a creating graph. ")
        generated_graph = Graph(number_of_vertices, 0)
        for index in range(number_of_edges):
            is_edge_ok = False
            while not is_edge_ok:
                first_point = randint(0, number_of_vertices-1)
                second_point = randint(0, number_of_vertices-1)
                cost_of_edge = randint(0, 500)
                is_edge_ok = generated_graph.add_given_edge(first_point, second_point, cost_of_edge)
        return generated_graph

    def find_shortest_path_ui(self):
        """
        The ui functions which gets the vertices from the user and calls from the console the function that finds the shortest path.
        :return: prints on the screen the shortest path between the given vertices and its length if there is one
        """
        starting_vertex = int(input(" Enter the starting vertex for the path: "))
        ending_vertex = int(input(" Enter the ending vertex for the path. "))
        shortest_path = self._list_of_graphs[self._current_one].find_shortest_path(starting_vertex, ending_vertex)
        print(" The shortest path for the given vertices is: " + str(shortest_path) + " and its length is " + str(len(shortest_path)-1))

    def find_min_cost_walk_ui(self):
        vertex_begin = int(input("Enter source vertex = "))   # the starting vertex
        vertex_end = int(input("Enter end vertex = "))    # the ending vertex
        if vertex_begin not in self._list_of_graphs[self._current_one].parse_keys() or vertex_end not in self._list_of_graphs[self._current_one].parse_keys():
            raise ValueError("One vertex/ both vertices entered might not exist.")     # we check if both vertices exist
        else:
            distance, path = self._list_of_graphs[self._current_one].minimum_cost_path(vertex_begin, vertex_end)
            if distance == float("inf"):       # we call the function that determines the total cost and the actual path
                raise ValueError("There is no walk from {} to {}".format(vertex_begin, vertex_end))
            print("The cost of the minimum cost path is: {}".format(str(distance)))
        print("The path is: ", end=' ')        # we print the path
        for index in range(len(path) - 1, -1, -1):
            print(path[index], end=' ')
        print("\n")

    def kruskal_algo_ui(self):
        """
        Constructs a minimum spanning tree using the Kruskal's algorithm.
        """
        g, cost = create_graph_and_cost()
        print(" The undirected given graph is: ")
        print_graph(g)
        print(cost)
        print(kruskal(g, cost))

    def hamiltonian_cycle(self):
        # minimum cost Hamiltonian cycle

        minimum_cost, sol = self._list_of_graphs[self._current_one].HamiltonianCycle()

        if minimum_cost == inf:
            raise ValueError(" No Hamiltonian cycle found!")

        print(" Minimum cost: " + str(minimum_cost))
        print(" Hamiltonian cycle: ", )
        for i in sol:
            print(str(i) + " ", end="")
        print(str(sol[0]))

    @staticmethod
    def show_menu(self):
        print(" Available options: ")
        print("0. Exit. ")
        print("1. Get the number of vertices. ")
        print("2. Parse the set of vertices. ")
        print("3. Find out whether there is an edge between two vertices. ")
        print("4. Get the in degree of a specified vertex. ")
        print("5. Get the out degree of a specified vertex. ")
        print("6. Parse and list the set of outbound edges of a specified vertex. ")
        print("7. Parse and list the set of inbound edges of a specified vertex. ")
        print("8. Modify the given cost of an edge. ")
        print("9. Add an edge. ")
        print("10. Remove an edge. ")
        print("11. Add a vertex. ")
        print("12. Remove a vertex. ")
        print("13. Copy the graph. ")
        print("14. Read the graph from a text file. ")
        print("15. Write the graph in a text file. ")
        print("16. Create a random graph with specified number of vertices and of edges. ")
        print("17. Find the a lowest length path between two given vertices, by using a forward breadth-first search "
              "from the starting vertex. ")
        print("18.Find the minimum cost walk between two given vertices. ")
        print("19. Construct a minimum spanning tree using the Kruskal's algorithm.")
        print("20. Find a minimum cost Hamiltonian cycle.")
        print(" No graph has been selected so the actual graph is currently empty.")

    def start(self):
        while True:
            try:
                self.show_menu(self)
                user_option = input(" Enter "
                                    "your option: ")
                if user_option == '1':
                    self.get_number_of_vertices()
                elif user_option == '2':
                    self.parse_the_set_vertices_ui()
                elif user_option == '3':
                    self.find_if_there_is_edge_between_two_given_vertices()
                elif user_option == '4':
                    self.get_the_in_degree_of_a_vertex_ui()
                elif user_option == '5':
                    self.get_the_out_degree_of_a_vertex_ui()
                elif user_option == '6':
                    self.parse_outbound_edges()
                elif user_option == '7':
                    self.parse_outbound_edges()
                elif user_option == '8':
                    self.modify_the_costs_ui()
                elif user_option == '9':
                    self.add_given_edge_ui()
                elif user_option == '10':
                    self.remove_an_edge_ui()
                elif user_option == '11':
                    self.add_a_vertex_ui()
                elif user_option == '12':
                    self.remove_a_vertex_ui()
                elif user_option == '13':
                    self.copy_the_graph_ui()
                elif user_option == '14':
                    self.read_graph_from_file_ui()
                elif user_option == '15':
                    self.write_graph_to_file_ui()
                elif user_option == '16':
                    self.create_a_random_graph_ui()
                elif user_option == '17':
                    self.find_shortest_path_ui()
                elif user_option == '18':
                    self.find_min_cost_walk_ui()
                elif user_option == '19':
                    self.kruskal_algo_ui()
                elif user_option == '20':
                    self.hamiltonian_cycle()
                elif user_option == '0':
                    return
                else:
                    print(" The command you inserted is not available. Please select another one from the given menu. ")
            except ValueError as ve:
                print(ve)


start = UI()
start.start()
