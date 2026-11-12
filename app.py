def greet(name:str)->str:
    return f"Hello {name}, running inside docker via Jenkins on WSL2 !"


if __name__ == "__main__":
    print(greet("Lucky"))

