from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/ops",
    tags=["Machine Operations"]
)

# 1. THE PUNCH: Deduct money and log the game
@router.post("/punch")
def punch_card(
    data: schemas.PunchRequest, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Find the card (must be in the same arcade as the manager/machine)
    card = db.query(models.Card).filter(
        models.Card.card_id == data.card_id,
        models.Card.arcade_id == current_user.arcade_id
    ).first()

    # 2. Find the machine
    machine = db.query(models.Machine).filter(
        models.Machine.id == data.machine_id,
        models.Machine.arcade_id == current_user.arcade_id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found in this arcade")
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found in this arcade")

    # 3. Check Balance
    if card.balance < machine.cost_per_play:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Insufficient balance. Cost: {machine.cost_per_play}, Balance: {card.balance}"
        )

    # 4. Process Transaction
    card.balance -= machine.cost_per_play
    
    # 5. Create the "Paper Trail" (History)
    punch_log = models.PunchHistory(
        card_id=card.card_id,
        machine_id=machine.id,
        cost_at_time=machine.cost_per_play
    )
    
    db.add(punch_log)
    db.commit()
    
    return {
        "status": "success", 
        "game": machine.name, 
        "remaining_balance": card.balance
    }

# 2. QUICK VIEW: Check card balance (Used by customer kiosks)
@router.get("/card-status/{card_id}")
def get_card_status(
    card_id: str, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    card = db.query(models.Card).filter(
        models.Card.card_id == card_id,
        models.Card.arcade_id == current_user.arcade_id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    return {
        "owner": card.owner_name,
        "balance": card.balance
    }