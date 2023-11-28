import heapq
import time

graph = {
    'Jakarta': [('Bandung', 45), ('Cirebon', 205),('Semarang',160)],
    'Bandung': [('Surabaya', 550),('Semarang', 160), ('Cirebon', 105) ],
    'Cirebon': [('Semarang', 400), ('Surabaya', 300 ), ('Purwokerto', 430)],
    'Semarang': [('Cirebon', 400), ('Purwokerto', 300), ('Surabaya',300)],
    'Purwokerto': [('Semarang', 300), ('Yogyakarta', 165)],
    'Yogyakarta': [('Purwokerto', 165), ('Madiun', 135),('Cirebon', 165)],
    'Madiun': [('Yogyakarta', 135), ('Surabaya', 95), ('Malang', 95)],
    'Surabaya': [('Bandung', 550), ('Madiun', 95), ('Malang', 40), ('Jember', 190),('Bandung', 550), ('Cirebon', 300 )],
    'Malang': [('Surabaya', 40), ('Madiun',95),('Yogyakarta',200)],
    'Jember': [('Surabaya', 190),('Malang',58),('Madiun',88)]
}


heuristic_values = {
    'Jakarta': 0,
    'Bandung': 200,
    'Cirebon': 205,
    'Semarang': 160,
    'Purwokerto': 235,
    'Yogyakarta': 300,
    'Madiun': 300,
    'Surabaya': 340,
    'Malang': 710,
    'Jember': 800
}
def heuristic(node, goal):
    return heuristic_values[node]

def reconstruct_path(came_from, start, goal):
    path = [goal]
    current_node = goal

    while current_node != start:
        current_node = came_from[current_node]
        path.insert(0, current_node)

    return path

def astar(graph, start, goal, heuristic):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (0, start))

    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)

    came_from = {node: None for node in graph}

    start_time = time.time()

    while open_set:
        current_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            # Path found
            path = reconstruct_path(came_from, start, goal)
            total_cost = g_score[goal]
            end_time = time.time()
            print("Time taken:", end_time - start_time, "seconds")
            return path, total_cost

        closed_set.add(current_node)

        for neighbor, cost in graph[current_node]:
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current_node] + cost

            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                came_from[neighbor] = current_node

    end_time = time.time()
    print("Time taken:", end_time - start_time, "seconds")
    print()
    return None, None  # No path found

# Example usage:
start_node = 'Jakarta'
goal_node = 'Jember'

result, total_cost = astar(graph, start_node, goal_node, heuristic)
if result:
    print("Optimal Path:", result)
    print("Total Cost:", total_cost*1000)
else:
    print("No path found.")
