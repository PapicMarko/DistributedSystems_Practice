# worker.py
import fastapi

app = fastapi.FastAPI()

def fib(n):
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

@app.get("/fib/{n}")
def calculate_fibonacci(n: int):
    result = fib(n)
    return {"input": n, "result": result}
