using UnrealBuildTool;
using System.Collections.Generic;

public class AnimeRPGProjectTarget : TargetRules
{
    public AnimeRPGProjectTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("AnimeRPGProject");
    }
}
