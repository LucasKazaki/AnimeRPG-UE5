
# AnimeRPGProject.Build.cs
using UnrealBuildTool;

public class AnimeRPGProject : ModuleRules
{
	public AnimeRPGProject(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.Prepackaged;
		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore" });

		// Add modules for specialized gameplay features
		PrivateDependencyModuleNames.AddRange(new string[] { "EnhancedInput", "GameplayAbilities" }); 
	}
}
