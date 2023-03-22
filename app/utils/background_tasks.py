import threading

def process_urls_background(urls: list, callback, delay=1):
    threading.Thread(target=callback, args=(urls, delay)).start()
