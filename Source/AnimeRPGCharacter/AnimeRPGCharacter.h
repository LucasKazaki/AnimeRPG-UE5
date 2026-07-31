// AnimeRPGCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "AnimeRPGCharacter.generated.h"

UCLASS()
class ANIMERPGPROJECT_API AAnimeRPGCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AAnimeRPGCharacter();

protected:
    virtual void BeginPlay() override;

private:
    // Movement/Camera Logic (Dash, Basic Movement)
    void HandleMovementInput(float Value);
    UFUNCTION()
    void OnLookUp(const FInputActionValue& Value); 

public:
    // Combat Actions
    UFUNCTION(BlueprintCallable)
    void LightAttack(); // Placeholder for melee combo logic

    UFUNCTION(BlueprintCallable)
    void HeavyAttack(); // Placeholder for charged attack logic

    UFUNCTION(BlueprintCallable)
    void PerformDash(); // Implementation of dash mechanic
};
