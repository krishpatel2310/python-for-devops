import psutil

# Function to get system metrics
def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, memory, disk

# Function to check thresholds
def check_thresholds(cpu, memory, disk, cpu_th, mem_th, disk_th):
    
    print("\n--- System Health Report ---")

    # CPU Check
    if cpu > cpu_th:
        print(f"CPU Usage: {cpu}% ❌ (Above Threshold)")
    else:
        print(f"CPU Usage: {cpu}% ✅ (Normal)")

    # Memory Check
    if memory > mem_th:
        print(f"Memory Usage: {memory}% ❌ (Above Threshold)")
    else:
        print(f"Memory Usage: {memory}% ✅ (Normal)")

    # Disk Check
    if disk > disk_th:
        print(f"Disk Usage: {disk}% ❌ (Above Threshold)")
    else:
        print(f"Disk Usage: {disk}% ✅ (Normal)")

# Main function
def main():
    print("Enter Threshold Values (%)")

    cpu_threshold = float(input("CPU Threshold: "))
    memory_threshold = float(input("Memory Threshold: "))
    disk_threshold = float(input("Disk Threshold: "))

    cpu, memory, disk = get_system_metrics()

    check_thresholds(cpu, memory, disk, cpu_threshold, memory_threshold, disk_threshold)

# Run the script
if __name__ == "__main__":
    main()
