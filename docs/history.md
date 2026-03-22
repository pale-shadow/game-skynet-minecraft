Here is a comprehensive **HISTORY.md** file for your repository. It synthesizes your server logs, the 2012 legacy details, and the technical milestones found in your archives and notes.

---

# HISTORY.md - Bitsmasher Minecraft Network

## 📜 Overview

**Server Address:** `minecraft.bitsmasher.net`

**Founded:** 2012

**Current Era:** Modern Paper (1.21.11)

This document tracks the evolution of the Bitsmasher server from a 2012 private project to its current state as a high-performance, DevOps-managed Minecraft environment.

---

## 📅 Timeline

### 🏗️ The Foundations (2012 – 2020)

* **2012:** Server founded. Originally running early versions of **Paper** and **CraftBukkit**.
* **2012-2020:** Continuous world-building and community growth. The world files (`world`, `world_nether`, `world_the_end`) established during this era remain the core of the current map.

### ⚙️ The Technical Modded Era (2021 – 2024)

The server transitioned to a heavy **Forge** environment, focusing on industrial automation and technical complexity.

* **April 2021:** Early infrastructure management begins using **Ansible** and **Nix** configuration.
* **August 2021:** Implementation of the **Thermal Series** (Expansion/Foundation) on Minecraft 1.15.2.
* **2022:** Migration through Minecraft versions 1.16.5, 1.17.1, and 1.18.2.
* **July 2022:** Major backup milestone (`bitsmasher.zip`) created to preserve the modded legacy before version jumps.
* **March 2024:** Testing of **Fabric** and **Minescript** integrations for automated world-building.

### 🚀 The "Modern Era" (2025 – Present)

A strategic shift back to **Paper** for peak performance and public accessibility.

* **Feb 10, 2025:** Finalized the new directory structure (`~/bin`, `~/archive`, `~/workspace`) on the **Chonk** server.
* **March 13, 2025:** Final Forge test (1.20.1) before full migration to Paper 1.21.
* **March 15, 2026:** Official launch on **minecraft.bitsmasher.net**.
* Transitioned from FTB Ranks to a weight-based **LuckPerms** system.
* Deployment of **BlueMap** (Port 8100) for real-time 3D web rendering.
* Deployment of **Plan** (Port 8804) for deep player analytics.

#### 🛤️ The Great Northern Expansion
- **Jungle Hutt Preservation:** Recognized as a foundation-era jungle settlement. The historic rail connection to Spawn has been officially designated as part of the "Bitsmasher Main Line."
- **2026 Modernization:** Commenced the technical overhaul of the Jungle Hutt Railway Station, integrating modern Paper 1.21.11 features into the legacy 2012 architecture.

---

## 🛠️ Technical Milestones

### Infrastructure Evolution
* **OS:** Migrated to **Debian 12 (Bookworm)**.
* **Java:** Upgraded from OpenJDK 17 (Forge Era) to **Java 21** (Modern Paper).
* **Automation:** Developed `start.sh` (v0.1 Sept 2023) and `backup_to_git.sh` (v0.1 Feb 2026) for automated snapshots.

### 🗺️ Infrastructure & Navigation
- **Public Transport:** The 2012 legacy world features a centralized **Train Station** accessible via specialized armor-stand navigation markers.
- **Modpack Hosting:** Established a presence on the **Technic Platform** (Modpack ID: 1928704) to allow players easy access to the Forge/modded eras of the server.

### Management Philosophy
* **Permission Logic:** Shifted from "Power" levels (FTB Ranks) to "Weights" (LuckPerms). Established the five-tier hierarchy: **Hobo → Ninja → Hacker → Sheriff → Janitor**.
* **Auditability:** Integrated **CoreProtect** and **Vault** to ensure all transactions and block changes are logged in the MySQL/MariaDB backends.
* **Public Access:** Enabled **Query (Port 25555)** and **RCON (Port 25575)** for external monitoring and management.

---

## 📂 Archive Reference

* **Legacy Modsets:** 1.15.2 (Thermal Expansion), 1.16.5 (Forge), 1.18.2 (Industrial).
* **Historical Notes:** Located in `~/docs/notes.txt`, detailing the transition from manual installs to Ansible playbooks.
