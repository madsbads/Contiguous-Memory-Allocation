import sys

class MemoryAllocator:
    def __init__(self, max_size):
        self.max_size = max_size
        self.free_memory = [(0, max_size - 1)]  # Initially one large free block
        self.allocated_memory = {}  # Maps process ID to (start, end) tuples

    def allocate_memory(self, process_id, size, strategy):
        if size <= 0 or size > self.max_size:
            print("Invalid memory size requested.")
            return
        
        hole_index = -1
        if strategy == 'F':  # First Fit
            for i, (start, end) in enumerate(self.free_memory):
                if end - start + 1 >= size:
                    hole_index = i
                    break
        elif strategy == 'B':  # Best Fit
            best_fit = None
            for i, (start, end) in enumerate(self.free_memory):
                if end - start + 1 >= size:
                    if best_fit is None or (end - start + 1) < (self.free_memory[best_fit][1] - self.free_memory[best_fit][0] + 1):
                        best_fit = i
            hole_index = best_fit
        elif strategy == 'W':  # Worst Fit
            worst_fit = None
            for i, (start, end) in enumerate(self.free_memory):
                if end - start + 1 >= size:
                    if worst_fit is None or (end - start + 1) > (self.free_memory[worst_fit][1] - self.free_memory[worst_fit][0] + 1):
                        worst_fit = i
            hole_index = worst_fit
        
        if hole_index == -1:
            print(f"Error: Not enough memory to allocate {size} bytes for process {process_id}.")
            return
        
        # Allocate memory from the selected hole
        start, end = self.free_memory[hole_index]
        if end - start + 1 == size:
            del self.free_memory[hole_index]
        else:
            self.free_memory[hole_index] = (start + size, end)
        
        self.allocated_memory[process_id] = (start, start + size - 1)
        print(f"Allocated {size} bytes to process {process_id}.")
    
    def release_memory(self, process_id):
        if process_id not in self.allocated_memory:
            print(f"Error: Process {process_id} not found.")
            return
        
        start, end = self.allocated_memory.pop(process_id)
        new_hole = (start, end)
        
        # Merge with adjacent holes if possible
        merged = False
        for i, (hole_start, hole_end) in enumerate(self.free_memory):
            if hole_end + 1 == start:
                self.free_memory[i] = (hole_start, end)
                merged = True
                break
            elif end + 1 == hole_start:
                self.free_memory[i] = (start, hole_end)
                merged = True
                break
        
        if not merged:
            self.free_memory.append(new_hole)
        
        self.free_memory.sort()  # Maintain sorted order
        print(f"Released memory of process {process_id}.")
    
    def compact_memory(self):
        if not self.free_memory:
            print("No free memory to compact.")
            return
        
        new_free_memory = []
        current_position = 0
        
        for process_id, (start, end) in sorted(self.allocated_memory.items(), key=lambda item: item[1][0]):
            size = end - start + 1
            if start != current_position:
                self.allocated_memory[process_id] = (current_position, current_position + size - 1)
            current_position += size
        
        new_free_memory.append((current_position, self.max_size - 1))
        self.free_memory = new_free_memory
        print("Memory compacted.")
    
    def print_status(self):
        print("Memory status:")
        for process_id, (start, end) in sorted(self.allocated_memory.items(), key=lambda item: item[1][0]):
            print(f"Addresses [{start}:{end}] Process {process_id}")
        
        for start, end in sorted(self.free_memory):
            print(f"Addresses [{start}:{end}] Unused")
    
    def handle_command(self, command):
        parts = command.split()
        if not parts:
            print("Invalid command.")
            return

        command_type = parts[0]
        if command_type == 'RQ':
            if len(parts) != 4:
                print("Invalid RQ command format.")
                return
            process_id = parts[1]
            try:
                size = int(parts[2])
            except ValueError:
                print("Invalid memory size.")
                return
            strategy = parts[3]
            if strategy not in ['F', 'B', 'W']:
                print("Invalid strategy. Use 'F' for first fit, 'B' for best fit, or 'W' for worst fit.")
                return
            self.allocate_memory(process_id, size, strategy)
        elif command_type == 'RL':
            if len(parts) != 2:
                print("Invalid RL command format.")
                return
            process_id = parts[1]
            self.release_memory(process_id)
        elif command_type == 'C':
            if len(parts) != 1:
                print("Invalid C command format.")
                return
            self.compact_memory()
        elif command_type == 'STAT':
            if len(parts) != 1:
                print("Invalid STAT command format.")
                return
            self.print_status()
        elif command_type == 'X':
            print("Exiting.")
            exit(0)
        else:
            print("Unknown command.")

def main():
    if len(sys.argv) != 2:
        print("Usage: allocator <max_memory_size>")
        return
    
    try:
        max_size = int(sys.argv[1])
    except ValueError:
        print("Invalid memory size. It must be a number.")
        return

    allocator = MemoryAllocator(max_size)
    
    print("allocator>")
    while True:
        try:
            command = input().strip()
            if command:
                allocator.handle_command(command)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
