# Q4: Divide 192.168.1.0/24 into subnets, find subnet mask and usable hosts

address = input("Enter base IP address (e.g., 192.168.1.0): ")
num_subnets = int(input("Enter number of subnets required (e.g., 2): "))

a, b, c, d = address.split(".")

# Borrow n bits from host part such that 2^n >= subnets required
borrowed = 0
while (1 << borrowed) < num_subnets:
    borrowed += 1

prefix = 24 + borrowed

if prefix > 30:
    print("Error: Too many subnets for a /24 network.")
    exit()

host_bits = 32 - prefix
size = 2 ** host_bits
subnet_count = 256 // size
hosts = size - 2
mask = 256 - size

print("\n--- General Subnet Information ---")
print("Original Network       :", address + "/24")
print("Bits Borrowed          :", borrowed)
print("New CIDR Prefix        : /" + str(prefix))
print("Calculated Subnet Mask : 255.255.255." + str(mask))
print("Total Subnets Created  :", subnet_count)
print("Total Usable Hosts     :", hosts, "per subnet (2^" + str(host_bits) + " - 2)\n")

for subnet in range(num_subnets):

    network_address = subnet * size
    first = network_address + 1
    last = network_address + hosts
    broadcast_address = network_address + size - 1

    print("Subnet", subnet + 1)
    print("Network Address   :", a + "." + b + "." + c + "." + str(network_address))
    print("Subnet Mask       : 255.255.255." + str(mask))
    print("First Host        :", a + "." + b + "." + c + "." + str(first))
    print("Last Host         :", a + "." + b + "." + c + "." + str(last))
    print("Broadcast Address :", a + "." + b + "." + c + "." + str(broadcast_address))
    print("Usable Hosts      :", hosts)
    print()
