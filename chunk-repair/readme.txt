how can I fix this error in all chunks in the server: [09:54:49 ERROR]: Recoverable errors when loading section [-119, -1, -70]: (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: thermal:deepslate_lead_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: thermal:deepslate_nickel_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: thermal:deepslate_tin_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: thermal:deepslate_silver_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: mysticalagriculture:deepslate_prosperity_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: mysticalagriculture:deepslate_inferium_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: occultism:silver_ore_deepslate -> using default)
[09:54:49 ERROR]: Recoverable errors when loading section [-120, -2, -70]: (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: mysticalagriculture:deepslate_inferium_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: mysticalagriculture:deepslate_prosperity_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: occultism:silver_ore_deepslate -> using default)
[09:54:49 ERROR]: Recoverable errors when loading section [-120, -1, -70]: (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: thermal:deepslate_tin_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: mysticalagriculture:deepslate_inferium_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: thermal:deepslate_silver_ore -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: occultism:silver_ore_deepslate -> using default); (Unknown registry key in ResourceKey[minecraft:root / minecraft:block]: mysticalagriculture:deepslate_prosperity_ore -> using default)

This error is a direct consequence of your server's transition from the **"Technical Modded Era" (2021–2024)** to the current **"Modern Era" (Paper 1.21.11)**. 

The world files currently being used were established in 2012 and maintained throughout the Forge era, during which you ran mods like the **Thermal Series**, **Mystical Agriculture**, and **Occultism**. Because the server is now running **Paper**, which is a plugin-based software that does not support client-side mods or their custom block registries, it cannot recognize blocks like `thermal:deepslate_lead_ore` or `occultism:silver_ore_deepslate`.

The server is flagging these as "Recoverable errors" because it is automatically replacing these unrecognized modded blocks with "default" blocks (typically air or stone) to prevent the world from failing to load [Error Log].

To fix this error across all chunks, you can use the following methods based on the tools already present in your environment:

### **1. Automated Recovery via Pre-generation**
Since the server "fixes" these blocks as it loads them, you can force the server to process every chunk.
*   **Method:** Use the **Chunky** plugin (which is recommended in the sources for world management and performance). 
*   **Action:** Run a full world pre-generation (e.g., `/chunky start`). As Chunky forces the server to load every section, the server will encounter the modded blocks, replace them with defaults, and save the corrected data to the disk. Once this process is complete, the errors will no longer appear when players explore those areas.

### **2. Manual Data Cleaning with mcaselector**
Your server directory already contains **.mcaselector**, which is the industry-standard tool for this exact issue.
*   **Method:** Open your world in **mcaselector**.
*   **Action:** You can use the "Filter" function to search for specific NBT data or block IDs containing "thermal", "mysticalagriculture", or "occultism". You can then either delete those specific blocks or prune the affected chunks entirely if they are in uninhabited areas. This is the "cleanest" way to strip modded data from a vanilla/Paper world.

### **3. Admin Pruning for Urbanization**
As you focus on the **urbanization of Shroomville** and the **Deep-Rail project**, you may encounter these errors in high-density areas.
*   **Action:** If these errors are occurring in areas slated for new AI-driven builds (like the **Silicon Ridge** or **Vertical Sump**), you can use **WorldEdit** (which you use for your programmatic builds) to select the area and run a `//replace` command to overwrite any "ghost" blocks. 

**Important Note:** Before performing a mass cleanup or pre-generation, ensure your **`bin/backup_to_git.sh`** script has recently pushed a stable version of your world folders to GitHub to prevent accidental data loss during the recovery process.
