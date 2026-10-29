# Q6: Distance Vector Routing (Bellman-Ford) - routing tables and shortest path

INF = 999999

n = int(input("Enter number of nodes: "))

nodes = []

for i in range(n):
    nodes.append(chr(65 + i))

cost = []

for i in range(n):
    row = []

    for j in range(n):
        if i == j:
            row.append(0)
        else:
            row.append(INF)

    cost.append(row)

print("Enter -1 if nodes are not connected")

for i in range(n):
    for j in range(i + 1, n):

        value = int(input(nodes[i] + " to " + nodes[j] + ": "))

        if value != -1:
            cost[i][j] = value
            cost[j][i] = value

dist = []
next_hop = []

for i in range(n):

    dist.append(cost[i].copy())

    row = []

    for j in range(n):

        if i == j:
            row.append(i)

        elif cost[i][j] != INF:
            row.append(j)

        else:
            row.append(-1)

    next_hop.append(row)


def print_table(title):

    print("\n", title)

    for i in range(n):

        print("\nRouting Table for", nodes[i])
        print("Destination\tDistance\tNext Hop")

        for j in range(n):

            if dist[i][j] == INF:
                d = "INF"
            else:
                d = dist[i][j]

            if next_hop[i][j] == -1:
                h = "-"
            else:
                h = nodes[next_hop[i][j]]

            print(nodes[j], "\t\t", d, "\t\t", h)


print_table("INITIAL ROUTING TABLES")

changed = True

while changed:

    changed = False

    old = []

    for i in range(n):
        old.append(dist[i].copy())

    for x in range(n):

        for v in range(n):

            if cost[x][v] != INF and x != v:

                for y in range(n):

                    new_dist = cost[x][v] + old[v][y]

                    if new_dist < dist[x][y]:

                        dist[x][y] = new_dist
                        next_hop[x][y] = v
                        changed = True


print_table("FINAL ROUTING TABLES")


# Shortest path between two routers using next hop table
print("\nSHORTEST PATH")
src = input("Enter source node (e.g. A): ").upper()
dst = input("Enter destination node (e.g. C): ").upper()

s = nodes.index(src)
t = nodes.index(dst)

if dist[s][t] == INF:
    print("No path exists from", src, "to", dst)
else:
    path = [src]
    current = s

    while current != t:
        current = next_hop[current][t]
        path.append(nodes[current])

    print("Path         :", " -> ".join(path))
    print("Minimum Cost :", dist[s][t])
