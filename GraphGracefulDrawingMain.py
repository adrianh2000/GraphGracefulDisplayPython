from tkinter import *
import random
import copy

canvas_width = 1600
canvas_height = 1600
num_trees_width = 14
box_width = canvas_width / num_trees_width
num_trees_height = 14
box_height = canvas_height / num_trees_height
num_vertices = 10

vertex_colors = {
    'green0': '#009999',
    'green1': '#336666',
    'green2': '#00CCCC',
    'green3': '#CCFFCC',
    'blue0': '#00CCCC',
    'blue1': '#66CCFF',
    'blue2': '#CCFFFF',
    'purple0': '#999FFF'
}

master = Tk()

w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()


class Vertex:
    def __init__(self, x, y, radius=10, label='', fill_color='silver'):
        self.x = x
        self.y = y
        self.radius = radius
        self.label = label
        self.fill_color = fill_color

    def set_label(self, label):
        self.label = label

    def set_coordinates(self, x0, y0):
        self.x = x0
        self.y = y0

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius,
                      fill=self.fill_color)
        canvas.create_text(self.x, self.y, text=self.label, font=('Times', -1 * self.radius, 'bold'))

    def draw(self, canvas, box_x0, box_y0, box_x1, box_y1):
        vertex_x = box_x0 + (box_x1 - box_x0) * self.x
        vertex_y = box_y0 + (box_y1 - box_y0) * self.y

        canvas.create_oval(vertex_x - self.radius, vertex_y - self.radius, vertex_x + self.radius,
                           vertex_y + self.radius, fill=self.fill_color)

        canvas.create_text(vertex_x, vertex_y, text=self.label, font=('Times', -1 * self.radius, 'bold'))

class Graph:
    def __init__(self, vertex_list, edge_list):
        self.vertex_list = vertex_list
        self.edge_list = edge_list

    def clone(self):
        new_graph = Graph([], [])
        new_vertex_list = []
        new_edge_list = []

        # copy all vertices
        for vertex in self.vertex_list:
            v0 = copy.deepcopy(vertex)
            new_vertex_list.append(v0)

        # copy all edges
        for edge in self.edge_list:
            e0 = copy.deepcopy(edge)
            new_edge_list.append(edge)

         # add to new graph
        new_graph.vertex_list = new_vertex_list
        new_graph.edge_list = new_vertex_list
        return new_graph

    def read_from_file(self, file_name, x0, y0, x1, y1, convert_to_screen_coordinates=False):
        self.vertex_list = []
        self.edge_list = []
        f = open(file_name, 'r')

        # read first line 'vertices'
        cur_line = f.readline()

        cur_line = f.readline()
        # read vertices
        while 'edges' not in cur_line and 'end' not in cur_line:
            cur_list = cur_line.split(',')
            x = float(cur_list[1])
            y = float(cur_list[2])

            if convert_to_screen_coordinates:
                x = float(cur_list[1]) * (x1-x0) + x0
                y = float(cur_list[2]) * (y1-y0) + y0

            new_vertex = Vertex(x, y, 10, cur_list[0], '#CCFFCC')
            self.vertex_list.append(new_vertex)
            cur_line = f.readline()

        # read edges
        cur_line = f.readline()
        while 'end' not in cur_line:
            cur_list = cur_line.split(',')
            # convert all strings into integers
            cur_list = list(map(int, cur_list))
            self.edge_list.append(cur_list)
            cur_line = f.readline()

    def draw(self, canvas):
        for edge in self.edge_list:
            vertex0 = self.vertex_list[edge[0]]
            x0 = vertex0.x
            y0 = vertex0.y

            vertex1 = self.vertex_list[edge[1]]
            x1 = vertex1.x
            y1 = vertex1.y

            canvas.create_line(x0, y0, x1, y1, fill='#000000')

        for vertex in self.vertex_list:
            vertex.draw(w)

    def draw(self, canvas, box_x0, box_y0, box_x1, box_y1):
        cur_box_width = float(box_x1 - box_x0)
        cur_box_height = float(box_y1 - box_y0)

        for edge in self.edge_list:
            vertex0 = self.vertex_list[edge[0]]
            x0 = box_x0 + int(vertex0.x * cur_box_width)
            y0 = box_y0 + int(vertex0.y * cur_box_height)

            vertex1 = self.vertex_list[edge[1]]
            x1 = box_x0 + int(vertex1.x * cur_box_width)
            y1 = box_y0 + int(vertex1.y * cur_box_height)

            canvas.create_line(x0, y0, x1, y1, fill='#000000')

        for vertex in self.vertex_list:
            vertex.draw(w, box_x0, box_y0, box_x1, box_y1)   # a-a


def create_list_of_trees_with_graceful_labelings(file_name, tree_graph: Graph):
    list_trees = []

    f = open(file_name, 'r')

    # ignore header
    cur_line = f.readline()

    # read first line
    cur_line = f.readline()

    while 'end' not in cur_line:
        vertex_labels = cur_line.split(',')

        # create a new tree graph isomorphic to the given one
        new_graph = copy.deepcopy(tree_graph)

        # set the new graph vertex labels to the graceful ones
        for index, cur_vertex in enumerate(new_graph.vertex_list):
            cur_vertex.set_label(vertex_labels[index])

        # add new tree to the list
        list_trees.append(new_graph)

        # read next line
        cur_line = f.readline()

    return list_trees


vertex_list0 = []
for i in range(0, num_vertices):
    x = random.randint(0, canvas_width)
    y = random.randint(0, canvas_height)
    v = Vertex(x, y, 10, str(i), vertex_colors['green3'])
    vertex_list0.append(v)

edge_list0 = [[1, 2], [2, 3], [3, 4], [5, 2]]

# my_graph = Graph(vertex_list0, edge_list0)
# my_graph0 = Graph([], [])
# my_graph0.read_from_file('graph_labeling.txt', 0, 0, canvas_width/2, canvas_height/2)
# my_graph0.draw(w)

my_graph1 = Graph([], [])
my_graph1.read_from_file('GraphTreeV0.txt', canvas_width/2, canvas_height/2, canvas_width, canvas_height)
# my_graph1.draw(w)

tree_list = create_list_of_trees_with_graceful_labelings('GraphTreeV0-Graceful Labels.txt', my_graph1)
for index, my_tree in enumerate(tree_list):
    col = (index % num_trees_width)
    row = int(index / num_trees_height)
    x0 = col * box_width
    y0 = row * box_height
    x1 = x0 + box_width
    y1 = y0 + box_height
    my_tree.draw(w, x0, y0, x1, y1)


mainloop()



