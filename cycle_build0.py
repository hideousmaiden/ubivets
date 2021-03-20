import networkx as nx

final_cycles = []
weighted_edges = []
mutual_edges = []
# raw_graph - сырои направленныи граф
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 2), (2, 1), (4, 1), (4, 5), (3, 5), (2, 6), (6, 4), (4, 6), (5, 2), (2, 5)]
# limit - максимальная степень знакомства, которую мы допускаем (это уменьшает количество циклов для проверки), можно менять
limit = 2
raw_graph = nx.DiGraph()
raw_graph.add_edges_from(edges)
nodes = raw_graph.nodes
#выкидываем все невзаимные знакомства (они не считаются личнои связью)
for edge_number in range(len(edges)):
     rev_edge = list(edges[edge_number])
     rev_edge.reverse()
     if tuple(rev_edge) not in edges:
         raw_graph.remove_edge(edges[edge_number][0], edges[edge_number][1])
#после подсчета кратчаиших путеи тем, кто совсем не знаком присваивается расстояние no_conn_rate
paths = nx.shortest_path(raw_graph)
no_conn_rate = len(nodes) + 1
#print(paths)
weighted_edges = []
for start in paths:
    for target in nodes:
        if start != target:
            if target in paths[start]:
                weight = len(paths[start][target])
            else:
                weight = no_conn_rate
            if weight > limit:
                weighted_edge = []
                weighted_edge.append(start)
                weighted_edge.append(target)
                weighted_edge.append(weight)
                weighted_edges.append(tuple(weighted_edge))
#print(weighted_edges)
#weighted_graph - взвешенныи направленныи граф (веса - расстояния между узлами)
weighted_graph = nx.DiGraph()
weighted_graph.add_weighted_edges_from(weighted_edges)
final_paths =  weighted_graph.adj
#ищем все простые циклы, включающие все узлы, выкидываем повторяющиеся (одинаковыи порядок связеи, разное направление)
cycles = list(nx.simple_cycles(weighted_graph))
if len(cycles) == 0:
    print('измените значение limit')
else:
    for cycle in cycles:
        if len(cycle) == len(nodes):
            reversed = []
            reversed.append(cycle[0])
            part = cycle[1:len(cycle)]
            part.reverse()
            reversed.extend(part)
            if reversed not in final_cycles:
                final_cycles.append(cycle)
#    print(final_cycles)
    max_count = 0
    for cycle in final_cycles:
        cycle_count = 0
        for n_number in range(len(nodes) - 1):
            start = cycle[n_number]
            target = cycle[n_number + 1]
            cycle_count += final_paths[start][target]['weight']
        cycle_count += final_paths[cycle[-1]][cycle[0]]['weight']
        if cycle_count > max_count:
            max_count = cycle_count
            best_cycle = cycle
    print(best_cycle, max_count)
#    print(final_paths)
