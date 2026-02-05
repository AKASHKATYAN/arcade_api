from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Arcade(Base):
    __tablename__ = "arcades"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)

    users = relationship("User", back_populates="arcade")
    machines = relationship("Machine", back_populates="arcade")
    cards = relationship("Card", back_populates="arcade")

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="manager") # 'administrator' or 'manager'
    arcade_id = Column(String, ForeignKey("arcades.id"), nullable=True)
    
    arcade = relationship("Arcade", back_populates="users")

class Machine(Base):
    __tablename__ = "machines"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cost_per_play = Column(Float, default=1.0)
    arcade_id = Column(String, ForeignKey("arcades.id"))
    
    arcade = relationship("Arcade", back_populates="machines")

class Card(Base):
    __tablename__ = "cards"
    card_id = Column(String, primary_key=True, index=True)
    owner_name = Column(String)
    contact_no = Column(String(10))
    balance = Column(Float, default=0.0)
    arcade_id = Column(String, ForeignKey("arcades.id"))
    
    arcade = relationship("Arcade", back_populates="cards")

class RechargeHistory(Base):
    __tablename__ = "recharge_history"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String, ForeignKey("cards.card_id"))
    amount = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class PunchHistory(Base):
    __tablename__ = "punch_history"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String, ForeignKey("cards.card_id"))
    machine_id = Column(String, ForeignKey("machines.id"))
    cost_at_time = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())