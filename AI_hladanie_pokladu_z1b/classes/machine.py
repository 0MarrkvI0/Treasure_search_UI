# Custom exception to handle when the number of executed instructions exceeds a limit (500 instructions)
class MaxInstructionsReached(Exception):
    pass

class Machine:
    ARCHITECTURE = 64  # Define the memory architecture size (64 memory addresses)

    def __init__(self):
        # Initialize memory for the machine
        # The memory is a 2D list with 64 addresses. Each address has an index (in binary) and an 8-bit value.
        self.memory = [[0 for _ in range(self.ARCHITECTURE)] for _ in range(2)]
        
        # Fill the first row of memory with the binary representation of each memory index
        for i in range(self.ARCHITECTURE):
            self.memory[0][i] = self.decimal_to_binary(i, 6)  # 6-bit binary representation for the address

        # Clear the second row of memory (data row)
        self.clear_memory()

    def clear_memory(self):
        # Resets the memory by setting all values in the second row (data) to '00000000' (8-bit zeroes)
        for value in range(self.ARCHITECTURE):
            self.memory[1][value] = '0' * 8

    def fill_memory(self, input_arr):
        # Fill the memory with input values from the agent's instruction set
        # Only fills up to 64 memory addresses or the length of the input array, whichever is smaller
        for value in range(min(self.ARCHITECTURE, len(input_arr))):
            if input_arr[value] is not None:
                self.memory[1][value] = self.decimal_to_binary(input_arr[value], 8)  # Convert values to 8-bit binary

    def display_memory(self):
        # Display the memory contents (address in the first row, data in the second row)
        for column in range(len(self.memory[0])):
            print(f"{self.memory[0][column]} {self.memory[1][column]}")
        print()

    def execute_commands(self):
        # Executes the commands stored in memory and generates a movement trajectory for the agent
        instructions = 0  # Counter for the number of executed instructions
        index = 0  # Index in the memory to fetch the next command
        trajectory = []  # List to store the agent's movement commands ('H', 'D', 'P', 'L')

        # Main execution loop that processes commands until the end of memory or an instruction limit is reached
        while index < self.ARCHITECTURE:
            if instructions >= 500: 
                raise MaxInstructionsReached()  # Raise an exception if more than 500 instructions are executed

            current_cmd = self.memory[1][index]  # Fetch the current 8-bit command from memory
            cmd = self.binary_to_decimal(current_cmd[:2])  # The first 2 bits represent the command type
            address = self.binary_to_decimal(current_cmd[2:])  # The last 6 bits represent the memory address
            instructions += 1  # Increment the instruction counter

            # Execute the command based on the 2-bit 'cmd' value
            if cmd == 0:
                # Command 0: Increment the value at the specified memory address
                self.memory[1][address] = self.increment_binary(self.memory[1][address])  
            elif cmd == 1:
                # Command 1: Decrement the value at the specified memory address
                self.memory[1][address] = self.decrement_binary(self.memory[1][address])
            elif cmd == 2:
                # Command 2: Jump to a specified memory address
                index = address  # Set index to the address to jump to
                continue  # Skip the normal index increment to jump directly
            elif cmd == 3:
                # Command 3: Output a movement command based on the number of '1's in the current command
                move = self.count_ones(current_cmd)
                # Decide movement based on the number of '1's (H = Up, D = Down, P = Right, L = Left)
                if move < 3:
                    trajectory.append("H")  # Move Up
                elif 3 <= move < 4:
                    trajectory.append("D")  # Move Down
                elif move in [5, 6]:
                    trajectory.append("P")  # Move Right
                else:
                    trajectory.append("L")  # Move Left
            index += 1  # Move to the next memory address for the next instruction
        return trajectory  # Return the complete movement trajectory of the agent

    # Helper functions for binary operations

    def count_ones(self, binary_str):
        # Counts the number of '1's in the binary string and returns the count
        return binary_str.count('1')

    def decimal_to_binary(self, num, bits):
        # Convert a decimal number to a binary string, ensuring the binary string has a specific number of bits
        binary_str = bin(num)[2:]  # Remove the '0b' prefix from the binary representation
        return binary_str.zfill(bits)  # Pad the binary string with leading zeros to fit the specified bit length

    def binary_to_decimal(self, binary_str):
        # Convert a binary string to its decimal equivalent
        return int(binary_str, 2) 

    def increment_binary(self, binary_str):
        # Increment the binary value (with wrap-around at 255)
        decimal_value = self.binary_to_decimal(binary_str)  # Convert the binary string to a decimal value
        if decimal_value == 255:  # Wrap around if the value is 255 (8-bit max)
            return self.decimal_to_binary(0, 8)  # Reset to 0
        decimal_value += 1  # Increment the decimal value by 1
        return self.decimal_to_binary(decimal_value, 8)  # Convert back to an 8-bit binary string

    def decrement_binary(self, binary_str):
        # Decrement the binary value (with wrap-around at 0)
        decimal_value = self.binary_to_decimal(binary_str)  # Convert the binary string to a decimal value
        if decimal_value == 0:  # Wrap around if the value is 0
            return self.decimal_to_binary(255, 8)  # Reset to 255
        decimal_value -= 1  # Decrement the decimal value by 1
        return self.decimal_to_binary(max(decimal_value, 0), 8)  # Convert back to an 8-bit binary string
