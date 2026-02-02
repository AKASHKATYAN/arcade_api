from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/manager",
    tags=["Manager Operations"]
)

@router.post("/create-card", response_model=schemas.CardResponse)
def create_card(
    card_data: schemas.CardCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Security: Ensure only a manager/admin can do this
    if current_user.role not in ["manager", "administrator"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Create card and link it to the manager's arcade automatically
    new_card = models.Card(
        **card_data.model_dump(),
        arcade_id=current_user.arcade_id,
        balance=0.0
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@router.put("/recharge")
def recharge_card(
    data: schemas.RechargeRequest, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Find card only within the manager's arcade
    card = db.query(models.Card).filter(
        models.Card.card_id == data.card_id, 
        models.Card.arcade_id == current_user.arcade_id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found in your arcade")

    card.balance += data.amount
    
    # Log the history
    log = models.RechargeHistory(card_id=card.card_id, amount=data.amount)
    db.add(log)
    
    db.commit()
    return {"message": "Recharge successful", "new_balance": card.balance}

@router.put("/refund")
def refund_card(
    data: schemas.RefundRequest, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # 1. Find the card and ensure it belongs to this Manager's arcade
    card = db.query(models.Card).filter(
        models.Card.card_id == data.card_id,
        models.Card.arcade_id == current_user.arcade_id
    ).first()

    if not card:
        raise HTTPException(
            status_code=404, 
            detail="Card not found or does not belong to your arcade"
        )

    refund_amount = card.balance
    
    # 2. Reset balance
    card.balance = 0.0

    # 3. Log the transaction as a negative recharge or a specific refund log
    # We will use the RechargeHistory table but with a negative value to represent money leaving
    refund_log = models.RechargeHistory(
        card_id=card.card_id, 
        amount=-refund_amount  # Negative amount indicates money back to customer
    )
    
    db.add(refund_log)
    db.commit()

    return {
        "message": "Refund processed successfully",
        "card_id": card.card_id,
        "refunded_amount": refund_amount,
        "new_balance": 0.0
    }