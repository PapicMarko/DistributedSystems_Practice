import fastapi
import requests
import time
import asyncio
import httpx

from multiprocessing.pool import ThreadPool

app = fastapi.FastAPI()


def pozovi_fib(x):
    t1 = time.time()
    response = requests.get(f"http://localhost:8000/fib/{x}")
    rezultat = response.json()
    # rezultat = {
    #   "input": 10,
    #   "result": 55
    # }
    print("JSON", rezultat)

    pravi_rezulatat = rezultat["result"]
    t2 = time.time()

    trajanje = (t2 - t1) * 1000.0
    print(f"Pozivanje fib({x}) je trajalo {trajanje:.2f}ms")

    return pravi_rezulatat


async def get_fib(x):
    async with httpx.AsyncClient() as client:
        url = f"http://127.0.0.1:8000/fib/{x}"
        response = await client.get(url)
        rezultat = response.json()["result"]
        print(f"Rezultat za {x} je {rezultat}")
        return rezultat


@app.get("/zbroj_fib/{n}")
async def zbroj_fib(n: int):
    # pozivati drugi servis da bi izračunala sumu prvih
    # N fib brojeva

    # npr. primi 3 kao argument
    # mora vratiti fib(1) + fib(2) + fib(3)
    # primi 10 kao argument
    # mora vratiti fib(1) + fib(2) + ... + fib(10)
    # prevedeno        1  +     2  + ... +     55

    parametri = [get_fib(x) for x in range(n + 1)]

    #    * - spreading operator
    rezultat = await asyncio.gather(*parametri)

    # rezultat = 0
    # for x in range(n + 1):
    #     rezultat += await get_fib(x)

    return {"input": n, "result": sum(rezultat)}


# Pitanje: koliko traje izvođenje za N=100?