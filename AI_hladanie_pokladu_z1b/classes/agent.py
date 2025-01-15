import random  # Import random module for generating random numbers and choices

class Agent:
    def __init__(self, instructions):
        # Initialize an Agent with a given set of instructions
        self.inst_set = instructions  # The instruction set, which is a list of integers (0-255)
        self.cmd_set = []  # The command set (interpreted instructions, will be filled later)
        self.fit_index = 0  # Fitness index to evaluate the agent's performance
        self.steps = 0  # Number of steps the agent has taken (movement in the environment)
        self.treasures_found = 0  # Number of treasures the agent has found

    def mutate(self, mutation_rate=0.1):
        # Mutate the instruction set based on a mutation rate (default is 10%)
        
        repeat = 0  # Variable to control how many mutation rounds to perform
        
        # Decide the number of mutation rounds based on mutation rate
        if mutation_rate < 0.5:
            repeat = random.randint(0, 4)  # If mutation rate is low, perform 0 to 4 mutation rounds
        else:
            repeat = random.randint(3, 9)  # If mutation rate is high, perform 3 to 9 mutation rounds

        # Perform mutation for the determined number of rounds
        for _ in range(repeat):
            # Iterate through each instruction in the instruction set
            for i in range(len(self.inst_set)):
                # Apply mutation only if a random value is below the mutation rate
                if random.random() < mutation_rate:
                    # Randomly choose a mutation type: swap, increment, or decrement
                    mutation_type = random.choice(['swap', 'increment', 'decrement'])

                    # Mutation type: Swap two random instructions
                    if mutation_type == 'swap':
                        idx1, idx2 = random.sample(range(len(self.inst_set)), 2)  # Pick two distinct random indices
                        # Swap the instructions at the chosen indices
                        self.inst_set[idx1], self.inst_set[idx2] = self.inst_set[idx2], self.inst_set[idx1]

                    # Mutation type: Increment the value of the current instruction (wrap around 256)
                    elif mutation_type == 'increment':
                        self.inst_set[i] = (self.inst_set[i] + 1) % 256  # Increment and ensure value stays within 0-255

                    # Mutation type: Decrement the value of the current instruction (wrap around 256)
                    elif mutation_type == 'decrement':
                        self.inst_set[i] = (self.inst_set[i] - 1) % 256  # Decrement and ensure value stays within 0-255

        return self  # Return the mutated agent (useful for chaining or further processing)
