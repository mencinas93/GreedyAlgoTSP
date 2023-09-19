import tkinter as tk #GUI
import math # library for math 
import time #count steps and time

start_time = time.time()
steps = 0
#start time and steps initialized. 

#Function to calculate distance between two cities with euclid formula. 
def euclid_distance(city1, city2):
    x1, y1 = city1["x"], city1["y"]
    x2, y2 = city2["x"], city2["y"]
    
    distance_traveled = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance_traveled

#Function to calculate the total path cost. 
def path_cost(path, cities):
    total_cost = 0.0
    number_of_cities = len(path)
    
    for i in range(number_of_cities):
        city1 = cities[path[i]]
        city2 = cities[path[(i + 1) % number_of_cities]]  # Wrap around for the last city
        
        distance = euclid_distance(city1, city2)
        total_cost += distance
    
    return total_cost

#Empty dictionary to store city information 
cities = {}

#reads file when it is open. 
with open("Random30.tsp", "r") as tsp_file:
    reading_cities_flag = False  # Flag to indicate when to read city data
    for reading_line in tsp_file:
        reading_line = reading_line.strip()
        #reads until it reaches line in TSP file that says NODE_COORD_SECTION
        if reading_line == "NODE_COORD_SECTION":
            reading_cities_flag = True
            continue  # Move to the next line (start reading city data)
        
        if reading_cities_flag:
            # Split the line into parts (City ID, X and Y coordinates)
            CityInfo = reading_line.split()
            if len(CityInfo) == 3: #makes sure to check if their is 3 elements in the CityInfo
                city_id = int(CityInfo[0])
                x = float(CityInfo[1])
                y = float(CityInfo[2])
                
                # Store city information in the 'cities' dictionary
                cities[city_id] = {"x": x, "y": y}

# Print city coordinates
for city_id, coordinates in cities.items():
    x = coordinates["x"]
    y = coordinates["y"]
    print(f"City {city_id}: X:{x}, Y:{y}")

Starting_City_ID = 1

Starting_City_Coordinates = cities[Starting_City_ID]
Starting_X = Starting_City_Coordinates["x"]
Starting_Y = Starting_City_Coordinates["y"]

print(f"Starting City ({Starting_City_ID}): X: {Starting_X}, Y: {Starting_Y}")

def greedy_algorithm(cities, initial_city_id):
    global steps #steps counter
    # Initialize the tour with the initial city

    tour = [initial_city_id]
    
    # Create a list of unvisited cities, Keeps tracking of cities visited except initial city
    unvisited_cities = list(cities.keys())
    unvisited_cities.remove(initial_city_id)
    
    #while their is still unvisted cites. 
    while unvisited_cities:
        current_city_id = tour[-1]
        #take the ID of the last city you visited. 
        closest_distance = float('inf')
        #closest distance set to infinity, Closest city ID and distance keep track of closest unvisited city.
        closest_city_id = None
        
        # Find the closest city to an existing edge in the tour
        #loop all unvisited_cities.
        for city_id in unvisited_cities:
            x1, y1 = cities[current_city_id]["x"], cities[current_city_id]["y"]
            x2, y2 = cities[city_id]["x"], cities[city_id]["y"]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            #calculate between current and a city being considered
            if distance < closest_distance:
                closest_distance = distance
                closest_city_id = city_id
            #compare calculated distance to closest distance. If distance less than closest than closest is equal now to distance. closest City ID is now city_ID
        
        # Insert the closest city into the tour at the next position
        insert_index = tour.index(current_city_id) + 1
        tour.insert(insert_index, closest_city_id)
        
        # Remove the closest city from the list of unvisited cities
        unvisited_cities.remove(closest_city_id)

        steps += 1  # Increment the step counter

    return tour

initial_city_id = 1  # Your chosen initial city

tour = greedy_algorithm(cities, initial_city_id)


# Check if the last city in the tour is not the same as the starting city
if tour[-1] != initial_city_id:
    # Calculate the distance from the last city to the starting city
    last_city = cities[tour[-1]]
    starting_city = cities[initial_city_id]
    distance_to_start = euclid_distance(last_city, starting_city)
    
    # Add an edge from the last city to the starting city, connection. 
    tour.append(initial_city_id)

    steps += 1 


end_time = time.time()
elapsed_time = end_time - start_time

print("Tour:", tour)
tour_cost = path_cost(tour, cities)
print(f"Total Tour Cost: {tour_cost}")

# Create a function to draw the tour on a canvas
def draw_tour(canvas, cities, tour):
    canvas.delete("all")  # Clear the canvas
    spacing_factor = 2
    
    # Draw cities as points
    for city_id, city_info in cities.items():
        x, y = city_info["x"], city_info["y"]
        shifted_x = x * 5 + spacing_factor  
        shifted_y = y * 5 + spacing_factor  
        canvas.create_oval(shifted_x - 2, shifted_y - 2, shifted_x + 2, shifted_y + 2, fill="blue")  # City points
        canvas.create_text(shifted_x, shifted_y - 10, text=str(city_id), font=("Helvetica", 10), fill="black")  # City numbers
    # Draw the tour as lines connecting cities
    for i in range(len(tour) - 1):
        city1 = cities[tour[i]]
        city2 = cities[tour[i + 1]]
        x1, y1 = city1["x"] * 5  + spacing_factor, city1["y"] * 5  + spacing_factor
        x2, y2 = city2["x"] * 5  + spacing_factor, city2["y"] * 5  + spacing_factor
        canvas.create_line(x1, y1, x2, y2, fill="red")  

# Create a function to update the canvas with the current tour
def update_canvas():
    draw_tour(canvas, cities, tour)
    tour_cost = path_cost(tour, cities)
    cost_label.config(text=f"Total Tour Cost: {tour_cost:.2f}")

# Create the Tkinter window
root = tk.Tk()
root.title("TSP Tour Visualization")

# Create a canvas to display the cities and the tour
canvas = tk.Canvas(root, width=800, height=600)
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

# Start the Tkinter main loop
root.mainloop()