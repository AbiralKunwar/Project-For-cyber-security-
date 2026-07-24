import customtkinter as ctk
from password_strength_checker import check_password_strength, generate_password

# ---------------- Appearance ---------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- Window ---------------- #
app = ctk.CTk()
app.title("Password Strength Checker")
app.geometry("650x500")
app.resizable(False, False)

# ---------------- Title ---------------- #
title = ctk.CTkLabel(
    app,
    text="🔐 Password Strength Checker",
    font=("Arial", 28, "bold"),
    text_color="#00FF11"
)
title.pack(pady=20)

# ---------------- Password Entry ---------------- #
# ---------------- Password Frame ---------------- #
password_frame = ctk.CTkFrame(
    app,
    fg_color="#1F1F1F",
    corner_radius=25,
    border_width=2,
    border_color="#9CFF00"
)
password_frame.pack(pady=10)

entry = ctk.CTkEntry(
    password_frame,
    width=380,
    height=45,
    placeholder_text="Enter your password",
    show="*",
    fg_color="transparent",
    border_width=0,
    text_color="white"
)
entry.grid(row=0, column=0, padx=(15,0)
)
entry.grid(row=0, column=0)

show_password = False

def toggle_password():
    global show_password

    show_password = not show_password

    if show_password:
        entry.configure(show="")
        eye_btn.configure(text="🙈")
    else:
        entry.configure(show="*")
        eye_btn.configure(text="👁")

eye_btn = ctk.CTkButton(
    password_frame,
    text="👁",
    width=40,
    height=40,
    fg_color="transparent",
    hover_color="#2A2A2A",
    border_width=0,
    command=toggle_password,
    text_color="#9CFF00"
)
eye_btn.grid(row=0, column=1, padx=(0,10))


# ---------------- Strength Label ---------------- #
strength = ctk.CTkLabel(
    app,
    text="Password Strength",
    font=("Arial", 18)
    
)
strength.pack()

# ---------------- Progress Bar ---------------- #
progress = ctk.CTkProgressBar(app, width=400)
progress.pack(pady=10)
progress.set(0)

# ---------------- Result Box ---------------- #
result = ctk.CTkTextbox(app, width=500, height=120)
result.pack(pady=15)

# ---------------- Show / Hide Password ---------------- #
show_password = False

def toggle_password():
    global show_password

    show_password = not show_password

    if show_password:
        entry.configure(show="")
        eye_btn.configure(text="🙈")
    else:
        entry.configure(show="*")
        eye_btn.configure(text="👁")

# ---------------- Check Password ---------------- #
def check():

    password = entry.get()

    if password == "":
        return

    output = check_password_strength(password)

    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        score += 1

    progress.set(score / 5)

    if score <= 2:
        strength.configure(text="🔴 Weak", text_color="red")
    elif score == 3:
        strength.configure(text="🟡 Medium", text_color="yellow")
    elif score == 4:
        strength.configure(text="🟢 Strong", text_color="lightgreen")
    else:
        strength.configure(text="💎 Very Strong", text_color="#00FF99")

    result.delete("1.0", "end")
    result.insert("end", output)

# -----------------countdown for generate button----------------- #
def countdown(seconds):
    if seconds > 0:
        generate_btn.configure(
            text=f"Wait {seconds}s",
            state="disabled"
        )

        app.after(1000, lambda: countdown(seconds - 1))

    else:
        generate_btn.configure(
            text="Generate Password",
            state="normal"
        )
# ---------------- Generate Password ---------------- #
def generate():

    # Start countdown
    countdown(10)

    word = entry.get()

    if word == "":
        word = "Password"

    new_password = generate_password(word)

    entry.delete(0, "end")
    entry.insert(0, new_password)

    check()

# ---------------- Clear ---------------- #
def clear():

    entry.delete(0, "end")

    result.delete("1.0", "end")

    progress.set(0)

    strength.configure(
        text="Password Strength",
        text_color="white"
    )

# ---------------- Buttons ---------------- #
frame = ctk.CTkFrame(app, fg_color="transparent")
frame.pack(pady=20)

check_btn = ctk.CTkButton(
    frame,
    text="Check Password",
    width=150,
    fg_color="green",
    hover_color="#00CC00",
    command=check
)
check_btn.grid(row=0, column=0, padx=10)

generate_btn = ctk.CTkButton(
    frame,
    text="Generate Password",
    width=150,
    command=generate
)
generate_btn.grid(row=0, column=1, padx=10)

clear_btn = ctk.CTkButton(
    frame,
    text="Clear",
    width=150,
    fg_color="red",
    hover_color="#F42929",
    command=clear
)
clear_btn.grid(row=0, column=2, padx=10)

# ---------------- Footer ---------------- #
footer = ctk.CTkLabel(
    app,
    text="Cyber Security Project • Developed by Abiral Xettri",
    text_color="gray"
)
footer.pack(side="bottom", pady=10)

app.mainloop()