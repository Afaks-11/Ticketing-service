from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
import os 

from .database import SessionLocal

JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = 'HS256'

def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
        
def get_current_user(req: Request): 
    auth_header = req.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing Authorization Header or invalid token')
    
    token = auth_header.split(' ')[1]
    
    try: 
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub') or payload.get('id')
        if user_id is None:
            raise HTTPException(status_code=401, detail='Token missing user information')
        
        return {'id': user_id, 'role': payload.get('role')}
    except JWTError: 
        raise HTTPException(status_code=401, detail='Could not validate credentials')
