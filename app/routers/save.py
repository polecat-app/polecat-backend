from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.database import get_db
from app.deps import get_current_user_from_access_token
from app.models import User, UserLike, Animal

# Router
router = APIRouter(
    prefix="/save", tags=["save"], responses={401: {"user": "Not authorized"}}
)


@router.get("/liked")
async def get_liked_animals(
    user: User = Depends(get_current_user_from_access_token),
    database: Session = Depends(get_db),
):
    """Get all liked animals for a user."""

    # Query database for liked animals with user id, or raise exception
    animal_ids = [user_like.animal_id for user_like in user.user_likes]
    animals = database.query(Animal).filter(Animal.id.in_(animal_ids)).all()
    if not animals:
        raise HTTPException(status_code=404, detail="No liked animals")
    return animals


@router.post("/liked")
async def like_animal(
    payload: schemas.LikeAnimal,
    user: User = Depends(get_current_user_from_access_token),
    database: Session = Depends(get_db),
):
    """Like an animal."""

    # Check if animal exists, else raise conflict error
    animal = database.query(Animal).filter(Animal.id == payload.animal_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Animal does not exist"
        )

    # Check if animal is not liked, else raise conflict error
    user_like = (
        database.query(UserLike)
        .filter(UserLike.owner_id == user.id)
        .filter(UserLike.animal_id == payload.animal_id)
        .first()
    )
    if user_like:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Animal already liked"
        )

    user_like = UserLike()
    user.user_likes.append(user_like)
    animal.user_likes.append(user_like)
    database.add(user_like)
    database.commit()
    return {"animal_id": payload.animal_id}


@router.delete("/liked")
async def delete_liked_animal(
    payload: schemas.LikeAnimal,
    user: User = Depends(get_current_user_from_access_token),
    database: Session = Depends(get_db),
):
    """Get all liked animals for a user."""
    print(user.user_likes)

    # Query database for to do with same id, or raise exception
    user_like = (
        database.query(UserLike)
        .filter(UserLike.owner_id == user.id)
        .filter(UserLike.animal_id == payload.animal_id)
        .first()
    )
    if user_like:
        # Add to do model to database, overwriting previous model with same id
        database.delete(user_like)
        database.commit()
        return f"deleted liked animal with id {payload.animal_id}"

    raise HTTPException(
        status_code=404, detail=f"Animal with id {payload.animal_id} is not liked"
    )
