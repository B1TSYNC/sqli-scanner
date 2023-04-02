import threading
import requests
import os
import ascii_magic

def validate_file(filename):
    if not os.path.isfile(filename):
        print(f"> Error: File '{filename}' not found.")
        return False
    elif os.stat(filename).st_size == 0:
        print(f"> Error: File '{filename}' is empty.")
        return False
    return True

def test_params(url, payload, results_file):
    try:
        dl = f"{url}{payload}"
        r = requests.get(dl)
        if "SQL" in r.text.upper() or "Error" in r.text.lower():
            print(f"> SQL Injectable paramater found: {dl}")
            with open(results_file, 'a') as sqli:
                sqli.write(f"{dl}\n")
    except requests.exceptions.RequestException as e:
        print(f"> Exception caught: {e}")
        
def scan_sqli(url_list, payload_list, results_file):
    threads = []
    thread_limit = min(10, len(url_list) * len(payload_list)) # limit to 10 threads or less
    thread_count = 0
    for url in url_list:
        for payload in payload_list:
            if thread_count >= thread_limit:
                break
            t = threading.Thread(target=test_params, args=(url, payload, results_file))
            threads.append(t)
            t.start()
            thread_count += 1
        if thread_count >= thread_limit:
            break
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    endpoints_file = input("> Endpoints file: ")
    payloads_file = input("> Payloads file: ")
    results_file = input("> Results file: ")

    if not validate_file(endpoints_file) or not validate_file(payloads_file):
        exit(1)
        
    url_list = open(endpoints_file, 'r').read().split('\n')
    payload_list = open(payloads_file, 'r').read().split('\n')
    
    if len(url_list) == 0 or len(payload_list) == 0:
        print("> Error: Endpoints or Payloads file is empty.")
        exit(1)
    
    scan_sqli(url_list, payload_list, results_file)
    
    print("> SQL injection scan complete.")
