package net.bitsmasher.testmod;

import org.apache.logging.log4j.Logger;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;

@Mod(modid = EchoCommandMod.MODID, name = EchoCommandMod.NAME, version = EchoCommandMod.VERSION)
public class EchoCommandMod {

      public static final String MODID = "testmod";
      public static final String NAME = "Echo Command Mod";
      public static final String VERSION = "0.0.1";

      public static Logger logger;

      @EventHandler
      public void preInit(FMLPreInitializationEvent event)
      {
          logger = event.getModLog();
      }

      @EventHandler
      public void init(FMLServerStartingEvent event)
      {
        logger.info("initalise FMLServerStartingEvent :" + NAME);
        event.registerServerCommand(new EchoCommand());
      }
}