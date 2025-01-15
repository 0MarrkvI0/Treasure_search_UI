import random
from classes.agent import Agent  # Importing the Agent class to create and manage agents

class Population():
    
    def __init__(self):
        self.generation = []  # List to store the current generation of agents
        self.num_agents = 0  # Number of agents in the current generation
        self.fitness_history = []  # To track fitness progression across generations
        self.first_i = 0  # This could be used as a starting index for future implementations

    def __getitem__(self, index):
        # Enables indexing into the Population object directly, e.g., population[index]
        return self.generation[index] 
    
    def add_agent(self, agent):
        # Add a new agent to the current generation and increment the agent count
        self.generation.append(agent)
        self.num_agents += 1

    def create_new_generation(self, distaction):
        # Sort the generation based on the fitness index, highest fit agents come first
        self.generation = sorted(self.generation, key=lambda obj: obj.fit_index, reverse=True)
        new_generation = []  # New list to store agents for the next generation

        if not distaction:
            # If distaction is not applied, we apply standard elitism and crossover
            num_elite = round(1)  # Number of elite agents to carry over to the next generation (1 in this case)
            
            # Retain the elite agents (top performers)
            for i in range(num_elite):
                new_generation.append(Agent(self.generation[i].inst_set))

            new_generation_length = len(new_generation)

            # Fill the rest of the new generation with offspring from crossover
            for i in range((self.num_agents - new_generation_length) // 2):
                random_fx = random.sample(self.generation, 4)  # Randomly select 4 agents for the tournament

                # Perform two tournaments and select the two best parents
                parent1 = self.tournament(random_fx[0], random_fx[1])
                parent2 = self.tournament(random_fx[2], random_fx[3])

                # Perform crossover to generate two children
                childs = self.crossover(parent1, parent2)

                # Add the offspring to the new generation
                new_generation.append(childs[0])
                new_generation.append(childs[1])
        else:
            # If distaction is applied, we use a different crossover mechanism
            num_elite = round(1)  # Keep one elite agent as before
            for i in range(num_elite):
                new_generation.append(Agent(self.generation[i].inst_set))

            new_generation_length = len(new_generation)

            # Fill the rest of the generation with offspring using the random crossover method
            for i in range((self.num_agents - new_generation_length) // 2):
                parent1 = self.generation[random.randint(0, self.num_agents - 1)]  # Random parent
                parent2 = max(random.sample(self.generation, 3), key=lambda agent: agent.fit_index)  # Best of 3

                # Perform random crossover
                childs = self.random_crossover(parent1, parent2)

                # Add the offspring to the new generation
                new_generation.append(childs[0])
                new_generation.append(childs[1])

        # Update the current generation with the new generation
        self.generation = new_generation

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents
        parse_point = random.randint(0, len(parent1.inst_set))  # Choose a random crossover point

        # The better-fit parent starts the instruction set
        if parent1.fit_index > parent2.fit_index:
            # First child: Beginning from parent1, end from parent2
            child1 = parent1.inst_set[:parse_point] + parent2.inst_set[:len(parent1.inst_set) - parse_point]
            # Second child: Beginning from parent1, end from parent2 but with different crossover point
            child2 = parent1.inst_set[:parse_point] + parent2.inst_set[parse_point:]
        else:
            # Reverse roles if parent2 has a better fitness index
            child1 = parent2.inst_set[:parse_point] + parent1.inst_set[:len(parent1.inst_set) - parse_point]
            child2 = parent2.inst_set[:parse_point] + parent1.inst_set[parse_point:]

        # Set mutation rate based on the similarity of parents
        mutation_rate = 0.5 if parent1 == parent2 else 0.1  # Higher mutation if parents are identical

        # Return two new agents with the crossover result, applying mutation
        return Agent(child1).mutate(mutation_rate), Agent(child2).mutate(mutation_rate)

    def random_crossover(self, parent1, parent2):
        # Perform random crossover between two parents
        parse_point = random.randint(0, len(parent1.inst_set))  # Choose a random crossover point

        # Cross the instruction sets
        child1 = parent1.inst_set[parse_point:] + parent2.inst_set[:parse_point]
        child2 = parent2.inst_set[parse_point:] + parent1.inst_set[:parse_point]

        # Set a higher mutation rate for random crossover
        mutation_rate = 0.9 if parent1 == parent2 else 0.7

        # Return two new agents with mutation applied
        return Agent(child1).mutate(mutation_rate), Agent(child2).mutate(mutation_rate)

    def tournament(self, parent1, parent2):
        # Perform a tournament selection between two parents
        if parent1 == parent2:
            return random.choice([parent1, parent2])  # If identical, randomly choose one
        if parent1.fit_index > parent2.fit_index:
            return parent1  # Return the better-fit parent
        else:
            return parent2  # Return the better-fit parent
