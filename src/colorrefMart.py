import time
from graph import *
from graph_io import *

WAITTIME = 0.001
def basic_colorref(filename) -> List[Tuple[List[int], List[int], int, bool]]:
    with open(filename) as f:
        L = load_graph(f, read_list=True)[0]
    definedColors = {(()): (0, [])}
    matches = []
    result = []
    i = 0
    j = 0
    for graph in L:
        graph.label = i

        i += 1
    i = 0
    checkSame = []
    while len(L) > 0:
        graphDeletion = []
        # run through all the graphs vertices
        for graph in L:
            for v in graph.vertices:
                surroundingColors = calculateSurroundingColor(v)
                if surroundingColors in definedColors:
                    # if the color is defined and not yet set the colour
                    if v.colornum != definedColors.get(surroundingColors)[0]:
                        v.colornum = definedColors.get(surroundingColors)[0]
                        definedColors.get(v.oldColors)[1].remove(v)
                        definedColors.get(surroundingColors)[1].append(v)
                        v.oldColors = surroundingColors
                else:
                    # if the neighbourhood has not yet been defined but the vertices in the previous color all have the same neighbourhood
                    if checkUnique(v.oldColors, definedColors, surroundingColors):
                        # move all vertices to the new neighbourhood
                        definedColors[surroundingColors] = (definedColors[v.oldColors][0],[])
                        toDelete = []
                        for u in definedColors.get(v.oldColors)[1]:
                            color = calculateSurroundingColor(u)
                            if color == surroundingColors:
                                toDelete.append(u)
                        for u in toDelete:
                            definedColors.get(surroundingColors)[1].append(u)
                            definedColors.get(u.oldColors)[1].remove(u)
                            u.oldColors = surroundingColors
                        v.oldColors = surroundingColors
                    else:
                        # create a new neighbourhood
                        definedColors.get(v.oldColors)[1].remove(v)
                        v.colornum = len(definedColors)
                        definedColors[surroundingColors] = (len(definedColors), [v])
                        v.oldColors = surroundingColors
            if len(set([v.colornum for v in graph.vertices])) == len(set([v.label for v in graph.vertices])):
                graphDeletion.append(graph)
                checkSame.append(graph)
        for graph in graphDeletion:
            L.remove(graph)
        for graph in L:
            for v in graph.vertices:
                v.label = v.colornum
        for graph in checkSame:
            found = False
            colors1 = [v.colornum for v in graph.vertices]
            for list in matches:
                colors2 = [v.colornum for v in list[0].vertices]
                if sorted(colors1) == sorted(colors2):
                    found = True
                    list.append(graph)
            if not found:
                matches.append([graph])
        checkSame = []
        toDelete = []
        for list in matches:
            graphs = sorted([g.label for g in list])

            color_count = {}
            for v in sorted(list.pop().vertices, key=lambda v: v.label):
                if color_count.get(v.colornum) is None:
                    color_count[v.colornum] = 1
                else:
                    color_count[v.colornum] += 1
            color_count = sorted(color_count.values())
            discrete = set(color_count) == {1}
            result.append((graphs, color_count, i, discrete))
            toDelete.append(list)
        for delete in toDelete:
            matches.remove(delete)

        # print(definedColors)
        i += 1

    return result


def checkUnique(old, definedColors, compareWith):
    for v in definedColors.get(old)[1]:
        color = calculateSurroundingColor(v)
        if color == compareWith or (color != old and color in definedColors):
            continue
        else:
            return False
    return True


def calculateSurroundingColor(v):
    surroundingColors = []
    for e in v.neighbours:
        surroundingColors.append(e.label)
    surroundingColors.sort()
    surroundingColors = tuple(surroundingColors)
    return surroundingColors

start = time.time()
print(basic_colorref('Graphs/SampleGraphsBasicColorRefinement/CrefBenchmark4.grl'))
print("time: {}s".format(time.time() - start))
