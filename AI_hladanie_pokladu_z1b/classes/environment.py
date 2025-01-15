from classes.machine import MaxInstructionsReached  # Import custom exception to handle instruction overflow

# Custom exception for when the agent moves out of the defined boundaries
class OutOfBound(Exception):
    pass

class Environment:
    def __init__(self, size, start_location, treasure_locations):
        # Initialize the environment with its size, start location, and treasure locations
        self.size = size  # Size of the square environment (size x size grid)
        self.x = start_location[0]  # Agent's current x-coordinate
        self.y = start_location[1]  # Agent's current y-coordinate
        self.num_treasures = len(treasure_locations)  # Total number of treasures in the environment
        self.base = self.initialize_environment(treasure_locations)  # Set up the environment grid

    def initialize_environment(self, treasure_locations):
        # Create an empty grid and place treasures at specified locations
        base = [[0 for _ in range(self.size)] for _ in range(self.size)]  # Initialize an empty grid
        for treasure in treasure_locations:
            base[treasure[1]][treasure[0]] = 1  # Mark treasure locations with a '1'
        return base

    def clear_environment(self, start_location, treasure_locations):
        # Reset the environment to its initial state (used after each agent evaluation)
        self.x = start_location[0]  # Reset agent's x-coordinate
        self.y = start_location[1]  # Reset agent's y-coordinate
        self.num_treasures = len(treasure_locations)  # Reset the number of treasures
        self.base = self.initialize_environment(treasure_locations)  # Reinitialize the grid with treasures

    def check_coordinates(self, agent):
        # Check if the agent's current position is within bounds and whether there's a treasure
        if 0 <= self.x < self.size and 0 <= self.y < self.size:  # Ensure the agent is within bounds
            if self.base[self.y][self.x] == 1:  # Check if there's a treasure at the current location
                self.base[self.y][self.x] = 0  # Remove the treasure from the grid
                return True  # Return True when treasure is found
            return False  # No treasure at the current location
        else:
            OutOfBound(agent)  # Raise OutOfBound exception if agent goes out of bounds

    def fitness_function(self, agent):
        # Fitness function to evaluate the agent's performance (steps taken and treasures found)
        if self.check_coordinates(agent):
            agent.treasures_found += 1  # Increment treasures found if there's one at the start location

        # Iterate through the agent's command set and move accordingly
        for move in agent.cmd_set:
            if agent.treasures_found == self.num_treasures:  # Stop if all treasures are found
                break
            self.move_agent(move)  # Move the agent based on the command
            if self.check_coordinates(agent):  # Check if agent lands on a treasure after the move
                agent.treasures_found += 1  # Increment treasures found
            agent.steps += 1  # Increment the number of steps taken

        # Calculate fitness based on treasures found and steps taken
        if agent.steps == 0:
            agent.fit_index = 0  # No steps taken, fitness is 0
        else:
            agent.fit_index = agent.treasures_found + 0.1 - (agent.steps / 100)  # Fitness formula

        # Return True if the agent finds all treasures, otherwise return False
        if agent.treasures_found == self.num_treasures:
            return True
        return False

    def move_agent(self, move):
        # Move the agent based on the given command ('H' for up, 'D' for down, 'L' for left, 'P' for right)
        if move == 'H':  
            self.y -= 1  # Move up
        elif move == 'D': 
            self.y += 1  # Move down
        elif move == 'P':  
            self.x += 1  # Move right
        elif move == 'L':  
            self.x -= 1  # Move left

    def evaluate_commands(self, machine, agent):
        try:
            # Use the machine to execute the agent's instruction set
            commands = machine.execute_commands()
        except MaxInstructionsReached:
            # If the machine exceeds the allowed instruction limit, penalize the agent's fitness
            agent.fit_index = -1
            return False
        
        # Set the agent's command set from the machine's execution
        agent.cmd_set = commands
        
        # Calculate the agent's fitness and return whether all treasures are found
        return self.fitness_function(agent)
