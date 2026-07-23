import threading
import time
import pyperclip


# clipboard copy timeout
def clear_clipboard_after(text, timeout):
    time.sleep(timeout)

    if pyperclip.paste() == text:
        pyperclip.copy("")

def copy_to_clipboard(text, timeout):
    pyperclip.copy(text)

    thread = threading.Thread(
        target=clear_clipboard_after,
        args=(text, timeout),
        daemon=True
    )
    thread.start()


# auto lock timeout
def update_activity():
    global last_activity
    last_activity = time.time()

def system_timeout(timeout):
    global logged_out

    while not logged_out:
        if time.time() - last_activity >= timeout:
            logged_out = True
            print("\nSession timed out.")
            break

        time.sleep(1)