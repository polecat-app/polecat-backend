from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.database import get_db
from app.deps import get_current_user_from_access_token
from app.models import User, UserSave, Animal

# Router
router = APIRouter(
    prefix="/save", tags=["save"], responses={status.HTTP_401_UNAUTHORIZED: {"user": "Not authorized"}}
)


@router.get("/")
async def get_saved_animals(
    payload: schemas.Save,
    user: User = Depends(get_current_user_from_access_token),
    database: Session = Depends(get_db),
):
    """Get all saved animals for a user."""
    animal_ids = [user_save.animal_id for user_save in user.user_saves if user_save.method == payload.method]
    animals = database.query(Animal).filter(Animal.id.in_(animal_ids)).all()
    if not animals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No saved animals with method {payload.method}")
    return animals


@router.post("/")
async def save_animal(
    payload: schemas.SaveAnimal,
    user: User = Depends(get_current_user_from_access_token),
    database: Session = Depends(get_db),
):
    """Save an animal."""

    # Check if animal exists, else raise conflict error
    animal = database.query(Animal).filter(Animal.id == payload.animal_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Animal does not exist"
        )

    # Check if animal is not liked, else raise conflict error
    user_save = (
        database.query(UserSave)
        .filter(UserSave.owner_id == user.id)
        .filter(UserSave.method == payload.method)
        .filter(UserSave.animal_id == payload.animal_id)
        .first()
    )
    if user_save:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Animal already liked"
        )

    user_save = UserSave(method=payload.method)
    user.user_saves.append(user_save)
    animal.user_saves.append(user_save)
    database.add(user_save)
    database.commit()
    return {"animal_id": payload.animal_id, "method": payload.method}


@router.delete("/")
async def delete_saved_animal(
    payload: schemas.SaveAnimal,
    user: User = Depends(get_current_user_from_access_token),
    database: Session = Depends(get_db),
):
    """Delete saved animal."""

    # Get saved animal
    user_save = (
        database.query(UserSave)
        .filter(UserSave.owner_id == user.id)
        .filter(UserSave.method == payload.method)
        .filter(UserSave.animal_id == payload.animal_id)
        .first()
    )

    # Delete saved animal or raise exception
    if user_save:
        database.delete(user_save)
        database.commit()
        return f"Deleted saved animal with method {payload.method} and id {payload.animal_id}"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal with id {payload.animal_id} is not saved"
    )
