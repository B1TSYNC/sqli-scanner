import threading
import requests
import os
import ascii_magic


# please put the URL's with or without URI's you want to scan inside of the default endpoints file -> endpoints.txt
# please put the URL's with or without URI's you want to scan inside of the default endpoints file -> endpoints.txt
# please put the URL's with or without URI's you want to scan inside of the default endpoints file -> endpoints.txt
# please put the URL's with or without URI's you want to scan inside of the default endpoints file -> endpoints.txt

# ALSO THIS IS BETTER RUN IN THE VISUAL STUDIO CODE TERMINAL


def testparams(url, payload, results_file):
    try:
        dl = f"{url}{payload}"
        r = requests.get(dl)
        if "SQL" in r.text.upper() or "Error" in r.text.lower():
            print(f"> SQL Injectable paramater found: {dl}")
            with open(results_file, 'a') as sqli:
                sqli.write(f"{dl}\n")
    except Exception as e:
        print(f"> Exception caught: {e}")

def scan_sqli(url_list, payload_list, results_file):
    threads = []
    for url in url_list:
        for payload in payload_list:
            t = threading.Thread(target=testparams, args=(url, payload, results_file))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    endpoints_file = input("> Endpoints file: ") # The file containing the endpoints / directories you want to scan, f.eg http://example.com/ or http://example.com/login/
    payloads_file = input("> Payloads file: ") # The file containing the SQLi payloads. You can add more by searching for SQLi wordlists globally.
    results_file = input("> Results file: ") # The file where vulnerable paramaters are stored.

    if not os.path.isfile(endpoints_file) or not os.path.isfile(payloads_file):
        print("> Error: Endpoints or Payloads file not given or found.") # This error can be caught when no files are created or populated with the needed information.
    else:
        url_list = open(endpoints_file, 'r').read().split('\n')
        payload_list = open(payloads_file, 'r').read().split('\n')
        scan_sqli(url_list, payload_list, results_file)
