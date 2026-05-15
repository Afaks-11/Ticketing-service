from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.core.config import settings

app = FastAPI(title='Payment Service')

app.middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']
)

app.include_router(checkout.router, prefix='/payments', tags=['Checkout'])
app.include_router(webhooks.router, prefix='/payments', tags=['Webhooks'])

@app.get('/health')
def health_check():
    return({ 'status': 200, 'message': 'Payment Service is activate'})

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
if __name__ == '__main__':
    import uvicorn
    port = int(settings.PORT)
    uvicorn.run('app.main:app', host='localhost', port=port, reload=True)