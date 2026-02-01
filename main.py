from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "n7eb nesl alik cv wala lee w habitch eli ysir Ysir ,juste koli cv wala lee"}

