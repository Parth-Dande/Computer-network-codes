# Packet Tracer Steps: Q1, 3, 5, 10–14

Cable rule: **PC↔Switch / Switch↔Router = Copper Straight-Through**. **PC↔PC, Switch↔Switch, Router↔Router (Ethernet) = Copper Cross-Over**. Router↔Router can also use **Serial DCE** (only if both routers have a serial port; otherwise use Gigabit ports with cross-over).
To set a static IP: PC → Desktop → IP Configuration → Static. Test with: PC → Desktop → Command Prompt → `ping <ip>`

---

## Q1. Star, Mesh, Bus, Extended Star

| Topology | Build | IPs (one network for all) |
|---|---|---|
| Star | 1 switch + 4 PCs | 192.168.1.1–4 /24 |
| Extended Star | 1 central switch → 2 switches (cross-over), 2–3 PCs on each | 192.168.1.10–15 |
| Bus | 3–4 switches in a line (cross-over) = the "backbone", 1 PC on each switch | 192.168.1.20–23 |
| Mesh | 4 switches, every switch connected to every other one (6 links, cross-over), 1 PC on each | 192.168.1.30–33 |

(Mesh: STP blocks the extra links. Wait until the link lights turn green/amber before you ping.)
Verify: ping from the first PC to the last PC in every topology.

**Comparison**

| | Star | Extended Star | Bus | Mesh |
|---|---|---|---|---|
| Cost | Low–medium (1 switch) | Medium | Lowest (least cable) | Highest (n(n−1)/2 links) |
| Reliability | Good; central device is the single point of failure | Good; a branch switch failure affects only that branch | Poor; one break in the backbone splits the network | Highest |
| Fault tolerance | One cable fails → only that PC goes down | Partial | Very low | Very high (other paths available) |
| Troubleshooting | Easy | Easy | Hard | Hard |

---

## Q3. 192.168.1.0/24 split into two subnets (Packet Tracer)

Calculation: 2 subnets → borrow 1 bit → **/25 = 255.255.255.128**, 126 hosts each.

| | Subnet 1 (Lab A) | Subnet 2 (Lab B) |
|---|---|---|
| Network | 192.168.1.0/25 | 192.168.1.128/25 |
| Gateway (router) | 192.168.1.1 | 192.168.1.129 |
| PCs | .2, .3 | .130, .131 |
| Mask | 255.255.255.128 | 255.255.255.128 |

Build: Router (1941/2911) → G0/0 to Switch1 → PCs of Lab A; G0/1 to Switch2 → PCs of Lab B.

```
enable
conf t
int g0/0
 ip address 192.168.1.1 255.255.255.128
 no shut
int g0/1
 ip address 192.168.1.129 255.255.255.128
 no shut
end
```
On each PC, set the Default Gateway to its own subnet's router IP. Then ping 192.168.1.130 from 192.168.1.2.

---

## Q5. RIP across three branches (three routers)

Topology: R1 — R2 — R3 in a line, plus a switch and a PC behind each router.

| Link / LAN | Network | Router IPs |
|---|---|---|
| LAN1 (R1 G0/0) | 192.168.1.0/24 | R1 .1, PC .2 |
| LAN2 (R2 G0/0) | 192.168.2.0/24 | R2 .1, PC .2 |
| LAN3 (R3 G0/0) | 192.168.3.0/24 | R3 .1, PC .2 |
| R1–R2 | 10.0.0.0/30 | R1 10.0.0.1, R2 10.0.0.2 |
| R2–R3 | 10.0.0.4/30 | R2 10.0.0.5, R3 10.0.0.6 |

(Router–router: use G0/1 and G0/2 on 2911 routers with a cross-over cable. Or add HWIC-2T for Serial: power off the router → drag the module in → power on. Set `clock rate 64000` on the DCE end.)

R1:
```
enable
conf t
int g0/0
 ip address 192.168.1.1 255.255.255.0
 no shut
int g0/1
 ip address 10.0.0.1 255.255.255.252
 no shut
router rip
 version 2
 no auto-summary
 network 192.168.1.0
 network 10.0.0.0
end
```
R2: G0/0 192.168.2.1, G0/1 10.0.0.2, G0/2 10.0.0.5 → `router rip` / `version 2` / `no auto-summary` / `network 192.168.2.0` / `network 10.0.0.0`
R3: G0/0 192.168.3.1, G0/1 10.0.0.6 → `network 192.168.3.0` / `network 10.0.0.0`

Verify: `show ip route` (routes marked **R**), `show ip protocols`. Then ping 192.168.3.2 from PC1.

---

## Q10. 20 PCs + switch with DHCP, DNS and Web server

Build: 1 switch (2960 has 24 ports) + 20 PCs + 1 Server (can be fewer PCs in the demo; say "same for all 20").

Server: static IP **192.168.1.2 / 255.255.255.0**. Then go to Services:
1. **DHCP** → On. Pool: Default Gateway 192.168.1.1, **DNS Server 192.168.1.2**, Start IP 192.168.1.10, Subnet 255.255.255.0, Max users 50 → **Save**.
2. **DNS** → On. Name `www.college.com`, Type A Record, Address 192.168.1.2 → **Add**.
3. **HTTP** → HTTP On (you can edit index.html to show the college name).

On every PC: IP Configuration → **DHCP** (it should get 192.168.1.x).
Verify: PC → Desktop → Web Browser → `www.college.com`. You can also run `ping www.college.com` in Command Prompt.

---

## Q11. Email server

Server static IP 192.168.1.2/24. PCs at 192.168.1.10 and .11 (static, or use DHCP as in Q10).
Server → Services:
1. **DNS** → On. Add `mail.company.com` A record → 192.168.1.2.
2. **EMAIL** → SMTP On, POP3 On. Domain name `company.com` → **Set**. Users: `user1` / `1234` → +, `user2` / `1234` → +.

PC1 → Desktop → **Email** → configure:
Your Name: User1, Email: `user1@company.com`, Incoming & Outgoing Mail Server: `192.168.1.2` (or `mail.company.com`), User Name: user1, Password: 1234 → **Save**.
Configure PC2 the same way with user2.
Verify: PC1 → Compose → To `user2@company.com` → Send. PC2 → Receive → the mail should appear.

---

## Q12. Two departments + router + DHCP/DNS/Web

Router G0/0 → Switch1 (Dept A + **Server**), G0/1 → Switch2 (Dept B).

```
enable
conf t
int g0/0
 ip address 192.168.1.1 255.255.255.0
 no shut
int g0/1
 ip address 192.168.2.1 255.255.255.0
 ip helper-address 192.168.1.2
 no shut
end
```
(`ip helper-address` forwards Dept B's DHCP broadcasts to the server.)

Server: static 192.168.1.2, GW 192.168.1.1. DHCP service, **two pools**:
- `serverPool` (default): GW 192.168.1.1, DNS 192.168.1.2, start 192.168.1.10, mask 255.255.255.0 → Save
- `deptB`: GW **192.168.2.1**, DNS 192.168.1.2, start 192.168.2.10, mask 255.255.255.0 → Add

DNS: `www.college.com` → 192.168.1.2. HTTP: On.
PCs in both departments: set to DHCP. Verify: ping the other department, then open `www.college.com` in the Web Browser from both departments.

*(Alternative: configure DHCP on the router instead of `ip helper-address`):*
```
ip dhcp pool A
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 192.168.1.2
ip dhcp pool B
 network 192.168.2.0 255.255.255.0
 default-router 192.168.2.1
 dns-server 192.168.1.2
ip dhcp excluded-address 192.168.1.1 192.168.1.9
```

---

## Q13. University: DHCP + DNS + Web + Email

Combine Q10 and Q11 on one network (one server can run everything, or use 2 servers):
- Server 192.168.1.2: DHCP (DNS = 192.168.1.2), DNS records `www.university.com` and `mail.university.com` → 192.168.1.2, HTTP On, EMAIL with domain `university.com` and users `student` and `faculty`.
- PCs use DHCP. Verify the website in the Web Browser and send mail from `student@university.com` to `faculty@university.com`.

---

## Q14. Troubleshooting: DHCP works but the domain name doesn't

Symptom: PC gets an IP, `ping 192.168.1.2` works, but `www.college.com` fails ("Host Name Unresolved" / Request Timeout).

Check in this order (examiner usually breaks one of these):
1. **PC → IP Configuration → DNS Server**: is it blank, 0.0.0.0 or wrong? → the cause is the **DHCP pool's DNS Server field**. Fix: set it to 192.168.1.2 → **Save**, then switch the PC to Static and back to DHCP to renew.
2. **Server → Services → DNS**: is the service **Off**? → turn it On.
3. **DNS record**: is the name misspelled or the IP wrong (e.g. pointing to .3)? → fix the A record.
4. **HTTP** service is Off → turn it on (the IP in the browser fails too in this case).
5. Server has no static IP / wrong mask → re-set it.

Verify the fix: `nslookup www.college.com` in Command Prompt should return 192.168.1.2. The browser should then load the page.

**Explanation for the viva:** DHCP gives the PC its IP, gateway *and DNS server address*. If the DNS server address or DNS record is wrong, IPs still work but names can't be translated to IPs.
