using UnrealBuildTool;
using System.Collections.Generic;

public class AnimeRPGProjectEditorTarget : TargetRules
{
    public AnimeRPGProjectEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("AnimeRPGProject");
    }
}
