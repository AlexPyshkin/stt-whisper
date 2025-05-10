from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello_world():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9099, reload=True)
