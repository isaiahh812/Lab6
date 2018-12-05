#Isaiah Hernandez
#80591211
#12/4/18
#CS2302
from queue import *
class DisjointSetForest:
    def __init__(self, n):
        self.dsf = [-1] * n

    def is_index_valid(self, index):
        return 0 <= index <= len(self.dsf)

    def find(self, a):
        if not self.is_index_valid(a):
            return -1

        if self.dsf[a] < 0:
            return a

        self.dsf[a] = self.find(self.dsf[a])

        return self.dsf[a]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra != rb:
            self.dsf[rb] = ra

    def get_num_of_sets(self):
        count = 0

        for num in self.dsf:
            if num < 0:
                count += 1

        return count


class GraphAM:

    def __init__(self, initial_num_vertices, is_directed):
        self.adj_matrix = []

        for i in range(initial_num_vertices):  # Assumption / Design Decision: 0 represents non-existing edge
            self.adj_matrix.append([0] * initial_num_vertices)

        self.is_directed = is_directed

    def is_valid_vertex(self, u):
        return 0 <= u < len(self.adj_matrix)

    def add_vertex(self):
        for lst in self.adj_matrix:
            lst.append(0)

        new_row = [0] * (len(self.adj_matrix) + 1)  # Assumption / Design Decision: 0 represents non-existing edge
        self.adj_matrix.append(new_row)

        return len(self.adj_matrix) - 1  # Return new vertex id

    def add_edge(self, src, dest, weight = 1.0):
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return

        self.adj_matrix[src][dest] = weight

        if not self.is_directed:
            self.adj_matrix[dest][src] = weight

    def remove_edge(self, src, dest):
        self.add_edge(src,dest, 0)

    def get_num_vertices(self):
        return len(self.adj_matrix)

    def get_vertices_reachable_from(self, src):
        reachable_vertices = set()

        for i in range(len(self.adj_matrix)):
            if self.adj_matrix[src][i] != 0:
                reachable_vertices.add(i)

        return reachable_vertices

    def get_vertices_that_point_to(self, dest):
        vertices = set()

        for i in range(len(self.adj_matrix)):
            if self.adj_matrix[i][dest] != 0:
                vertices.add(i)

        return vertices

    def __str__(self):

        return str(self.adj_matrix)
    def get_edge_weight(self, src , dest):
        if self.adj_matrix[src][dest] > 0:
            return self.adj_matrix[src][dest] 

def creates_cycle(dsf, src, dest): #used for kruskals algorithm
        if dsf.find(src) == dsf.find(dest):
            return True
        return False
def compute_indegree_every_vertex(graph):
    indegrees_for_graph = []
    for i in range(graph.get_num_vertices()):
        indegrees_for_graph.append(len(graph.get_vertices_that_point_to(i)))
    return indegrees_for_graph    
def topological_sort(graph):
    all_in_degrees = compute_indegree_every_vertex(graph)
    sort_result = []
    
    q = Queue()
    
    for i in range(len(all_in_degrees)):
        if all_in_degrees[i] == 0:
            q.put(i)
    while not q.empty():
        u = q.get()
        
        sort_result.append(u)
        
        for adj_vertex in graph.get_vertices_reachable_from(u):
            all_in_degrees[adj_vertex] -= 1
            
            if all_in_degrees[adj_vertex] == 0:
                q.put(adj_vertex)
    if len(sort_result) != graph.get_num_vertices():
        return None
    return sort_result
def kruskal_algorithm(graph):       #Method for finding the MST
    edges_in_graph= []

    for vertex in range(graph.get_num_vertices()):
        for adj_vertex in graph.get_vertices_reachable_from(vertex):
            edges_in_graph.append([graph.get_edge_weight(vertex, adj_vertex), adj_vertex, vertex])

    edges_in_graph.sort()
    dsf = DisjointSetForest(graph.get_num_vertices())
    result = []

    for i in range(len(edges_in_graph)):
        src = edges_in_graph[i][2]
        dest = edges_in_graph[i][1]
        if creates_cycle(dsf,src,dest) == False:
            result.append(edges_in_graph[i])
            dsf.union(edges_in_graph[i][2] , edges_in_graph[i][1])

    for i in range(len(result)):
        result[i].reverse()

    return result

graph = GraphAM(5,True)     #Creating the graph
graph.add_edge(0, 4, 4)     #Vertex 0, dest 1, weight 1
graph.add_edge(0, 3, 7)
graph.add_edge(1, 4, 6)
graph.add_edge(2, 1, 3)
graph.add_edge(3, 1, 5)
graph.add_edge(2, 4, 1)
graph.add_edge(3, 4, 2)
T = topological_sort(graph)
K = kruskal_algorithm(graph)
file = open("results.txt","w")
for i in range(len(T)):
    file.write(str(T[i]))
for i in range(len(K)):    
    file.write(str(K[i]))
print("Topological sort the the hard coded graph:")
print(topological_sort(graph))
print("Kruskals Algorithm for the hard coded graph:")
print(kruskal_algorithm(graph))

