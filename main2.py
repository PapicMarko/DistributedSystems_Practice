from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


#definiranje HTTP rute s odgovorom
@app.get("/info_2") #python dekoratori
def krumpir():
    print("unutar funkcije")

    return{
        "status": "ok",
        "lista": [1, 2, 3, {"ok": "not"}]
           }
