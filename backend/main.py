from fastapi import FastAPI

app = FastAPI(title="HeritageGraph API")


@app.get("/health")
def health():
    return {"status": "ok"}