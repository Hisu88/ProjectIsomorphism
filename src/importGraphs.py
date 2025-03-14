import time
from graph_io import *
from colorrefMart import *


# main function, does all the steps necessary for the project
def main(path: str):
    if "grl" not in path:
        # opens singular graph and calculate the amount of automorphisms
        with open(path) as f:
            G = load_graph(f, read_list=True)
            return calculateAut(G)
    else:
        with open(path) as f:
            graphs = load_graph(f, read_list=True)[0]
        # get basic color refinement results
        results = basic_colorref(path)
        # TODO reiterate over non discrete groups
        if "Aut" in path:
            # if the file is an Aut file, calculate the automorphisms
            autResults = []
            for result in results:
                autResults.append((result[0], calculateAut(graphs[result[0][0]])))
            return autResults
        return results


# calculates the amount of automorphisms for a graph
def calculateAut(graph: Graph):
    setBase(graph)
    # TODO call modified color refinement


# sets the colour of all vertices to it's base value
def setBase(graph: Graph):
    for vector in graph.vertices:
        vector.colornum = 0
