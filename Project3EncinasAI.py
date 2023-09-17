import tkinter as tk
import math
import time

start_time = time.time()
steps = 0


def euclid_distance(city1, city2):
    x1, y1 = city1["x"], city1["y"]
    x2, y2 = city2["x"], city2["y"]
    
    distance_traveled = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance_traveled


def path_cost(path, cities):
    total_cost = 0.0
    num_cities = len(path)
    
    for i in range(num_cities):
        city1 = cities[path[i]]
        city2 = cities[path[(i + 1) % num_cities]]  # Wrap around for the last city
        
        distance = euclid_distance(city1, city2)
        total_cost += distance
    
    return total_cost

# Initialize an empty dictionary to store city information
cities = {}

with open("Random30.tsp", "r") as file:
    reading_cities = False  # Flag to indicate when to read city data
    for line in file:
        line = line.strip()
        
        if line == "NODE_COORD_SECTION":
            reading_cities = True
            continue  # Move to the next line (start reading city data)
        
        if reading_cities:
            # Split the line into parts (assuming city ID, X-coordinate, and Y-coordinate)
            parts = line.split()
            if len(parts) == 3:
                city_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                
                # Store city information in the 'cities' dictionary
                cities[city_id] = {"x": x, "y": y}

# Print city coordinates
for city_id, coordinates in cities.items():
    x = coordinates["x"]
    y = coordinates["y"]
    print(f"City {city_id}: X = {x}, Y = {y}")

Starting_City_ID = 1

Starting_City_Coordinates = cities[Starting_City_ID]
Starting_X = Starting_City_Coordinates["x"]
Starting_Y = Starting_City_Coordinates["y"]

print(f"Starting City ({Starting_City_ID}): X = {Starting_X}, Y = {Starting_Y}")

import math

def closest_edge_insertion(cities, initial_city_id):
    global steps
    # Initialize the tour with the initial city
    tour = [initial_city_id]
    
    # Create a list of unvisited cities (excluding the initial city)
    unvisited_cities = list(cities.keys())
    unvisited_cities.remove(initial_city_id)
    
    while unvisited_cities:
        current_city_id = tour[-1]
        closest_distance = float('inf')
        closest_city_id = None
        
        # Find the closest city to an existing edge in the tour
        for city_id in unvisited_cities:
            x1, y1 = cities[current_city_id]["x"], cities[current_city_id]["y"]
            x2, y2 = cities[city_id]["x"], cities[city_id]["y"]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            if distance < closest_distance:
                closest_distance = distance
                closest_city_id = city_id
        
        # Insert the closest city into the tour at the appropriate position
        insert_index = tour.index(current_city_id) + 1
        tour.insert(insert_index, closest_city_id)
        
        # Remove the closest city from the list of unvisited cities
        unvisited_cities.remove(closest_city_id)

        steps += 1  # Increment the step counter

    
    return tour

end_time = time.time()
elapsed_time = end_time - start_time

# Usage example:
# Assuming you have populated the 'cities' dictionary and selected an initial city
initial_city_id = 1  # You can choose any initial city
tour = closest_edge_insertion(cities, initial_city_id)
print("Tour:", tour)

tour_cost = path_cost(tour, cities)
print(f"Total Tour Cost: {tour_cost}")

# Create a function to draw the tour on a canvas
def draw_tour(canvas, cities, tour):
    canvas.delete("all")  # Clear the canvas
    spacing_factor = 20 
    
    # Draw cities as points
    for city_id, city_info in cities.items():
        x, y = city_info["x"], city_info["y"]
        shifted_x = x + spacing_factor
        shifted_y = y + spacing_factor
        canvas.create_oval(shifted_x - 5, shifted_y - 5, shifted_x + 5, shifted_y + 5, fill="blue")  # City points
        canvas.create_text(shifted_x, shifted_y - 10, text=str(city_id), font=("Helvetica", 10), fill="black")  # City numbers
    # Draw the tour as lines connecting cities
    for i in range(len(tour) - 1):
        city1 = cities[tour[i]]
        city2 = cities[tour[i + 1]]
        x1, y1 = city1["x"]  + spacing_factor, city1["y"]  + spacing_factor
        x2, y2 = city2["x"]  + spacing_factor, city2["y"]  + spacing_factor
        canvas.create_line(x1, y1, x2, y2, fill="red")  # Customize as needed

# Create a function to update the canvas with the current tour
def update_canvas():
    draw_tour(canvas, cities, tour)
    tour_cost = path_cost(tour, cities)
    cost_label.config(text=f"Total Tour Cost: {tour_cost:.2f}")

# Create the Tkinter window
root = tk.Tk()
root.title("TSP Tour Visualization")

# Create a canvas to display the cities and the tour
canvas = tk.Canvas(root, width=2000, height=1200)
canvas.pack()

# Create a label to display the total tour cost
cost_label = tk.Label(root, text="", font=("Helvetica", 12))
cost_label.pack()

# Create a button to trigger the canvas update
update_button = tk.Button(root, text="Update Tour", command=update_canvas)
update_button.pack()

# Initialize the canvas with the initial tour
update_canvas()
elapsed_time_ms = elapsed_time * 1000

print(f"Elapsed Time: {elapsed_time_ms:.2f} milliseconds")
print(f"Total Steps: {steps}")

print(f"hi there")

print(f"Whats up")


# Start the Tkinter main loop
root.mainloop()