import networkx as nx
import matplotlib.pyplot as plt

def calculate_critical_path(tasks):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for each task
    for task in tasks:
        G.add_node(str(task['numero']), duration=task['duracion'], description=task['descripcion'])


    # Add edges representing task dependencies
    for task in tasks:
        for prev_task in task['tareas_previas']:
            G.add_edge(str(prev_task), str(task['numero']))

    # Calculate earliest start time and earliest finish time for each task
    earliest_start = {}
    earliest_finish = {}
    for task in nx.topological_sort(G):
        if 'duration' not in G.nodes[task]:
            continue  # Skip nodes without 'duration' attribute
        duration = G.nodes[task]['duration']
        predecessors = list(G.predecessors(task))
        if len(predecessors) > 0:
            earliest_start[task] = max(earliest_finish.get(prev_task, 0) for prev_task in predecessors)
        else:
            earliest_start[task] = 0
        earliest_finish[task] = earliest_start[task] + duration

    # Calculate latest start time and latest finish time for each task
    latest_start = {}
    latest_finish = {}
    critical_path_length = earliest_finish[max(G.nodes, key=earliest_finish.get)]
    for task in reversed(list(nx.topological_sort(G))):
        duration = G.nodes[task]['duration']
        successors = list(G.successors(task))
        if len(successors) > 0:
            latest_finish[task] = min(latest_start.get(next_task, critical_path_length) for next_task in successors)
        else:
            latest_finish[task] = critical_path_length
        latest_start[task] = latest_finish[task] - duration

    # Identify the critical path
    critical_path = [task for task in G.nodes if earliest_start[task] == latest_start[task]]

    # Calculate the total duration of the critical path
    total_duration = critical_path_length

    return G, critical_path, total_duration



def draw_graph(G, tasks, critical_path):
    # Specify node positions for better layout
    pos = nx.circular_layout(G)  # Use circular_layout algorithm


    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)

    # Draw edges
    nx.draw_networkx_edges(G, pos)

    # Draw labels
    labels = {str(task['numero']): task['descripcion'] for task in tasks}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

    # Highlight critical path
    critical_path_edges = [(critical_path[i], critical_path[i+1]) for i in range(len(critical_path)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=critical_path_edges, edge_color='r', width=2)

    # Show the graph
    plt.axis('off')
    plt.show()
