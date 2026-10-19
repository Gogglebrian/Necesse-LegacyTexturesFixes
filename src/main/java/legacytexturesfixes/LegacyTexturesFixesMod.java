package legacytexturesfixes;
import necesse.engine.modLoader.annotations.ModEntry;
import necesse.gfx.gameTexture.GameTexture;

@ModEntry
public class LegacyTexturesFixesMod {
    public static GameTexture ostrichmountmask;

    public void init() {
    }

    public void initResources() {
        ostrichmountmask = GameTexture.fromFile("mobs/ostrichmountmask");
    }
}
