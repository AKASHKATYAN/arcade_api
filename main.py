from fastapi import FastAPI,HTTPException
import uvicorn as uv
from utils import load_data,write_data
import pandas as pd
from schema.data_validation import Cards,ViewCardsDetails,Recharge,Refund

#Initializing FastAPI
app=FastAPI()

#Home page
@app.get("/")
def home_page():
   return {'message':'Welcome to RFID API'}

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


#Creating new card
@app.post("/create")
def create(card: Cards):
    cards = load_data()

    # Check for duplicate card_id
    for c in cards:
        if c["card_id"] == card.card_id:
            raise HTTPException(
                status_code=400,
                detail="Card with this card_id already exists"
            )

    # Add new card
    cards.append(card.model_dump())
    write_data(cards)

    return {
        "message": "Card created successfully",
        "card": card
    }
@app.post("/punch")
def punch_card(card_id: str)->dict:
  cards=load_data()
  for c in cards:
    if c["card_id"] == card_id:
        return {"message": "Card accepted"}

  return {"error": "Invalid card"}


#Viwing a existing card    
@app.get("/view_cards/{card_id}")
def view_card(card_id: str)->dict:
  #checking for existing card
   cards = load_data()
   for c in cards:
        if c["card_id"] == card_id:
            return c
   raise HTTPException(status_code=400,detail='Given card does not exists')
  
#RECHARGE THE CARD    
@app.put("/recharge/")
def recharge_card(data:Recharge):
    #checking for existing card
   cards = load_data()
   if data.amount<0:
       raise HTTPException(status_code=400,detail='Amount cannot be negative')
   for c in cards:
        if c["card_id"] == data.card_id:
            c["balance"] +=data.amount
            write_data(cards)
            return c
   raise HTTPException(status_code=400,detail='Given card does not exists.')
  
#REFUND THE AMOUNT
@app.put("/refund")
def refund(data:Refund):
    cards=load_data()
    for c in cards:
        if c['card_id']==data.card_id:
            c["balance"]=0
            write_data(cards)
            return c
    raise HTTPException(status_code=400,detail='Given card does not exist.')

