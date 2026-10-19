package legacytexturesfixes;

import necesse.engine.modLoader.annotations.ModMethodPatch;
import necesse.entity.mobs.summon.summonFollowingMob.mountFollowingMob.TameOstrichMob;
import net.bytebuddy.asm.Advice;

@ModMethodPatch(target = TameOstrichMob.class, name = "getRiderDrawYOffset", arguments = {})
public class TameOstrichMobGetRiderDrawYOffsetPatch {
    @Advice.OnMethodEnter(skipOn = Advice.OnNonDefaultValue.class)
    static boolean onEnter() {
        // Always skip the original method body
        return true;
    }

    @Advice.OnMethodExit
    static void onExit(@Advice.This TameOstrichMob ostrich,
                       @Advice.Return(readOnly = false) int returned) {
        returned = ostrich.getSwimMaskShaderOptions(ostrich.inLiquidFloat(ostrich.getDrawX(), ostrich.getDrawY())).drawYOffset - 30;
    }
}
