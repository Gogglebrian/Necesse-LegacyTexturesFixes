package legacytexturesfixes;

import necesse.engine.modLoader.annotations.ModMethodPatch;
import necesse.entity.mobs.summon.summonFollowingMob.mountFollowingMob.TameOstrichMob;
import necesse.gfx.gameTexture.GameTexture;
import net.bytebuddy.asm.Advice;

@ModMethodPatch(target = TameOstrichMob.class, name = "getRiderMask", arguments = {})
public class TameOstrichMobGetRiderMaskPatch {
    @Advice.OnMethodEnter(skipOn = Advice.OnNonDefaultValue.class)
    static boolean onEnter() {
        // Always skip the original method body
        return true;
    }

    @Advice.OnMethodExit
    static void onExit(@Advice.Return(readOnly = false) GameTexture returned) {
        returned = LegacyTexturesFixesMod.ostrichmountmask;
    }
}
