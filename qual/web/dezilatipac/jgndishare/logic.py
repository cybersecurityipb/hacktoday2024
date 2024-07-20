import os

def replacer(x):
    return x.replace(x[0], x[0].upper())

def commander(y):
    return os.system(y)

if __name__ == "__main__":
    while True:
        y = replacer(input(">"))
        x = commander(y)
        print(x)