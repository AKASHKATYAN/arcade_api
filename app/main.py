from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import our local modules
from . import models, security, database
from .database import engine, get_db
from .routers import admin, manager, operations

# Initialize the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure RFID Arcade Management System",
    description="A multi-tenant system for managing arcade branches, managers, and RFID cards.",
    version="2.0.0"
)

# --- INCLUDE ROUTERS ---
# This connects all the files you created in the 'routers' folder
app.include_router(admin.router)
app.include_router(manager.router)
app.include_router(operations.router)

# --- THE LOGIN ROUTE ---
@app.post("/token", tags=["Authentication"])
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    The entry point for Managers and Admins. 
    Verifies credentials and returns a JWT Access Token.
    """
    # 1. Look for the user in the database
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Check password security
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Create the token with user identity, role, and arcade_id
    access_token = security.create_access_token(
        data={
            "sub": user.username, 
            "role": user.role, 
            "arcade_id": user.arcade_id
        }
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

