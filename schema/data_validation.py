from typing import Annotated,Optional
from pydantic import BaseModel,Field

#Validating Fields
class Cards(BaseModel):
    card_id:str=Field(...,min_length=10,max_length=10,description='Card_id of the card a 10 digit unique number')
    balance:float=Field(...,gt=0,le=10000,description='The amount credited to the card after recharge')
    name:str=Field(...,min_length=1,description='Name of the user')
    contact_no:str=Field(...,min_length=10,max_length=10,description='Contact number of the user')

class ViewCardsDetails(BaseModel):
    card_id:str=Field(...,min_length=10,max_length=10,description='Card_id of the card a 10 digit unique number')

class Recharge(BaseModel):
    card_id:str=Field(...,min_length=10,max_length=10,description='Card_id of the card a 10 digit unique number')
    amount:float=Field(...,gt=100,description='Amount credited to be credited to the card.') 
class Refund(BaseModel):
    card_id:str=Field(...,min_length=10,max_length=10,description='Card_id of the card a 10 digit unique number')
