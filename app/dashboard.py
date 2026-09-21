from fastapi import FastAPI

app = FastAPI(
    title="IZgoN AI"
)

@app.get("/")
def home():

    return {
        "name":"IZgoN AI",
        "status":"running"
    }

@app.get("/health")
def health():

    return {
        "ok":True
    }
