import customtkinter as CTK
import subprocess
from PIL import Image

# --- Functions ---
def update_carousel(index): # Inicia e tualiza o carrossel
    item = items[index]

    main_button.configure(
        text=item["text"],
        image=item["image"],
        command=item["command"]
    )
    
def next_item(): # Passa para o proximo item da lista
    global index

    index = (index + 1) % len(items)
    update_carousel(index)
    
def prev_item():  # Passa para o item anterior da lista
    global index

    index = (index - 1) % len(items)
    update_carousel(index)

def execute_playstation():
    subprocess.run(["notepad.exe"])
    
def execute_gba():
    print("Executing Game Boy Advance...")

def execute_nintendo_64():
    print("Executing Nintendo 64...")
# --- Functions ---

# --- Images ---
psx2_image = CTK.CTkImage(light_image=Image.open("imgs\PCSX2_logo.png"), dark_image=Image.open("imgs\PCSX2_logo.png"), size=(80, 80))
mgba_image = CTK.CTkImage(light_image=Image.open("imgs\mGBA_logo.png"), dark_image=Image.open("imgs\mGBA_logo.png"), size=(80, 80))
simple64_image = CTK.CTkImage(light_image=Image.open("imgs\simple64_logo.png"), dark_image=Image.open("imgs\simple64_logo.png"), size=(80, 80))
# --- Images ---


# --- Emulators
items = [
    {
        "text": "PlayStation 2",
        "image": psx2_image,
        "command": execute_playstation
    },
    {
        "text": "Game Boy Adventure",
        "image": mgba_image,
        "command": execute_gba
    },
    {
        "text": "Nintendo 64",
        "image": simple64_image,
        "command": execute_nintendo_64
    }
]
# --- Emulators ---

# --- App ---
CTK.set_appearance_mode("dark")
app = CTK.CTk()
app.attributes('-fullscreen', True)
index = 0

CTK.CTkFrame(app, width=1050, height=600, fg_color="#0F0F0F").place(relx=0.5, rely=0.5,  anchor=CTK.CENTER)

main_button = CTK.CTkButton(
    app,
    text="",
    image=None,
    compound="top",
    hover_color="#444341",
    fg_color="transparent",
    bg_color="#333231",
    width=900,
    height=500
)

main_button.place(relx=0.5, rely=0.5, anchor=CTK.CENTER)

CTK.CTkButton(app, text=">", width=40, height=40, corner_radius=80, bg_color="#0F0F0F", command=next_item).place(relx=0.844, rely=0.5)

CTK.CTkButton(app, text="<", width=40, height=40, corner_radius=80, bg_color="#0F0F0F", command=prev_item).place(relx=0.12, rely=0.5)

exit_button = CTK.CTkButton(
    app, 
    text="EXIT", 
    command=app.destroy, 
    width=60, 
    height=50,
    fg_color="#FF0000"  ,
    hover_color="#D81313").place(x=app.winfo_screenwidth() - 80, y=20)

update_carousel(index)
app.mainloop()
# --- App ---