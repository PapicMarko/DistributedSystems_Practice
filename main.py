import fastapi
import requests
import time
import httpx

from multiprocessing import ThreadPool

app = fastapi.FastAPI()

def pozovi_fib(x):
    t1 = time.time()
    response = requests.get(f"http://localhost:8001/fib/{x}")
    rezultat = response.json()["result"]
    t2 = time.time()
    trajanje = (t2 - t1) * 1000.0

    print(f"Pozivanje fib({x}) je trajalo {trajanje:.2f} ms")

    return rezultat

@app.get("/zbroj_fib/{n}")
async def zbroj_fib(n: int):
    rezultat = pozovi_fib(n)
    return {"input": n, "result": rezultat}

    with ThreadPool(processes = 100) as pool:
        rezultat = pool.map(pozovi_fib, [0, 1, 2, 3])

        print(rezultat)

    rezultat = 0
    for x in range(n):
        rezultat += pozovi_fib(x)

    return {"input": n, "result": rezultat}