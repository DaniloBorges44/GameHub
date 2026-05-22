import customtkinter as CTK
import subprocess
import pygame
import pyautogui
from PIL import Image

# --- Functions ---
def update_carousel(index): # Inicia e tualiza o carrossel
    item = emulators[index]

    main_button.configure(
        text=item["text"],
        image=item["image"],
        command=item["command"],
        hover_color=item["hover_color"],
        fg_color=item["fg_color"]
    )
    
def next_item(): # Passa para o proximo item da lista
    global index

    index = (index + 1) % len(emulators)
    update_carousel(index)
    
def prev_item():  # Passa para o item anterior da lista
    global index

    index = (index - 1) % len(emulators)
    update_carousel(index)

def execute_playstation():
    subprocess.run(["notepad.exe"])
    
def execute_gba():
    subprocess.run(["notepad.exe"])

def execute_nintendo_64():
    subprocess.run(["notepad.exe"])
# --- Functions ---

# --- Images ---
psx2_image = CTK.CTkImage(light_image=Image.open("imgs\PCSX2_logo.png"), dark_image=Image.open("imgs\PCSX2_logo.png"), size=(100, 100))
mgba_image = CTK.CTkImage(light_image=Image.open("imgs\mGBA_logo.png"), dark_image=Image.open("imgs\mGBA_logo.png"), size=(100, 100))
simple64_image = CTK.CTkImage(light_image=Image.open("imgs\simple64_logo.png"), dark_image=Image.open("imgs\simple64_logo.png"), size=(100, 100))
# --- Images ---


# --- Emulators
emulators = [
    {
        "text": "PlayStation 2",
        "image": psx2_image,
        "command": execute_playstation,
        "hover_color":"#4860b1",
        "fg_color":"#1d3d6c"
    },
    {
        "text": "Game Boy Adventure",
        "image": mgba_image,
        "command": execute_gba,
        "hover_color":"#857de1",
        "fg_color":"#5b33b0"                                                                                  
    },
    {
        "text": "Nintendo 64",
        "image": simple64_image,
        "command": execute_nintendo_64,
        "hover_color":"#e94527",
        "fg_color":"#9e0b0f"  
    }
]
# --- Emulators ---

# --- App ---
# inicialização das variáveis  
index = 0
DEADZONE = 0.1
SPEED = 15

# Inicialização do Pygame e do CustomTkinter
pygame.init()
pygame.joystick.init()
app = CTK.CTk()

if pygame.joystick.get_count() == 0: # Verifica se há um controle conectado
    print("No gamepad found!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller: {joystick.get_name()} connected.")

# --- Interface ---
CTK.set_appearance_mode("dark") # Define o modo de aparência para "dark"
app.attributes('-fullscreen', True) # Define o aplicativo para tela cheia
CTK.CTkFrame(app, width=1050, height=600, fg_color="#0F0F0F").place(relx=0.5, rely=0.5,  anchor=CTK.CENTER) # Cria o fundo do carrossel

main_button = CTK.CTkButton( # Botão principal do carrossel
    app,
    text="",
    image=None,
    compound="top",
    hover_color="white",
    fg_color="white",
    bg_color="#0F0F0F",
    width=900,
    height=500
)

main_button.place(relx=0.5, rely=0.5, anchor=CTK.CENTER) # Posiciona o botão principal

CTK.CTkButton(app, text=">", width=40, height=40, corner_radius=80, bg_color="#0F0F0F", command=next_item).place(relx=0.844, rely=0.5) # Botão de avançar

CTK.CTkButton(app, text="<", width=40, height=40, corner_radius=80, bg_color="#0F0F0F", command=prev_item).place(relx=0.12, rely=0.5) # Botão de retroceder

exit_button = CTK.CTkButton( # Botão de sair
    app, 
    text="X",
    font=(None, 18),  
    width=40, 
    height=30,
    border_width=3,
    border_color="black",
    fg_color="#FF0000",
    hover_color="#D81313",
    command=app.destroy).place(x=app.winfo_screenwidth() - 80, y=20)
# --- Interface ---

# Inicializa a interface
update_carousel(index)
app.mainloop()

while True:
    pygame.event.pump()

    h_axis = joystick.get_axis(0) # Eixo horizontal (0)
    v_axis = joystick.get_axis(1) # Eixo vertical (1)

    if abs(h_axis) > DEADZONE or abs(v_axis) > DEADZONE: # Verifica se o movimento do joystick é maior que a DEADZONE
        pyautogui.moveRel(h_axis * SPEED, v_axis * SPEED)

    if joystick.get_button(0): # Verifica se o botão A foi pressionado (0)
        pyautogui.click()
        pygame.time.wait(200) # Evitar clique duplo
    
    pygame.time.delay(10) # Delay para atrasar o loop
# --- App ---