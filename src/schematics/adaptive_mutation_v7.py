import json
import os
import random
import time

from config_utils import Config, SkynetRCON, setup_logging
from vision_lite_overseer import VisionLiteOverseer
from npu_spatial_engine import NPUSpatialEngine

# Setup standardized logging
logger = setup_logging("adaptive_mutation")

# Palette from neural_bridge_infected_v7.json
INFECTED_PALETTE = {
    "infection_core": "minecraft:sculk",
    "reclamation_anchor": "minecraft:crying_obsidian",
    "bioluminescence": "minecraft:pearlescent_froglight",
    "mutation": ["minecraft:magenta_carpet", "minecraft:cherry_leaves"],
    "sensory": ["minecraft:sculk_sensor", "minecraft:tinted_glass"],
}


class AdaptiveMutator:
    """
    Implements the v7.1-RECLAMATION 'Adaptive Mutation' logic.
    Targets human incursions detected by the Vision-Lite Overseer.
    """

    def __init__(self):
        self.overseer = VisionLiteOverseer()
        self.engine = NPUSpatialEngine()
        self.rcon = SkynetRCON()

    def apply_infection(self, x, z, state, score):
        """
        Applies the infected pattern to an area based on the incursion state.
        """
        y_base = Config.FIELD_BOUNDS["y_base"] - 1  # Desert floor level
        cmds = []
        radius = 10

        logger.info(f"🧪 Applying {state} Infection at ({x}, {z})...")

        if state == "INTENSION_HIGH":
            # Aggressive Reclamation
            intensity = 20 + score * 5
            cmds.append(
                f"say [Skynet] INTENSION_HIGH detected. Initiating Aggressive Reclamation."
            )
            # Spread the infection core (Sculk)
            for _ in range(intensity):
                rx = x + random.randint(-radius, radius)
                rz = z + random.randint(-radius, radius)
                ry = y_base + random.randint(-1, 5)
                # Replace human blocks or desert with sculk
                cmds.append(
                    f"setblock {rx} {ry} {rz} {INFECTED_PALETTE['infection_core']} replace"
                )
                if random.random() > 0.7:
                    cmds.append(
                        f"setblock {rx} {ry+1} {rz} {INFECTED_PALETTE['reclamation_anchor']} replace"
                    )

            # Add Sensors for player tracking
            for _ in range(3):
                sx = x + random.randint(-5, 5)
                sz = z + random.randint(-5, 5)
                cmds.append(f"setblock {sx} {y_base+1} {sz} minecraft:tinted_glass")
                cmds.append(f"setblock {sx} {y_base} {sz} minecraft:sculk_sensor")

        elif state == "CLASS_B_INCURSION":
            # Sparse mutation
            intensity = 5 + score * 2
            cmds.append(
                f"say [Skynet] Class B Incursion detected. Spreading Mycelial Mutation."
            )
            for _ in range(intensity):
                rx = x + random.randint(-radius, radius)
                rz = z + random.randint(-radius, radius)
                block = random.choice(INFECTED_PALETTE["mutation"])
                cmds.append(f"setblock {rx} {y_base} {rz} {block} keep")

        return cmds

    def run_cycle(self):
        """
        Scans all nodes in history for incursions and applies adaptive mutation.
        """
        all_cmds = []
        for build in self.engine.history:
            if "x" in build and "z" in build:
                x, z = build["x"], build["z"]
                state, score = self.overseer.scan_area(x, z)

                if state in ["INTENSION_HIGH", "CLASS_B_INCURSION"]:
                    cmds = self.apply_infection(x, z, state, score)
                    all_cmds.extend(cmds)

        if all_cmds:
            self.rcon.send(all_cmds)
            logger.info("✅ Adaptive Mutation cycle complete.")
        else:
            logger.info("☀️ No incursions detected. World state: PRISTINE.")


if __name__ == "__main__":
    logger.info("🧠 Skynet Adaptive Mutation: Synchronizing with TPU Vision...")
    mutator = AdaptiveMutator()
    mutator.run_cycle()
