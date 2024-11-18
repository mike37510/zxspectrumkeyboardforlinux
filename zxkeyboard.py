import RPi.GPIO as GPIO
import time
import uinput

# Définir le mode de numérotation des GPIO
GPIO.setmode(GPIO.BCM)

# Lignes de données (dataLines)
dataLines = [26, 19, 13, 6, 5]

# Lignes d'adresse (addressLines)
addressLines = [25, 24, 23, 22, 27, 18, 17, 4]

# Configuration des pins GPIO en entrée et avec résistance de pull-up
for pin in dataLines:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in addressLines:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Initialisation des lignes d'adresse à l'état haut

# Mappage des touches en mode normal
normal_mode_matrix = [
    ['1', '2', '3', '4', '5'],
    ['q', 'w', 'e', 'r', 't'],
    ['a', 's', 'd', 'f', 'g'],
    ['0', '9', '8', '7', '6'],
    ['p', 'o', 'i', 'u', 'y'],
    ['LEFTSHIFT', 'z', 'x', 'c', 'v'],
    ['ENTER', 'l', 'k', 'j', 'h'],
    ['SPACE', 'RIGHTCTRL', 'm', 'n', 'b']
]

# Mappage des touches en mode SYMBOL
symbol_mode_matrix = [
    ['!', '@', '#', '$', '%'],
    ['<=', '<>', '>=', '<', '>'],
    ['STOP', 'NOT', 'STEP', 'TO', 'THEN'],
    ['BACKSPACE', ')', '(', "'", '&'],  # BACKSPACE remplace _
    ['"', ';', 'AT', 'OR', 'AND'],
    ['LEFTSHIFT', ':', '£', '?', '/'],
    ['ENTER', '=', '+', '-', 'UP'],
    ['SPACE', 'RIGHTCTRL', '.', "'", '*']
]

# Variable pour suivre l'état du mode : normal ou SYMBOL
current_mode = 'normal'  # Le mode par défaut est "normal"

# Variable pour suivre si LEFTSHIFT est actif
left_shift_active = False

# Initialisation de uinput
device = uinput.Device([
    uinput.KEY_A, uinput.KEY_B, uinput.KEY_C, uinput.KEY_D,
    uinput.KEY_E, uinput.KEY_F, uinput.KEY_G, uinput.KEY_H,
    uinput.KEY_I, uinput.KEY_J, uinput.KEY_K, uinput.KEY_L,
    uinput.KEY_M, uinput.KEY_N, uinput.KEY_O, uinput.KEY_P,
    uinput.KEY_Q, uinput.KEY_R, uinput.KEY_S, uinput.KEY_T,
    uinput.KEY_U, uinput.KEY_V, uinput.KEY_W, uinput.KEY_X,
    uinput.KEY_Y, uinput.KEY_Z, uinput.KEY_1, uinput.KEY_2,
    uinput.KEY_3, uinput.KEY_4, uinput.KEY_5, uinput.KEY_6,
    uinput.KEY_7, uinput.KEY_8, uinput.KEY_9, uinput.KEY_0,
    uinput.KEY_SPACE, uinput.KEY_ENTER, uinput.KEY_LEFTSHIFT,
    uinput.KEY_RIGHTCTRL, uinput.KEY_MINUS, uinput.KEY_EQUAL,
    uinput.KEY_SEMICOLON, uinput.KEY_APOSTROPHE, uinput.KEY_COMMA,
    uinput.KEY_DOT, uinput.KEY_SLASH, uinput.KEY_BACKSPACE
])

# Fonction pour scanner les lignes du clavier
def read_keyboard():
    global current_mode, left_shift_active

    key = None

    # Passer en revue chaque ligne d'adresse
    for i, address in enumerate(addressLines):
        # Mettre à l'état bas la ligne d'adresse actuelle
        GPIO.output(address, GPIO.LOW)

        # Lire les lignes de données
        for j, data in enumerate(dataLines):
            if GPIO.input(data) == GPIO.LOW:  # Si un bouton est pressé (niveau bas)
                key = (i, j)  # Retourner l'adresse de la touche (i, j)

                # Si la touche LEFTSHIFT est pressée, activer le suivi
                if normal_mode_matrix[i][j] == 'LEFTSHIFT':
                    left_shift_active = True
                elif normal_mode_matrix[i][j] == 'RIGHTCTRL':
                    toggle_mode()  # Basculer entre les modes si RIGHTCTRL est pressé
                else:
                    # Simuler la touche dans le mode actuel
                    key_name = get_key_name(i, j)
                    if key_name:
                        print(f"Touche pressée : {key_name}")
                        send_key_event(key_name)

        # Rétablir la ligne d'adresse à l'état haut après la lecture
        GPIO.output(address, GPIO.HIGH)

    return key

# Fonction pour obtenir le nom de la touche en fonction du mode
def get_key_name(i, j):
    if current_mode == 'normal':
        return normal_mode_matrix[i][j] if i < len(normal_mode_matrix) and j < len(normal_mode_matrix[i]) else None
    elif current_mode == 'symbol':
        return symbol_mode_matrix[i][j] if i < len(symbol_mode_matrix) and j < len(symbol_mode_matrix[i]) else None

# Fonction pour obtenir le code de la touche correspondant à un nom de touche
def get_key_code(key_name):
    key_mapping = {
        'a': uinput.KEY_A, 'b': uinput.KEY_B, 'c': uinput.KEY_C, 'd': uinput.KEY_D,
        'e': uinput.KEY_E, 'f': uinput.KEY_F, 'g': uinput.KEY_G, 'h': uinput.KEY_H,
        'i': uinput.KEY_I, 'j': uinput.KEY_J, 'k': uinput.KEY_K, 'l': uinput.KEY_L,
        'm': uinput.KEY_M, 'n': uinput.KEY_N, 'o': uinput.KEY_O, 'p': uinput.KEY_P,
        'q': uinput.KEY_Q, 'r': uinput.KEY_R, 's': uinput.KEY_S, 't': uinput.KEY_T,
        'u': uinput.KEY_U, 'v': uinput.KEY_V, 'w': uinput.KEY_W, 'x': uinput.KEY_X,
        'y': uinput.KEY_Y, 'z': uinput.KEY_Z, '1': uinput.KEY_1, '2': uinput.KEY_2,
        '3': uinput.KEY_3, '4': uinput.KEY_4, '5': uinput.KEY_5, '6': uinput.KEY_6,
        '7': uinput.KEY_7, '8': uinput.KEY_8, '9': uinput.KEY_9, '0': uinput.KEY_0,
        'SPACE': uinput.KEY_SPACE, 'ENTER': uinput.KEY_ENTER,
        'LEFTSHIFT': uinput.KEY_LEFTSHIFT, 'RIGHTCTRL': uinput.KEY_RIGHTCTRL,
        'BACKSPACE': uinput.KEY_BACKSPACE  # Ajout de BACKSPACE
    }
    return key_mapping.get(key_name)

# Fonction pour envoyer un événement de touche
def send_key_event(key_name):
    global left_shift_active

    key_code = get_key_code(key_name)

    if key_code:
        # Si LEFTSHIFT est actif et qu'une lettre est pressée
        if left_shift_active and key_name.isalpha():
            device.emit(uinput.KEY_LEFTSHIFT, 1)  # Appuyer sur LEFTSHIFT
            device.emit(key_code, 1)  # Appuyer sur la lettre
            device.emit(key_code, 0)  # Relâcher la lettre
            device.emit(uinput.KEY_LEFTSHIFT, 0)  # Relâcher LEFTSHIFT
        else:
            # Appuyer et relâcher une touche normale
            device.emit(key_code, 1)  # Appuyer sur la touche
            device.emit(key_code, 0)  # Relâcher la touche
    else:
        # Gestion des touches SYMBOL nécessitant une combinaison
        special_keys = {
            '!': (uinput.KEY_LEFTSHIFT, uinput.KEY_1),
            '@': (uinput.KEY_LEFTSHIFT, uinput.KEY_2),
            '#': (uinput.KEY_LEFTSHIFT, uinput.KEY_3),
            '$': (uinput.KEY_LEFTSHIFT, uinput.KEY_4),
            '%': (uinput.KEY_LEFTSHIFT, uinput.KEY_5),
            ')': (uinput.KEY_LEFTSHIFT, uinput.KEY_0),
            '(': (uinput.KEY_LEFTSHIFT, uinput.KEY_9),
            '"': (uinput.KEY_LEFTSHIFT, uinput.KEY_APOSTROPHE),
            "'": (uinput.KEY_APOSTROPHE,),
            '&': (uinput.KEY_LEFTSHIFT, uinput.KEY_7),
            '*': (uinput.KEY_LEFTSHIFT, uinput.KEY_8),
            '+': (uinput.KEY_LEFTSHIFT, uinput.KEY_EQUAL),
            '_': (uinput.KEY_LEFTSHIFT, uinput.KEY_MINUS),
            ':': (uinput.KEY_LEFTSHIFT, uinput.KEY_SEMICOLON),
            '<': (uinput.KEY_LEFTSHIFT, uinput.KEY_COMMA),
            '>': (uinput.KEY_LEFTSHIFT, uinput.KEY_DOT),
            '?': (uinput.KEY_LEFTSHIFT, uinput.KEY_SLASH),
            ';': (uinput.KEY_SEMICOLON,),
            '-': (uinput.KEY_MINUS,),
            '=': (uinput.KEY_EQUAL,),
            '/': (uinput.KEY_SLASH,),
            '.': (uinput.KEY_DOT,)
        }

        if key_name in special_keys:
            keys = special_keys[key_name]
            for key in keys:
                device.emit(key, 1)  # Appuyer sur chaque touche de la combinaison
            for key in keys:
                device.emit(key, 0)  # Relâcher chaque touche de la combinaison

# Fonction pour basculer entre les modes normal et SYMBOL
def toggle_mode():
    global current_mode
    if current_mode == 'normal':
        current_mode = 'symbol'
        print("Mode SYMBOL activé.")
    else:
        current_mode = 'normal'
        print("Mode normal activé.")

# Boucle principale pour lire le clavier en continu
try:
    while True:
        pressed_key = read_keyboard()
        if pressed_key:
            time.sleep(0.3)  # Délais pour éviter les lectures multiples rapides
        else:
            left_shift_active = False  # Réinitialiser LEFTSHIFT si aucune touche n'est pressée
            time.sleep(0.05)  # Ralentir la boucle s'il n'y a pas de touche pressée
except KeyboardInterrupt:
    print("Arrêt du programme.")
finally:
    GPIO.cleanup()  # Nettoyer les configurations GPIO avant de quitter
