import time

def timed(label, func, *args, **kwargs):
    start = time.perf_counter()
    
    result = func(*args, **kwargs)
    
    elapsed = time.perf_counter() - start
    print(f"[{label}] {elapsed:.2f}s")
    
    return result