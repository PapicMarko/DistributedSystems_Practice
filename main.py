from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


#definiranje HTTP rute s odgovorom
@app.get("/info") #python dekoratori
def krumpir():
    print("unutar funkcije")

    return{
        "status": "ok",
        "lista": [1, 2, 3, {"ok": "not"}]
           }

@app.get("/rasp")
def banana2():
    ...
#moram pozvati onaj drugi server