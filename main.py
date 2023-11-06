import fastapi
import requests
import time
import asyncio
import httpx
import concurrent.futures
import random


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


"""#WORKER 1
app = fastapi.FastAPI()
worker_service_url = "http://127.0.0.1:8003"
@app.get("/fibonacci/{n}")
async def calculate_fibonacci(n: int):
    # Pošaljite zahtjev za izračunom Fibonacci broja radniku.
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{worker_service_url}/fib/{n}")
        result = response.json()

    return {"input": n, "result": result["result"]}



app = fastapi.FastAPI()

def calculate_fibonacci_worker(port, n):
    url = f"http://localhost:{port}/fib/{n}"
    with httpx.Client() as client:
        response = client.get(url)
        result = response.json()["result"]
    return result

@app.get("/fibonacci_multiport/{n}")
async def calculate_fibonacci_multiport(n: int):
    ports = [8003, 8004, 8005, 8006]  # Portovi za različite workere

    # Kreirajte bazen radnika s 4 radnika.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Izračunajte Fibonacci brojeve za n koristeći različite portove.
        results = list(executor.map(calculate_fibonacci_worker, ports, [n] * len(ports)))

    return {"input": n, "results": results}
"""



app = fastapi.FastAPI()

# Konfigurirajte portove za svakog workera
worker_ports = [8003, 8004, 8005, 8006]

def calculate_fibonacci_worker(n):
    # Odaberite slučajni port iz liste
    port = random.choice(worker_ports)
    url = f"http://localhost:{port}/fib/{n}"
    with httpx.Client() as client:
        response = client.get(url)
        result = response.json()["result"]
    return {"input": n, "result": result, "used_port": port}

@app.get("/fibonacci_randomport/{n}")
async def calculate_fibonacci_randomport(n: int):
    result = calculate_fibonacci_worker(n)
    return result