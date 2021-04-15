import networkx as nx
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
#чтение из фаила
length = 6 #количество строчек в таблице
edges = []
isolat = []
column_name = 'A' #столбец с именами
column_conn = 'B' #столбец со знакомыми
column_vict = 'C' #колонка с жертвами
column_stat = 'D' #колонка со статусами
CREDENTIALS_FILE = 'ubivets1-da74a14302d5.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
service = apiclient.discovery.build('sheets', 'v4', credentials=credentials)
for number in range(2,length+1):
    cell_name = column_name + str(number)
    result = service.spreadsheets().values().get(
    spreadsheetId='1wZByQb2aARqsp0UUyCvUleCvQ_Ta29BiQ9sqGWIWmYU', range=cell_name).execute()
    name = result.get('values')
    cell_stat = column_stat + str(number)
    result = service.spreadsheets().values().get(
    spreadsheetId='1wZByQb2aARqsp0UUyCvUleCvQ_Ta29BiQ9sqGWIWmYU', range=cell_stat).execute()
    stat = result.get('values')
    cell_conn = column_conn + str(number)
    result = service.spreadsheets().values().get(
    spreadsheetId='1wZByQb2aARqsp0UUyCvUleCvQ_Ta29BiQ9sqGWIWmYU', range=cell_conn).execute()
    conn = result.get('values')
    if stat[0][0] == 'Участник':
        print(name[0][0])
        if conn != None:
            links = conn[0][0].split(';')
            for elem in links:
                link = []
                link.append(name[0][0])
                link.append(elem)
                edges.append(tuple(link))
        else:
            isolat.append(name[0][0])

#графы
final_cycles = []
weighted_edges = []
mutual_edges = []
limit = 0
raw_graph = nx.DiGraph()
raw_graph.add_edges_from(edges)
raw_graph.add_nodes_from(isolat)
nodes = raw_graph.nodes
for edge_number in range(len(edges)):
     rev_edge = list(edges[edge_number])
     rev_edge.reverse()
     if tuple(rev_edge) not in edges:
         raw_graph.remove_edge(edges[edge_number][0], edges[edge_number][1])
paths = nx.shortest_path(raw_graph)
no_conn_rate = len(nodes) + 1
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
weighted_graph = nx.DiGraph()
weighted_graph.add_weighted_edges_from(weighted_edges)
final_paths =  weighted_graph.adj
print(final_paths)
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
#запись в фаил
for number in range(2,length+1):
    cell_name = column_name + str(number)
    result = service.spreadsheets().values().get(
    spreadsheetId='1wZByQb2aARqsp0UUyCvUleCvQ_Ta29BiQ9sqGWIWmYU', range=cell_name).execute()
    name = result.get('values')
    cell_vict = column_vict + str(number)
    for num in range(len(best_cycle)):
        if name[0][0] == best_cycle[num] and num != (len(best_cycle) - 1):
            empt_l = []
            empt_ll = []
            empt_l.append(best_cycle[num+1])
            empt_ll.append(empt_l)
            results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1wZByQb2aARqsp0UUyCvUleCvQ_Ta29BiQ9sqGWIWmYU', body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": cell_vict,
                     "values": empt_ll}]
            }).execute()
        elif name[0][0] == best_cycle[num] and num == (len(best_cycle) - 1):
            empt_l = []
            empt_ll = []
            empt_l.append(best_cycle[0])
            empt_ll.append(empt_l)
            results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1wZByQb2aARqsp0UUyCvUleCvQ_Ta29BiQ9sqGWIWmYU', body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": cell_vict,
                     "values": empt_ll}]
            }).execute()

