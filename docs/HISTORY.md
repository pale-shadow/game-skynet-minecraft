# Bitsmasher Minecraft Network

📜 Overview
Server Domain: minecraft.bitsmasher.net

Established: 2012

Operating Environment: Paper 1.21.11 on Java 21 (Debian Bookworm)

Primary Map: "dreamland (overworld)" using SQL storage

📅 Chronological Eras
🏗️ The Foundations (2012 – 2020)
Inception: Launched as a private project utilizing early Paper and CraftBukkit builds.

Geological Landmarks: World-building focused on the original release of major biomes, including the first Mushroom and Jungle biome updates.

Legacy World: The core map files (world, world_nether, world_the_end) have been continuously maintained for over a decade.

⚙️ The Technical Modded Era (2021 – 2024)
Forge Transition: Shifted to a heavy industrial modded environment, specifically utilizing the Thermal Series on Minecraft 1.15.2.

Automation Adoption: Began managing infrastructure via Ansible and Nix configurations to handle modpack complexity.

Distribution: Established a public presence on the Technic Platform (Modpack ID: 1928704) with direct Dropbox sourcing for reliability.

🚀 The Modern Expansion (2025 – Present)
Infrastructure Reboot: Finalized a streamlined directory structure on the Chonk server in early 2025.

Modern Paper Migration: Formally transitioned back to Paper for the 1.21.11 launch to prioritize performance and public 3D rendering via BlueMap.

Expansion: Recorded significant northern growth with the founding of Knobbler's Gulch in March 2026.

🗺️ World Heritage & Landmarks
Central Spawn & Transit
Railway Hub: The original spawn features a central Railway Station and primary administrative buildings.

Navigation: Utilize armor-stand "Markers" (Invisible, NoGravity) for in-game floating text waypoints.

The Main Line: A functional rail network connects the Spawn Hub to Shroomville and Jungle Hutt.

Shroomville (X: 1752, Z: 702)
Historical Status: One of the server's oldest settlements, built when mushroom biomes were first introduced.

Key Architecture: Home base of theDevilsVoice (UnvaluedShoe79); features a hand-built Cathedral, Castle, and a large wooden ship.

Amenities: Enclosed by large castle walls, the site includes a farm, stable, gardens, and a dedicated aviary.

Jungle Hutt (X: -47, Z: -1541)
Origin: An original village established during the first jungle biome update.

2026 Modernization: The historic railway station is undergoing technical upgrades to integrate with modern 1.21.11 mechanics while preserving its legacy architecture.

Knobbler's Gulch (X: -761, Z: -2072)
Status: A primary settlement expansion founded in early 2026.

Maintenance Note: Identified as a high-activity zone near a documented NBT entity corruption point in region r.-2.-5.mca.

🛠️ Management & Security
Administrative Stack
The Janitors: Core administrative team consisting of UnvaluedShoe79 (Owner), some_garlic, and slyborg4realz.

RCON Interaction: Utilizes a custom pipe-based rcon.sh script for secure, local console interaction via doas -u _minecraft.

Audit Logic: All administrative actions and block changes are logged via CoreProtect and Vault using MySQL/MariaDB backends.

Permission Hierarchy
Rank System: Migrated from FTB Ranks' "Power" logic to LuckPerms weight-based inheritance.

Tiers: Players progress through a five-tier system: Hobo → Ninja → Hacker → Sheriff → Janitor.

Security: Default ranks (Hobo) are restricted via EssentialsX AntiBuild to prevent unauthorized interaction with legacy redstone and buildings.
