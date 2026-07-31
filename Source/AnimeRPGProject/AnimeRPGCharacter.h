#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "AnimeRPGCharacter.generated.h"

class UCameraComponent;
class USpringArmComponent;

UCLASS()
class ANIMERPGPROJECT_API AAnimeRPGCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AAnimeRPGCharacter();

    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
    TObjectPtr<UCameraComponent> FollowCamera;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Movement", meta = (ClampMin = "0.0"))
    float DashStrength = 1200.0f;

private:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void Dash();
};
