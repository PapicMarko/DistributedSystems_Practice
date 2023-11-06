import fastapi

app = fastapi.FastAPI()


def fib_v2(n):
    if n <= 1:
        return n

    n2, n1 = 0, 1

    for _ in range(n - 1):
        n2, n1 = n1, n1 + n2

    return n1


def fib(n):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


assert fib(10) == 55, "seems wrong?"
assert fib_v2(10) == 55, "seems wrong?"


@app.get("/fib/{x}")  # python dekoratori
def fibonacci(x: int):
    return {"input": x, "result": fib_v2(x)}


# uvicorn main2:app --reload --port 8001