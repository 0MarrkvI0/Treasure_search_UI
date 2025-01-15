from classes.environment import Environment, OutOfBound  # Import custom classes for environment and handling out-of-bound exceptions
from classes.machine import Machine  # Import the Machine class for simulating instruction execution
from classes.population import Population  # Import the Population class to manage agents in the simulation
from classes.agent import Agent  # Import the Agent class which represents an individual in the population
import random  # Import random for generating random instruction sets for agents
import matplotlib.pyplot as plt  # Import matplotlib for visualizing fitness progression

# Input file containing environment configuration (size, start location, treasure locations)
file_path = "resources/input.txt"

# Initialize variables for environment settings and agent parameters
def_environment_size = 0  # Default environment size, to be read from the input file
start_location_xy = []  # Starting location coordinates (x, y), to be read from the input file
treasure_locations_xy = []  # List to store treasure locations (x, y), read from input file

# Variables for managing population and evolutionary parameters
distractor = 0  # Variable to manage random disturbances during evolution
init_num_agents = 201  # Initial number of agents in the population
init_num_instructions = 30  # Number of instructions per agent (instruction set length)

try:
    # Load environment configuration from input file
    with open(file_path, "r") as file:
        def_environment_size = int(file.readline().strip())  # Read environment size (first line)
        start_location_xy = eval(file.readline().strip())  # Read start location (second line)
        for _ in range(int(file.readline().strip())):  # Read number of treasures
            treasure_locations_xy.append(eval(file.readline().strip()))  # Append each treasure location

    # Initialize Environment and Machine instances
    environment = Environment(def_environment_size, start_location_xy, treasure_locations_xy)  # Create the environment with size, start, and treasure locations
    virtual_machine = Machine()  # Create a virtual machine instance to process agent instructions

    # Create a Population instance and add Agents with randomly generated instruction sets
    population = Population()
    for _ in range(init_num_agents):
        # Add agents with random instruction sets (instructions are integers between 0 and 255)
        population.add_agent(Agent([random.randint(0, 255) for _ in range(init_num_instructions)]))

    # Simulation control variables
    solution_found = False  # Flag to indicate if the solution (path to all treasures) was found
    generations = 2000  # Number of generations to run the simulation
    frequency = 200  # Frequency for applying special events like distraction

    # Main evolutionary loop (over generations)
    for i in range(generations):
        # Iterate through each agent in the current generation
        for agent in population.generation:
            virtual_machine.fill_memory(agent.inst_set)  # Load agent's instruction set into the machine's memory
            
            try:
                # Evaluate the agent's commands in the environment
                if environment.evaluate_commands(virtual_machine, agent):
                    # If a valid solution (path) is found, output the agent's command set
                    print("Path Found:", agent.cmd_set)
                    solution_found = True  # Set the solution flag
                    break  # Exit the loop since the solution is found
            except OutOfBound:
                # Handle case where agent moves out of bounds, assigning negative fitness
                agent.fit_index = (agent.treasures_found + 0.1 - (agent.steps / 100)) * -1

            # Clear the machine memory and reset environment for the next agent
            virtual_machine.clear_memory()
            environment.clear_environment(start_location_xy, treasure_locations_xy)

        # Sort agents based on their fitness in descending order
        sorted_agents = sorted(population.generation, key=lambda obj: obj.fit_index, reverse=True)
        best_fitness = sorted_agents[0].fit_index  # Best fitness value in the current generation
        population.fitness_history.append(best_fitness)  # Append best fitness to the history for plotting
        population.first_i = best_fitness  # Store the best fitness value for this generation
        
        # Check if a valid path was found, and if so, print results and exit the loop
        if solution_found:
            break

        print(i)  # Print current generation number for tracking progress

        # Apply random distraction every 'frequency' generations
        if i % frequency == 0 and i != 0:
            # Annotate plot with distraction and create a new generation with forced changes
            plt.annotate('distraction', xy=(i, best_fitness), xytext=(i+5, best_fitness+1), arrowprops=dict(facecolor='red', shrink=0.05))
            population.create_new_generation(True)  # Create new generation with a distraction applied
            frequency = 500  # Increase the frequency interval after the first distraction
            distractor = random.randint(20, 40)  # Randomly set the number of generations to apply distractions
            print("CC:", distractor)
        else:
            # If a distraction is active, apply it, else continue with standard generation
            if distractor > 0:
                population.create_new_generation(True)  # Create a new generation with forced changes
                distractor -= 1  # Decrement the distraction counter
            else:
                population.create_new_generation(False)  # Create a normal new generation

    print("Treasures:",sorted_agents[0].treasures_found)
    print("Steps:", len(sorted_agents[0].cmd_set))  # Output the number of steps in the solution
    print("Generations: ", i)  # Output the generation at which the solution was found
    # Plot the evolution of fitness over generations
    plt.plot(population.fitness_history, marker='o', linestyle='-', color='b')
    plt.title('Fitness Function Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True)
    plt.show()

    print("End of simulation.")  # Print message indicating the end of the simulation

except FileNotFoundError:
    # Handle the case where the input file is not found
    print(f"File {file_path} not found.")
