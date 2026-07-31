// AnimeRPGGameMode.cpp
#include "AnimeRPGProjectGameMode.h"
#include "AnimeRPGProjectPlayerController.h"

AAnimeRPGProjectGameMode* AAnimeRPGProjectGameMode::GetDefaultObject<AAnimeRPGProjectGameMode>() const
{
    return Cast<AAnimeRPGProjectGameMode>(UGameplayStatics::GetGameModeForCurrentMap());
}

void AAnimeRPGProjectGameMode::BeginPlay()
{
    Super::BeginPlay();
    // Setup: Spawn initial character, set up world rules for the vertical slice.
}