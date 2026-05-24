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

def execute_emulator(): # Executa o emulador selecionado
     match index:
        case 0:
            print("Executando PCSX2")
            #subprocess.run(["notepad.exe"])
        case 1:
            print("Executando mGBA")
        case 2:
            print("Executando Simple64")
        case _:
            print("Emulador não encontrado")
            
def button_effect(button, border_color, border_width): # Adiciona o efeito de borda ao botão em hover
    button.configure(border_color=border_color, border_width=border_width)

def read_gamepad():
    global last_a_pressed

    if pygame.joystick.get_count() > 0:
        pygame.event.pump()

        h_axis = joystick.get_axis(0)
        v_axis = joystick.get_axis(1)
        
        if abs(h_axis) < DEADZONE:
            h_axis = 0

        if abs(v_axis) < DEADZONE:
            v_axis = 0
        
        if h_axis != 0 or v_axis != 0: # Move o mouse
            pyautogui.moveRel(int(h_axis * SPEED), int(v_axis * SPEED))

        a_pressed = joystick.get_button(0) # Botão A: clique apenas quando apertar, não enquanto segurar

        if a_pressed and not last_a_pressed:
            pyautogui.click()

        last_a_pressed = a_pressed

    app.after(10, read_gamepad) # chama novamente depois de 10ms

def close_app():
    pygame.quit()
    app.destroy()
# --- Functions ---

# --- Images ---
psx2_image = CTK.CTkImage(light_image=Image.open(r"imgs\PCSX2_logo.png"), dark_image=Image.open(r"imgs\PCSX2_logo.png"), size=(100, 100))
mgba_image = CTK.CTkImage(light_image=Image.open(r"imgs\mGBA_logo.png"), dark_image=Image.open(r"imgs\mGBA_logo.png"), size=(100, 100))
simple64_image = CTK.CTkImage(light_image=Image.open(r"imgs\simple64_logo.png"), dark_image=Image.open(r"imgs\simple64_logo.png"), size=(100, 100))
bg_image = CTK.CTkImage(light_image=Image.open(r"imgs\bg_img.jpg"), dark_image=Image.open(r"imgs\bg_img.jpg"), size=(1366, 768))
# --- Images ---


# --- Emulators
emulators = [
    {
        "text": "PlayStation 2",
        "image": psx2_image,
        "fg_color":"#1d3d6c",
        "border_color":"#4860b1",
        "border_width": 4
    },
    {
        "text": "Game Boy Adventure",
        "image": mgba_image,
        "fg_color":"#5b33b0",
        "border_color":"#857de1",
        "border_width": 4                                                                               
    },
    {
        "text": "Nintendo 64",
        "image": simple64_image,
        "fg_color":"#9e0b0f",
        "border_color":"#e94527",
        "border_width": 4
    }
]
# --- Emulators ---

# --- App ---
# inicialização das variáveis  
index = 0
DEADZONE = 0.1
SPEED = 50
last_a_pressed = False

# Inicialização do Pygame e do CustomTkinter
pygame.init()
pygame.joystick.init()
app = CTK.CTk()

if pygame.joystick.get_count() == 0: # Verifica se há um controle conectado
    print("No gamepad found!")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller: {joystick.get_name()} connected.")

# --- Interface ---
CTK.set_appearance_mode("dark") # Define o modo de aparência para "dark"
app.attributes('-fullscreen', True) # Define o aplicativo para tela cheia
CTK.CTkLabel(app, image=bg_image, text="").place(relwidth=1, relheight=1) # Define a imagem de fundo
CTK.CTkFrame(app, width=1050, height=600, fg_color="#0F0F0F", border_color="#252525", border_width=2).place(relx=0.5, rely=0.5,  anchor=CTK.CENTER) # Cria o fundo do carrossel

main_button = CTK.CTkButton( # Botão principal do carrossel
    app,
    text="",
    image=None,
    compound="top",
    hover=False,
    fg_color="white",
    bg_color="#0F0F0F",
    width=900,
    height=500,
    command=execute_emulator
)

main_button.place(relx=0.5, rely=0.5, anchor=CTK.CENTER) # Posiciona o botão principal
main_button.bind("<Enter>", lambda e: button_effect(main_button, emulators[index]["border_color"], emulators[index]["border_width"])) # Adiciona o efeito de hover ao botão principal
main_button.bind("<Leave>", lambda e: button_effect(main_button, "black", 0)) # Remove o efeito de hover quando o mouse sair do botão principal


left_button = CTK.CTkButton(app, text=">", width=40, height=40, corner_radius=80, fg_color ="#005fbe", hover_color= "#0075eb", bg_color="#0F0F0F", command=next_item) # Botão de avançar
left_button.place(relx=0.844, rely=0.5) 
right_button = CTK.CTkButton(app, text="<", width=40, height=40, corner_radius=80, fg_color ="#005fbe", hover_color= "#0075eb", bg_color="#0F0F0F", command=prev_item) # Botão de retroceder
right_button.place(relx=0.12, rely=0.5)     

left_button.bind("<Enter>", lambda e: button_effect(left_button, "#4aa5ff", 2)) 
left_button.bind("<Leave>", lambda e: button_effect(left_button, "black", 0))
right_button.bind("<Enter>", lambda e: button_effect(right_button, "#4aa5ff", 2))
right_button.bind("<Leave>", lambda e: button_effect(right_button, "black", 0))

exit_button = CTK.CTkButton( # Botão de sair
    app, 
    text="X",
    font=(None, 18),  
    width=40, 
    height=30,
    border_width=2,
    border_color="black",
    fg_color="#DB0C0C",
    hover_color="#FF0000",
    command=close_app)

exit_button.place(x=app.winfo_screenwidth() - 80, y=20)
exit_button.bind("<Enter>", lambda e: button_effect(exit_button, "#FF0000", 4))
exit_button.bind("<Leave>", lambda e: button_effect(exit_button, "black", 2))  
# --- Interface ---

# Inicializa a interface
update_carousel(index)
app.protocol("WM_DELETE_WINDOW", close_app)
read_gamepad()
app.mainloop()
# --- App ---