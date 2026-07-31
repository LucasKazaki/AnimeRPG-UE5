#include "AnimeRPGGameMode.h"
#include "AnimeRPGCharacter.h"

AAnimeRPGGameMode::AAnimeRPGGameMode()
{
    DefaultPawnClass = AAnimeRPGCharacter::StaticClass();
}
