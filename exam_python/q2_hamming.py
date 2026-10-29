# Q2: Hamming Code - encode, introduce single-bit error, detect and correct

data = input("Enter 4 bit binary data: ")

if len(data) != 4:
    print("Invalid input. Enter exactly 4 bits.")
    exit()

for c in data:
    if c != '0' and c != '1':
        print("Invalid input. Only 0 and 1 are allowed.")
        exit()

data_bits = 4
parity_bits = 0

# 2^r >= m + r + 1
while (1 << parity_bits) < data_bits + parity_bits + 1:
    parity_bits += 1

print("Data Bits:", data)
print("Number of Parity bits:", parity_bits)

# ---------------- SENDER ----------------
# index 0 unused, positions 1..7
code = [''] * 8

code[1] = 'P'
code[2] = 'P'
code[3] = data[3]
code[4] = 'P'
code[5] = data[2]
code[6] = data[1]
code[7] = data[0]

print("\nHamming code positions:")
for pos in range(1, 8):
    print("Position", pos, ":", code[pos])

# Even parity: P1, P2, P4
parity_pos = 1
while parity_pos <= 4:
    parity_value = 0
    checked = []

    for pos in range(1, 8):
        if (pos & parity_pos) != 0:
            checked.append(pos)
            if pos != parity_pos:
                parity_value ^= int(code[pos])

    code[parity_pos] = str(parity_value)
    print("P" + str(parity_pos), "checks positions:", checked, "-> P" + str(parity_pos), "=", code[parity_pos])

    parity_pos *= 2

sent = "".join(code[1:])
print("\nTransmitted Hamming Code:", sent)

# ---------------- ERROR ----------------
received = code.copy()

error_bit = int(input("\nEnter bit position to corrupt (1-7, 0 for no error): "))

if 1 <= error_bit <= 7:
    if received[error_bit] == '0':
        received[error_bit] = '1'
    else:
        received[error_bit] = '0'

print("Received Hamming Code   :", "".join(received[1:]))

# ---------------- RECEIVER ----------------
# Recheck each parity group, syndrome gives error position
error_pos = 0
parity_pos = 1
while parity_pos <= 4:
    check = 0

    for pos in range(1, 8):
        if (pos & parity_pos) != 0:
            check ^= int(received[pos])

    print("C" + str(parity_pos), "=", check)

    if check == 1:
        error_pos += parity_pos

    parity_pos *= 2

if error_pos == 0:
    print("\nResult: No error detected in transmission.")
else:
    print("\nResult: Error detected at position", error_pos)

    if received[error_pos] == '0':
        received[error_pos] = '1'
    else:
        received[error_pos] = '0'

    print("Corrected Hamming Code  :", "".join(received[1:]))

# Extract data bits back (positions 7, 6, 5, 3)
original = received[7] + received[6] + received[5] + received[3]
print("Original Data           :", original)
