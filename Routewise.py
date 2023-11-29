import tkinter as tk
from tkinter import ttk
import heapq

class RouteWiseApp:
    def __init__(self, root, graph, heuristic_values, astar):
        self.root = root
        self.root.title("RouteWise - Jakarta")

        self.graph = graph
        self.heuristic_values = heuristic_values
        self.astar = astar

        self.start_label = tk.Label(root, text="Start City: Jakarta", font=("Helvetica", 12))
        self.start_label.grid(row=0, column=0, pady=10)

        self.destination_label = tk.Label(root, text="Destination City:", font=("Helvetica", 12))
        self.destination_label.grid(row=1, column=0, pady=10)

        self.destination_var = tk.StringVar()
        self.destination_combobox = ttk.Combobox(root, textvariable=self.destination_var)
        self.destination_combobox['values'] = list(graph.keys())
        self.destination_combobox.grid(row=1, column=1, pady=10)

        self.find_route_button = tk.Button(root, text="Find Route", command=self.find_route)
        self.find_route_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def find_route(self):
        start_node = 'Jakarta'
        goal_node = self.destination_var.get()

        result, total_cost = self.astar(self.graph, start_node, goal_node, self.heuristic)
        if result:
            path_str = " -> ".join(result)
            result_str = f"Optimal Path: {path_str}\nTotal Cost: {total_cost}"
            self.result_label.config(text=result_str)
        else:
            self.result_label.config(text="No path found.")

    def heuristic(self, node, goal):
        return self.heuristic_values[node]

if __name__ == "__main__":
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
        'Purwokerto': 550,
        'Yogyakarta': 750,
        'Madiun': 600,
        'Surabaya': 550,
        'Malang': 710,
        'Jember': 670
    }

    def heuristic(node, goal):
        return heuristic_values[node]

    def astar(graph, start, goal, heuristic):
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start))

        g_score = {node: float('inf') for node in graph}
        g_score[start] = 0

        f_score = {node: float('inf') for node in graph}
        f_score[start] = heuristic(start, goal)

        came_from = {node: None for node in graph}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            if current_node == goal:
                # Path found
                path = reconstruct_path(came_from, start, goal)
                total_cost = g_score[goal]
                return path, total_cost*1000

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

        return None, None  # No path found

    def reconstruct_path(came_from, start, goal):
        path = [goal]
        current_node = goal

        while current_node != start:
            current_node = came_from[current_node]
            path.insert(0, current_node)

        return path

    root = tk.Tk()
    app = RouteWiseApp(root, graph, heuristic_values, astar)
    root.mainloop()
