from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, security, database
from ..dependencies import verify_admin

router = APIRouter(
    prefix="/admin",
    tags=["Administrator Only"]
)

@router.post("/create-arcade", status_code=status.HTTP_201_CREATED)
def create_arcade(
    name: str, 
    location: str, 
    db: Session = Depends(database.get_db), 
    _ = Depends(verify_admin)
):
    # Generate a simple ID or use a UUID
    arcade_id = f"ARC_{name[:3].upper()}_{location[:2].upper()}"
    new_arcade = models.Arcade(id=arcade_id, name=name, location=location)
    db.add(new_arcade)
    db.commit()
    db.refresh(new_arcade)
    return {"message": "Arcade created", "arcade": new_arcade}

@router.post("/create-manager", status_code=status.HTTP_201_CREATED)
def create_manager(
    username: str, 
    password: str, 
    arcade_id: str, 
    db: Session = Depends(database.get_db), 
    _ = Depends(verify_admin)
):
    # Check if arcade exists
    arcade = db.query(models.Arcade).filter(models.Arcade.id == arcade_id).first()
    if not arcade:
        raise HTTPException(status_code=404, detail="Arcade ID not found")

    # Hash the password for security
    hashed_pwd = security.get_password_hash(password)
    new_user = models.User(
        username=username, 
        hashed_password=hashed_pwd, 
        role="manager", 
        arcade_id=arcade_id
    )
    db.add(new_user)
    db.commit()
    return {"message": f"Manager {username} created for arcade {arcade_id}"}