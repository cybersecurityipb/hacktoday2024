import subprocess

def run(user_input):
    process = subprocess.Popen(['solver.exe'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    
    try:
        stdout, stderr = process.communicate(input=user_input, timeout=5)
        print('\nOUTPUT')
        print(f'> {stdout}')

        print('\nUnsuccessful Hacking Attempt')

    except subprocess.TimeoutExpired:
        print('\nSuccessful Hacking Attempt (time limit)')
        with open('flag.txt', 'r') as file:
            flag = file.readline()
        print(f'> {flag}')

def get_input():
    try:
        print('INPUT')
        n, x = map(int, input('> ').split())
        a = list(map(int, input('> ').split()))

        if not (1 <= n <= 200000):
            raise ValueError()
        if not (0 <= x <= 1000000000000000000):
            raise ValueError()
        if len(a) != n:
            raise ValueError()
        if not (0 <= min(a) and max(a) <= 1000000000000000000):
            raise ValueError()
        
        return f'{n} {x}\n{' '.join(map(str, a))}'
    
    except ValueError: 
        print('\nInvalid Input')

        return None

user_input = get_input()
if user_input:
    run(user_input)