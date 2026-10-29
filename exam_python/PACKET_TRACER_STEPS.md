# Cisco Packet Tracer – Step-by-Step Guide (Q1, 3, 5, 10, 11, 12, 13, 14)

> Read **Part 0** once. It explains the clicks you use in every question.
> Each question after that lists **what to build → exact clicks → what you should see → how to explain it**.

---

## Part 0 – Packet Tracer Basics (read this first)

### 0.1 Where things are
| What | Where on screen |
|---|---|
| Devices (Router, Switch, PC, Server) | **Bottom-left panel**. Top row = categories, bottom row = models |
| Routers | Network Devices → **Routers** → **2911** (has 3 ports: G0/0, G0/1, G0/2) |
| Switches | Network Devices → **Switches** → **2960** (24 FastEthernet ports + 2 Gigabit ports) |
| PC / Server | End Devices → **PC** / **Server** |
| Cables | **Connections** (orange lightning-bolt icon) |
| Realtime / Simulation switch | **Bottom-right corner** (stay in **Realtime**) |

Drag a device onto the white workspace to add it. Click once on a device to open its window.

### 0.2 Which cable to use
| Connecting | Cable (icon name) |
|---|---|
| PC ↔ Switch, Server ↔ Switch, Switch ↔ Router | **Copper Straight-Through** (solid black line) |
| Switch ↔ Switch, PC ↔ PC, Router ↔ Router (Ethernet) | **Copper Cross-Over** (dashed black line) |
| Not sure? | **Automatically Choose Connection Type** (yellow lightning icon, first one). It always picks correctly |

After you pick a cable, click device 1 → choose a port from the list → click device 2 → choose a port.

**Link lights:**
- 🟢 Green = working
- 🟠 Orange = switch port is starting up (wait 30–60 sec, or press **Fast Forward Time** at the bottom)
- 🔴 Red = wrong cable, or the router port is shut down (you haven't typed `no shutdown`)

### 0.3 Give a PC a static IP address
1. Click the PC → **Desktop** tab → **IP Configuration**
2. Select **Static**
3. Type **IPv4 Address**, **Subnet Mask** (it auto-fills when you press Tab), and **Default Gateway** (needed only if a router exists)
4. Close the window. It saves automatically.

For a **Server**, do the same: Server → **Desktop** → **IP Configuration**.

### 0.4 Ping (test connectivity)
1. Click a PC → **Desktop** → **Command Prompt**
2. Type `ping 192.168.1.3` and press Enter
3. Success = `Reply from 192.168.1.3: bytes=32 time<1ms TTL=128`
4. Failure = `Request timed out` or `Destination host unreachable`

> ⚠️ The **first 1–2 replies may time out** when a router is involved. This is normal: ARP is learning the MAC addresses. Run ping again. All 4 replies should succeed.

You can also ping without typing: use the **closed envelope icon (Add Simple PDU)** on the right toolbar, then click PC1 and PC2. The result shows at the bottom-right as **Successful**.

### 0.5 Open a router's command line
1. Click the router → **CLI** tab
2. If it asks `Would you like to enter the initial configuration dialog? [yes/no]:`, type **no** and press Enter
3. Press Enter again → you see `Router>`

| Prompt | Mode | How you got there |
|---|---|---|
| `Router>` | User mode | Start |
| `Router#` | Privileged mode | `enable` |
| `Router(config)#` | Global config | `configure terminal` (or `conf t`) |
| `Router(config-if)#` | Interface config | `interface g0/0` |
| `Router(config-router)#` | Routing protocol config | `router rip` |

- `exit` goes back one level. `end` goes straight to `Router#`.
- Save the config with `copy running-config startup-config` → Enter (or just `wr`)
- Check the interfaces with `show ip interface brief`. The interfaces you use must show **up / up**.

### 0.6 Save your work
**File → Save As** → e.g. `Q3_subnetting.pkt`

---

## Q1 – Star, Mesh, Bus and Extended Star Topologies

**Goal:** Build 4 topologies, give the devices IPs, ping, then compare them.
All PCs use subnet mask **255.255.255.0** and no gateway (there's no router).
Build all 4 in the same file, side by side, using different IPs for each.

### 1A. Star topology
*One central switch, every PC connects to it.*

```
        PC1
         |
PC2 —— Switch —— PC3
         |
        PC4
```
1. Add **1 switch (2960)** and **4 PCs**
2. Connect each PC → switch with **Copper Straight-Through** (PC: FastEthernet0, Switch: Fa0/1, Fa0/2…)
3. IPs: PC1 `192.168.1.1`, PC2 `192.168.1.2`, PC3 `192.168.1.3`, PC4 `192.168.1.4`
4. Wait for green lights → ping from PC1 to `192.168.1.4` ✅

### 1B. Extended Star topology
*Several stars joined to one central switch. This is a "star of stars".*

```
             Central Switch
             /            \
        Switch A        Switch B
        /     \          /     \
      PC5     PC6      PC7     PC8
```
1. Add **3 switches** (1 central, 2 branch) + **4 PCs**
2. Central switch ↔ Switch A and Central switch ↔ Switch B: **Copper Cross-Over** (use Gig0/1 ports or Fa ports)
3. PCs → their branch switch: **Straight-Through**
4. IPs: PC5 `192.168.1.5`, PC6 `.6`, PC7 `.7`, PC8 `.8`
5. Ping from PC5 to `192.168.1.8` ✅ (the ping goes through 3 switches)

### 1C. Bus topology
*Packet Tracer has no real bus cable. We show the bus as a "backbone" line of switches, with each PC hanging off it.*

```
PC9      PC10     PC11     PC12
 |        |        |        |
SW1 ——— SW2 ——— SW3 ——— SW4      ← this line is the "bus/backbone"
```
1. Add **4 switches** in a straight line + **4 PCs**
2. SW1↔SW2, SW2↔SW3, SW3↔SW4: **Cross-Over**
3. Each PC → its switch: **Straight-Through**
4. IPs: `192.168.1.9`, `.10`, `.11`, `.12`
5. Ping from PC9 to `192.168.1.12` ✅
6. *(Demo for the viva)* Delete the cable SW2–SW3 (**X icon**/Delete tool) → ping fails ❌. This shows that one break in the backbone splits the bus.

### 1D. Mesh topology (full mesh)
*Every switch is connected to every other switch.*

```
SW5 ——— SW6
 | \   / |
 |   X   |
 | /   \ |
SW8 ——— SW7
(each switch also has 1 PC)
```
1. Add **4 switches** + **4 PCs**
2. Links (all **Cross-Over**): SW5–SW6, SW5–SW7, SW5–SW8, SW6–SW7, SW6–SW8, SW7–SW8 = **6 links** (formula: n(n−1)/2 = 4×3/2 = 6)
3. Each PC → its switch: **Straight-Through**
4. IPs: `192.168.1.13`, `.14`, `.15`, `.16`
5. Some link lights stay **orange**. That's **STP (Spanning Tree Protocol)** blocking the extra paths so packets don't loop forever. This is correct.
6. Ping from PC13 to `192.168.1.16` ✅
7. *(Demo)* Delete one switch-to-switch cable → ping **still works** ✅ (STP opens a backup path). This is mesh's fault tolerance.

### Comparison table (write this in your answer)
| Feature | Star | Extended Star | Bus | Mesh |
|---|---|---|---|---|
| **Cost** | Low (1 switch, 1 cable per PC) | Medium (more switches) | **Lowest** (least cable) | **Highest** (n(n−1)/2 links, many ports) |
| **Reliability** | Good. Central switch is a single point of failure | Good. A branch failure affects only that branch | Poor | **Highest** |
| **Fault tolerance** | One PC cable fails → only that PC is down. Switch fails → all down | Branch switch fails → only that branch is down | One break → network splits / everything down | Link fails → traffic takes another path |
| **Adding devices** | Easy | Very easy (add a branch) | Easy but slows the bus | Hard (connect to all) |
| **Troubleshooting** | Easy | Easy | Hard | Hard |
| **Used in** | Small labs/offices | College campus, big buildings | Old LANs | WAN backbones, data centres |

**Conclusion for the college:** use **Extended Star**, with one switch per lab connected to a core switch in the admin office. It's cheap, scales well, and a fault in one lab doesn't affect the others.

---

## Q3 – Subnetting 192.168.1.0/24 into Two Labs (with Router)

### Step 1: Calculate (write this on paper)
- Need **2 subnets** → 2ⁿ ≥ 2 → **n = 1 bit borrowed**
- New prefix = 24 + 1 = **/25**
- Subnet mask = 11111111.11111111.11111111.**1**0000000 = **255.255.255.128**
- Host bits = 32 − 25 = 7 → addresses per subnet = 2⁷ = **128**, usable hosts = 128 − 2 = **126**

| | **Subnet 1 – Lab A** | **Subnet 2 – Lab B** |
|---|---|---|
| Network ID | 192.168.1.0 /25 | 192.168.1.128 /25 |
| Router (gateway) | 192.168.1.1 | 192.168.1.129 |
| PC-A1 | 192.168.1.2 | — |
| PC-A2 | 192.168.1.3 | — |
| PC-B1 | — | 192.168.1.130 |
| PC-B2 | — | 192.168.1.131 |
| Broadcast | 192.168.1.127 | 192.168.1.255 |
| Mask | 255.255.255.128 | 255.255.255.128 |

### Step 2: Build
```
PC-A1  PC-A2                 PC-B1  PC-B2
   \    /                       \    /
  Switch-A —— G0/0 Router G0/1 —— Switch-B
```
1. Add **1 Router (2911)**, **2 Switches (2960)**, **4 PCs**
2. PCs → their switch: **Straight-Through**
3. Switch-A → Router **GigabitEthernet0/0**: **Straight-Through**
4. Switch-B → Router **GigabitEthernet0/1**: **Straight-Through**
5. The router links are **red**. That's normal until you configure the router.

### Step 3: Configure the router (Router → CLI)
```
no                                   ← answer to the setup dialog
enable
configure terminal
interface g0/0
 ip address 192.168.1.1 255.255.255.128
 no shutdown
 exit
interface g0/1
 ip address 192.168.1.129 255.255.255.128
 no shutdown
 end
copy running-config startup-config
show ip interface brief
```
✅ G0/0 and G0/1 show **up up**, and the links turn green.

### Step 4: Configure the PCs (Desktop → IP Configuration → Static)
| PC | IP | Mask | Default Gateway |
|---|---|---|---|
| PC-A1 | 192.168.1.2 | 255.255.255.128 | **192.168.1.1** |
| PC-A2 | 192.168.1.3 | 255.255.255.128 | **192.168.1.1** |
| PC-B1 | 192.168.1.130 | 255.255.255.128 | **192.168.1.129** |
| PC-B2 | 192.168.1.131 | 255.255.255.128 | **192.168.1.129** |

> ⚠️ Type the mask **255.255.255.128** yourself. Packet Tracer auto-fills 255.255.255.0, which is **wrong** here.

### Step 5: Verify
- PC-A1 → `ping 192.168.1.3` (same lab) ✅
- PC-A1 → `ping 192.168.1.130` (other lab, goes through the router) ✅ (the first reply may time out)
- PC-A1 → `tracert 192.168.1.130` shows the hop through 192.168.1.1

**Why a router?** The two subnets are different networks. A switch can't move packets between networks, but a router can.

---

## Q5 – RIP Routing Between 3 Branch Offices

### Topology
```
 PC1                           PC2                           PC3
  |                             |                             |
 SW1                           SW2                           SW3
  | G0/0                        | G0/0                        | G0/0
 R1 G0/1 ———— 10.0.0.0/30 ———— G0/1 R2 G0/2 ———— 10.0.0.4/30 ———— G0/1 R3
```

### IP plan
| Device | Interface | IP Address | Mask |
|---|---|---|---|
| R1 | G0/0 (LAN 1) | 192.168.1.1 | 255.255.255.0 |
| R1 | G0/1 (to R2) | 10.0.0.1 | 255.255.255.252 |
| R2 | G0/0 (LAN 2) | 192.168.2.1 | 255.255.255.0 |
| R2 | G0/1 (to R1) | 10.0.0.2 | 255.255.255.252 |
| R2 | G0/2 (to R3) | 10.0.0.5 | 255.255.255.252 |
| R3 | G0/0 (LAN 3) | 192.168.3.1 | 255.255.255.0 |
| R3 | G0/1 (to R2) | 10.0.0.6 | 255.255.255.252 |
| PC1 | | 192.168.1.2 | 255.255.255.0, GW 192.168.1.1 |
| PC2 | | 192.168.2.2 | 255.255.255.0, GW 192.168.2.1 |
| PC3 | | 192.168.3.2 | 255.255.255.0, GW 192.168.3.1 |

(/30 = 255.255.255.252 gives exactly 2 usable IPs, which is perfect for a router-to-router link.)

### Build
1. Add **3 Routers (2911)**, **3 Switches**, **3 PCs**
2. PC → Switch, Switch → Router G0/0: **Straight-Through**
3. R1 G0/1 ↔ R2 G0/1 and R2 G0/2 ↔ R3 G0/1: **Copper Cross-Over**

### Configure R1 (CLI)
```
enable
conf t
hostname R1
interface g0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
 exit
router rip
 version 2
 no auto-summary
 network 192.168.1.0
 network 10.0.0.0
 end
wr
```

### Configure R2
```
enable
conf t
hostname R2
interface g0/0
 ip address 192.168.2.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 10.0.0.2 255.255.255.252
 no shutdown
 exit
interface g0/2
 ip address 10.0.0.5 255.255.255.252
 no shutdown
 exit
router rip
 version 2
 no auto-summary
 network 192.168.2.0
 network 10.0.0.0
 end
wr
```

### Configure R3
```
enable
conf t
hostname R3
interface g0/0
 ip address 192.168.3.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 10.0.0.6 255.255.255.252
 no shutdown
 exit
router rip
 version 2
 no auto-summary
 network 192.168.3.0
 network 10.0.0.0
 end
wr
```

**What each RIP line means:**
- `router rip` turns on RIP (a Distance Vector protocol)
- `version 2` uses RIPv2, which sends subnet masks (classless)
- `no auto-summary` stops RIP from shrinking networks back to their class boundary
- `network X` means "advertise this directly-connected network and send RIP updates out of it"

### Verify
1. Wait **about 30 seconds** (RIP sends updates every 30 sec), or press Fast Forward Time
2. On R1: `show ip route`. You should see lines starting with **R**:
   ```
   R    192.168.2.0/24 [120/1] via 10.0.0.2, GigabitEthernet0/1
   R    192.168.3.0/24 [120/2] via 10.0.0.2, GigabitEthernet0/1
   ```
   `[120/2]` = **120** is RIP's administrative distance, **2** is the hop count
3. `show ip protocols` shows that RIP is running and the networks it advertises
4. PC1 → `ping 192.168.3.2` ✅ (PC1 to PC3, through all 3 routers)
5. PC1 → `tracert 192.168.3.2` shows 192.168.1.1 → 10.0.0.2 → 10.0.0.6 → PC3

**Key points:** RIP uses **hop count** as its metric. The maximum is 15 hops (16 = unreachable). Updates are sent every 30 sec.

---

## Q10 – 20 PCs + Switch: DHCP, DNS and Web Server

### Topology
```
         Server (192.168.1.2)
              |
   PC1 —— Switch (2960) —— PC2 … PC20
```
1. Add **1 Switch (2960)**, **1 Server**, and PCs (**20 if time allows**; otherwise add 3–4 and say "the rest are configured the same way". Tip: select one configured PC, **Ctrl+C / Ctrl+V** to copy it)
2. Connect everything to the switch with **Straight-Through**

### Step 1: Server static IP
Server → **Desktop** → **IP Configuration** → **Static**
- IP **192.168.1.2**, Mask **255.255.255.0**, Gateway **192.168.1.1**, DNS Server **192.168.1.2**

### Step 2: DHCP service (gives IPs to all the PCs)
Server → **Services** tab → **DHCP** (left list)
1. Interface: FastEthernet0, Service: **On**
2. Fill in the `serverPool` row:
   - Default Gateway: **192.168.1.1**
   - DNS Server: **192.168.1.2** ← very important (PCs learn the DNS server from here)
   - Start IP Address: **192.168.1.10**
   - Subnet Mask: **255.255.255.0**
   - Maximum Number of Users: **50**
3. Click **Save**

### Step 3: DNS service (name → IP)
Server → Services → **DNS**
1. DNS Service: **On**
2. Name: **www.college.com**, Type: **A Record**, Address: **192.168.1.2**
3. Click **Add**. It appears in the list below.

### Step 4: HTTP service (the website)
Server → Services → **HTTP**
1. HTTP: **On** (HTTPS can stay On too)
2. *(Optional)* Click **edit** next to `index.html` → change the text to `<h1>Welcome to ABC College</h1>` → **Save**

### Step 5: PCs get IPs automatically
Each PC → Desktop → **IP Configuration** → select **DHCP**
- It shows "**DHCP request successful**" and fills in IP 192.168.1.10, .11, .12… with gateway and DNS 192.168.1.2
- If it says "DHCP failed", click Static, then DHCP again

### Step 6: Verify
1. PC → Command Prompt → `ipconfig /all` shows the IP and DNS server = 192.168.1.2
2. PC → `ping www.college.com` → `Pinging 192.168.1.2…` replies ✅ (this proves DNS works)
3. PC → Desktop → **Web Browser** → type **www.college.com** → **Go** → the college page appears ✅

**Explain:** DHCP = automatic IP, mask, gateway and DNS. DNS = turns `www.college.com` into 192.168.1.2. HTTP = serves the web page (port 80).

---

## Q11 – Email Server (2 users exchange mail)

### Topology
```
PC1 (user1) —— Switch —— PC2 (user2)
                  |
           Mail Server (192.168.1.2)
```

### Step 1: IPs
| Device | IP | Mask | DNS |
|---|---|---|---|
| Server | 192.168.1.2 | 255.255.255.0 | 192.168.1.2 |
| PC1 | 192.168.1.10 | 255.255.255.0 | 192.168.1.2 |
| PC2 | 192.168.1.11 | 255.255.255.0 | 192.168.1.2 |

### Step 2: DNS record for the mail server
Server → Services → **DNS** → **On** → Name **mail.company.com**, Type **A Record**, Address **192.168.1.2** → **Add**

### Step 3: EMAIL service + user accounts
Server → Services → **EMAIL**
1. SMTP Service: **On** (sends mail, port 25)
2. POP3 Service: **On** (receives mail, port 110)
3. Domain Name: **company.com** → click **Set**
4. User Setup:
   - User: **user1**, Password: **1234** → click **+**
   - User: **user2**, Password: **1234** → click **+**
   - Both users appear in the list ✅

### Step 4: Configure the email client on PC1
PC1 → Desktop → **Email** → a configuration form opens:
| Field | Value |
|---|---|
| Your Name | User One |
| Email Address | **user1@company.com** |
| Incoming Mail Server | **mail.company.com** (or 192.168.1.2) |
| Outgoing Mail Server | **mail.company.com** (or 192.168.1.2) |
| User Name | **user1** |
| Password | **1234** |
Click **Save**.

Do the same on **PC2** with `user2@company.com` / `user2` / `1234`.

### Step 5: Send and receive
1. PC1 → Email → **Compose** → To: **user2@company.com**, Subject: `Test`, Body: `Hello from user1` → **Send**
   - The bottom bar says "**Send Success**"
2. PC2 → Email → **Receive** → the mail from user1 appears ✅ → open it
3. *(Optional)* Reply from PC2 → PC1 clicks Receive ✅

**Explain:** **SMTP** = protocol for *sending* mail (client → server). **POP3** = protocol for *downloading* mail from the server to the client.

---

## Q12 – Two Departments + Router: DHCP, DNS and Web

### Topology
```
 Dept A (192.168.1.0/24)                 Dept B (192.168.2.0/24)
 PC-A1  PC-A2   Server                   PC-B1  PC-B2
    \     |     /                           \    /
      Switch-A ——— G0/0  Router  G0/1 ——— Switch-B
```
1. **1 Router (2911)**, **2 Switches**, **1 Server**, **2 PCs per department**
2. Everything uses **Straight-Through**. Switch-A → Router G0/0, Switch-B → Router G0/1

### Step 1: Router (CLI)
```
enable
conf t
interface g0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit
interface g0/1
 ip address 192.168.2.1 255.255.255.0
 ip helper-address 192.168.1.2
 no shutdown
 end
wr
```
**`ip helper-address 192.168.1.2`**: DHCP requests are **broadcasts**, and routers do **not** forward broadcasts. This command makes the router pass Dept B's DHCP requests on to the server in Dept A. Without it, Dept B PCs won't get IPs.

### Step 2: Server static IP
IP **192.168.1.2**, Mask **255.255.255.0**, Gateway **192.168.1.1** (it needs the gateway to reply to Dept B), DNS **192.168.1.2**

### Step 3: DHCP (two pools, one per department)
Server → Services → DHCP → **On**
1. Edit the existing **serverPool** (Dept A):
   - Gateway **192.168.1.1**, DNS **192.168.1.2**, Start **192.168.1.10**, Mask **255.255.255.0**, Max users **50** → **Save**
2. Create the Dept B pool: change **Pool Name** to **deptB**
   - Gateway **192.168.2.1**, DNS **192.168.1.2**, Start **192.168.2.10**, Mask **255.255.255.0**, Max users **50** → click **Add**
3. Both pools now appear in the table ✅

### Step 4: DNS + HTTP
- DNS **On** → `www.college.com` → A Record → `192.168.1.2` → **Add**
- HTTP **On**

### Step 5: PCs → DHCP
All PCs → IP Configuration → **DHCP**
- Dept A PCs get **192.168.1.x**
- Dept B PCs get **192.168.2.x** (with gateway 192.168.2.1)

### Step 6: Verify
1. PC-B1 → `ping 192.168.1.10` (to Dept A) ✅
2. PC-A1 and PC-B1 → `ping www.college.com` ✅
3. PC-A1 and PC-B1 → Web Browser → **www.college.com** → page loads ✅

*Alternative (if the examiner asks for DHCP on the router instead of the server):*
```
conf t
ip dhcp excluded-address 192.168.1.1 192.168.1.9
ip dhcp excluded-address 192.168.2.1 192.168.2.9
ip dhcp pool DEPT_A
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 192.168.1.2
 exit
ip dhcp pool DEPT_B
 network 192.168.2.0 255.255.255.0
 default-router 192.168.2.1
 dns-server 192.168.1.2
 end
```
(In this case remove the helper-address with `no ip helper-address 192.168.1.2` under g0/1, and turn the server's DHCP **Off**.)

---

## Q13 – University: DHCP + DNS + Web + Email

This is **Q10 + Q11 together** on one server.

### Topology
```
Student-PC1  Student-PC2  Faculty-PC1  Faculty-PC2
       \         |          |         /
                 Switch (2960)
                     |
           Server (192.168.1.2)
```

### Server setup (in this order)
1. **IP Configuration**: Static, 192.168.1.2 / 255.255.255.0, Gateway 192.168.1.1, DNS 192.168.1.2
2. **DHCP**: On → serverPool: Gateway 192.168.1.1, **DNS 192.168.1.2**, Start 192.168.1.10, Mask 255.255.255.0, Max 50 → **Save**
3. **DNS**: On → add two A Records:
   - `www.university.com` → 192.168.1.2 → **Add**
   - `mail.university.com` → 192.168.1.2 → **Add**
4. **HTTP**: On (edit index.html to say "Welcome to XYZ University")
5. **EMAIL**: SMTP On, POP3 On, Domain **university.com** → **Set**
   - Users: `student` / `1234` → **+**, `faculty` / `1234` → **+**

### PCs
1. All PCs → IP Configuration → **DHCP** ✅
2. Student PC → Desktop → Email → Name: Student, Email **student@university.com**, Incoming/Outgoing: **mail.university.com**, User **student**, Pass **1234** → Save
3. Faculty PC → same with **faculty@university.com** / faculty / 1234

### Verify
1. Any PC → Web Browser → **www.university.com** → page loads ✅
2. Student → Compose → To **faculty@university.com** → Send → "Send Success"
3. Faculty → **Receive** → mail arrives ✅

---

## Q14 – Troubleshooting: IP Works, but the Website Name Doesn't

### The problem
- PCs **do** get IPs from DHCP ✅
- `ping 192.168.1.2` works ✅
- But the browser shows **"Host Name Unresolved"** for `www.college.com` ❌

That means the network is fine, and the **name → IP translation (DNS) is broken**.

### Setup (build Q10 first)
Build the Q10 network: switch, server 192.168.1.2 with DHCP + DNS + HTTP, and PCs on DHCP.
The examiner may give you a broken file, or ask you to break it yourself and then fix it.

### Find the fault: check in this order
| # | Check | Where | Wrong value (the fault) | Fix |
|---|---|---|---|---|
| 1 | PC's DNS server | PC → Desktop → IP Configuration (or `ipconfig /all`) | DNS Server is **0.0.0.0** / blank / wrong IP | Server → Services → DHCP → set **DNS Server = 192.168.1.2** → **Save**. Then on the PC click **Static** → **DHCP** again to renew |
| 2 | DNS service on | Server → Services → DNS | DNS Service is **Off** | Turn it **On** |
| 3 | DNS record | Server → Services → DNS → record list | Name misspelled (`www.colege.com`), or wrong address (e.g. 192.168.1.5), or record missing | Remove the wrong record, then add `www.college.com` → A Record → **192.168.1.2** |
| 4 | Web service on | Server → Services → HTTP | HTTP **Off** (then even `http://192.168.1.2` fails) | Turn **HTTP On** |
| 5 | Server IP | Server → Desktop → IP Configuration | Server IP is not 192.168.1.2, or it's on DHCP | Set it to Static 192.168.1.2 |

**Most common answer:** fault #1. The **DHCP pool's DNS Server field is wrong**, so the PCs never learn where the DNS server is.

### Prove it's fixed
1. PC → Command Prompt → `nslookup www.college.com` → `Name: www.college.com  Address: 192.168.1.2` ✅
2. PC → `ping www.college.com` ✅
3. PC → Web Browser → `www.college.com` → page loads ✅

### How to explain it in the viva
> "DHCP gives each PC an IP, mask, gateway **and the DNS server address**. Since ping by IP worked, the network was fine. The browser needs DNS to turn www.college.com into 192.168.1.2. The DHCP pool had the wrong DNS server address (or the DNS service/record was wrong), so the name could not be resolved. I corrected it, renewed the IP on the PCs, and verified with nslookup and the web browser."

---

## Common Mistakes Checklist (if something doesn't work)
| Symptom | Likely cause | Fix |
|---|---|---|
| Red link on a router | Interface is shut down | `interface gX/X` → `no shutdown` |
| Red link between two switches | Wrong cable | Use **Cross-Over** (or the auto cable) |
| Orange link | Port still starting up / STP blocking | Wait, or press **Fast Forward Time** |
| Ping to another network fails | PC has no / wrong **Default Gateway** | Set the gateway to the router's IP for that LAN |
| First ping replies time out | ARP learning | Ping again |
| Wrong mask after subnetting | PT auto-filled 255.255.255.0 | Type the correct mask (e.g. .128) |
| RIP routes missing | Waited too little / `network` typo / no `version 2` | Wait 30 sec, check with `show ip protocols` |
| Dept B gets no DHCP IP | Missing `ip helper-address` | Add it on the router interface facing Dept B |
| DHCP gives the wrong DNS | DHCP pool DNS field wrong | Fix it in the pool → Save → renew on the PC |
| Mail "Send Failed" | Wrong server name, domain not **Set**, or user not added | Recheck EMAIL service + client settings |
| `% Invalid input` in the CLI | Wrong mode | `end` → `conf t` → retry |

---

## Quick Viva Answers
- **Hub vs Switch vs Router:** Hub sends to all ports (layer 1). Switch sends by **MAC** address (layer 2). Router forwards between networks by **IP** address (layer 3).
- **Straight vs Cross-over:** Straight-through for *different* devices (PC–switch). Cross-over for *same* devices (switch–switch, PC–PC).
- **Why subnet?** Smaller broadcast domains, better security, less IP wastage.
- **/25 hosts:** 2⁷ − 2 = 126 (minus Network ID and Broadcast).
- **RIP:** Distance vector protocol, metric = hop count, max 15, updates every 30 sec, AD = 120.
- **DHCP steps (DORA):** **D**iscover → **O**ffer → **R**equest → **A**cknowledge.
- **DNS:** Converts a domain name to an IP address. Uses port 53.
- **Ports:** HTTP 80, HTTPS 443, DNS 53, DHCP 67/68, SMTP 25, POP3 110.
- **ping:** Uses **ICMP** Echo Request / Echo Reply to test connectivity.
- **tracert:** Shows each router (hop) a packet passes through.
