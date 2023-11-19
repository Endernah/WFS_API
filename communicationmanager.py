from collections import deque
import pickle

def request(function, **args):
    try:
        with open('queue.pkl', 'rb') as f:
            request_queue = pickle.load(f)
    except (EOFError, FileNotFoundError):
        request_queue = deque()
    request_queue.append((function, args))
    with open('queue.pkl', 'wb') as f:
        pickle.dump(request_queue, f)
    return True

def recieverequests():
    with open('queue.pkl', 'rb') as f:
        request_queue = pickle.load(f)
    if request_queue:
        function, args = request_queue.popleft()
        with open('queue.pkl', 'wb') as f:
            pickle.dump(request_queue, f)
        return {"function": function, "args": args}