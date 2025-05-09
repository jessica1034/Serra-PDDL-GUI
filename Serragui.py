import subprocess
import pygame
import time
import os

# Configurazione file
DOMAIN_FILE = "serrairrigazionev5_domain.pddl"
PROBLEM_FILE = input("Inserisci il nome del file problem (ATTENZIONE! Va scritto con estensione .pddl): ")
     # Verifica iniziale del file
while not os.path.isfile(PROBLEM_FILE):
        print(f"File '{PROBLEM_FILE}' non trovato! File disponibili:")
        for f in os.listdir('.'):
            if f.endswith('.pddl'):
                print(f" - {f}")
        PROBLEM_FILE = input("\nInserisci il nome corretto del file problem (ATTENZIONE:Va scritto con estensione .pddl): ")
    


ENHSP_JAR = "enhsp.jar"
MODALITA = input("Inserisci la modalità di enshp (Suboptimal: digitare 'sat-hadd' Optimal: digitare 'opt-hrmax'): ")
while MODALITA not in ['sat-hadd', 'opt-hrmax']:
    MODALITA = input("Inserisci la modalità di enshp (Suboptimal: digitare 'sat-hadd' Optimal: digitare 'opt-hrmax'): ")



# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
CYAN = (0, 255, 255)
DARK_BLUE = (0, 50, 150)
LIGHT_GREEN = (150, 255, 150)

# Dimensioni finestra iniziali
WIDTH, HEIGHT = 1000, 600


def run_planner():
    """Esegue il planner EnSHaP e restituisce l'output del piano."""
    cmd = ["java", "-jar", ENHSP_JAR, "-o", DOMAIN_FILE, "-f", PROBLEM_FILE, "-planner", MODALITA]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def parse_plan(output_text):
    """Estrae il piano (sequenza di azioni) dal testo di output del planner."""
    plan = []
    reading = False
    for line in output_text.splitlines():
        if "Found Plan:" in line:
            reading = True
            continue
        if reading:
            if not line.strip() or line.startswith("Plan-Length"):
                break
            parts = line.split(":", 1)
            if len(parts) > 1:
                action = parts[1].strip().strip("()")
                plan.append(action)
    return plan

def estrai_piante_da_problem(filepath):
    """Estrae i nomi delle piante dal file PDDL (sezione :objects)."""
    with open(filepath, 'r') as f:
        lines = f.readlines()

    piante = []
    in_objects = False
    for line in lines:
        if ":objects" in line:
            in_objects = True
            continue
        if in_objects:
            if ")" in line:
                break
            if "- pianta" in line:
                parti = line.strip().split("-")[0].strip()
                piante += parti.split()
    return piante

def parse_initial_state():
    global giorno
    giorno = "lunedì"
    global momento
    momento = "mattina"
    """Estrae lo stato iniziale dal file PDDL (sezione :init)."""
    with open(PROBLEM_FILE, 'r') as f:
        text = f.read().lower()

    state = {
        'umidita': {},
        'manutenzione': {},
        'serbatoio': 4,
        'fabbisogno': {},
        'piante': estrai_piante_da_problem(PROBLEM_FILE)
    }

    for line in text.splitlines():
        line = line.strip()
        if '(umidita-basso' in line:
            p = line.split()[1].strip(')')
            state['umidita'][p] = 'bassa'
        if '(umidita-alto' in line or '(umidita-alta' in line:
            p = line.split()[1].strip(')')
            state['umidita'][p] = 'alta'
        if '(=(livello-serbatoio)' in line:
            try:
                val = int(line.strip('()').split()[-1].replace(")", ""))
                state['serbatoio'] = val
            except:
                pass
        if '(=(quantita-acqua-pianta' in line:
            try:
                line = line.replace('(', ' ').replace(')', ' ')
                parts = line.split()
                plant = parts[2]
                qty = int(parts[3])
                state['fabbisogno'][plant] = qty
            except:
                pass

    if ':objects' in text:
        block = text.split(':objects')[1].split(':init')[0]
        for token in block.replace('\n', ' ').split():
            if 'irrigatore' in token:
                state['manutenzione'][token] = False

    for p in state['piante']:
        if p not in state['umidita']:
            state['umidita'][p] = 'bassa'
    
    # Inizializza il contatore degli utilizzi per ogni irrigatore
    state['utilizzi'] = {}
    for irr in state['manutenzione'].keys():
        state['utilizzi'][irr] = 0

    state['Manutenzione eseguita'] = {}
    for irr in state['manutenzione'].keys():
        state['Manutenzione eseguita'][irr] = 0

    return state

def update_state(state, action):
    """Aggiorna lo stato in base all'azione eseguita."""
    global giorno  # Variabile globale per aggiornare il giorno
    global momento  # Variabile globale per aggiornare il momento della giornata
    if action.startswith('irrigazione'):
        parts = action.split()
        plant = parts[1]
        # Se l'azione specifica anche l'irrigatore (es.: "irrigazione lattuga irrigatore-lattuga")
        irrigator = parts[2] if len(parts) >= 3 else None
        qty = state['fabbisogno'].get(plant, 1)
        old = state['serbatoio']
        new = max(0, old - qty)
        state['serbatoio'] = new
        state['_serbatoio_transizione'] = (old, new)
        state['umidita'][plant] = 'alta'
        # Incrementa il contatore degli utilizzi per l'irrigatore
        if irrigator is not None:
            state['utilizzi'][irrigator] = state['utilizzi'].get(irrigator, 0) + 1
        else:
            print("Azione irrigazione senza irrigatore specificato!")
    elif action.startswith('ricarica-serbatoio'):
        state['_serbatoio_transizione'] = (state['serbatoio'], 4)
        state['serbatoio'] = 4
    elif action.startswith('esegui-manutenzione'):
        irr = action.split()[1]
        state['manutenzione'][irr] = True
    elif action.startswith('manutenzione-finita'):
        irr = action.split()[1]
        state['manutenzione'][irr] = False
        state['Manutenzione eseguita'][irr] = state['Manutenzione eseguita'].get(irr, 0) + 1    
    elif action.startswith('umidita-media'):
        plant = action.split()[1]
        state['umidita'][plant] = 'media'
    elif action.startswith('umidita-bassa'):
        plant = action.split()[1]
        state['umidita'][plant] = 'bassa'
    
    # Aggiornamento del giorno
    if "martedi-mattina" in action:
        giorno = "martedì"
        momento = "mattina"
    elif "mercoledi-mattina" in action:
        giorno = "mercoledì"
        momento = "mattina"
    elif "giovedi-mattina" in action:
        giorno = "giovedì"
        momento = "mattina"
    elif "venerdi-mattina" in action:
        giorno = "venerdì"
        momento = "mattina"
    elif "sabato-mattina" in action:
        giorno = "sabato"
        momento = "mattina"
    elif "domenica-mattina" in action:
        giorno = "domenica"
        momento = "mattina"

    elif "pomeriggio" in action:
        momento = "pomeriggio"
    elif "sera" in action:  
        momento = "sera"

    
    return state


def draw(state, action_text, screen, font, avanti_rect, indietro_rect, inizio_rect, fine_rect, idx, plan):
    """Disegna lo stato corrente, gli irrigatori e i pulsanti sulla finestra Pygame."""
    screen.fill(WHITE)
    width, height = screen.get_size()

    # Ottieni la posizione del mouse
    mouse_pos = pygame.mouse.get_pos()

    # Determina se il mouse è sopra i pulsanti
    hovering_avanti = avanti_rect.collidepoint(mouse_pos)
    hovering_indietro = indietro_rect.collidepoint(mouse_pos)
    hovering_inizio = inizio_rect.collidepoint(mouse_pos)
    hovering_fine = fine_rect.collidepoint(mouse_pos)

    # Titolo
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Simulazione Irrigazione Serra", True, DARK_BLUE)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 10))

    # Stato del piano: "Start", "Finish" o azione corrente
    if idx == 0:
        status_text = "Start"  # Mostra "Start" all'inizio del piano
    elif idx >= len(plan):
        status_text = "Finish"  # Mostra "Finish" alla fine del piano
    else:
        status_text = f"Azione successiva mostrata: {action_text}"  # Mostra l'azione corrente

    # Disegna il rettangolo dello stato
    pygame.draw.rect(screen, (230, 230, 250), (30, 470, width - 60, 40), border_radius=10)
    screen.blit(font.render(status_text, True, BLACK), (40, 480))

   # Scritta "Goal" con testo su più righe
    legenda_font = pygame.font.Font(None, 20)
    legenda_text = """
    VERDE = Livello di umidità alto
    ARANCIONE = Livello di umidità medio
    ROSSO = Livello di umidità basso

    """
    legenda_lines = legenda_text.splitlines()  # Dividi il testo in righe

    # Posizione iniziale
    legenda_x = width - 300  # Posizione orizzontale (a destra)
    legenda_y = 100  # Posizione verticale iniziale

# Disegna ogni riga
    for i, line in enumerate(legenda_lines):
        rendered_line = legenda_font.render(line, True, BLACK)
        screen.blit(rendered_line, (legenda_x, legenda_y + i * 20))  # Incrementa la posizione verticale    # Giorno
        subtitle_font = pygame.font.Font(None, 32)
        giorno_text = subtitle_font.render(f"Giorno: {giorno.capitalize()} - {momento.capitalize()}", True, BLACK)
        screen.blit(giorno_text, (width // 2 - giorno_text.get_width() // 2, 60))


    # Stato del serbatoio
    pygame.draw.rect(screen, BLACK, (60, 100, 50, 300), 2)
    max_livello = 4
    h = int(300 * state['serbatoio'] / max_livello)
    pygame.draw.rect(screen, BLUE, (60, 100 + 300 - h, 50, h))
    screen.blit(font.render("Acqua", True, BLACK), (65, 410))
    screen.blit(font.render(f"{round(state['serbatoio'], 1)}/4", True, BLACK), (65, 430))

    # Disegna le piante
    x0 = (width - (len(state['piante']) * 200)) // 2
    for i, plant in enumerate(state['piante']):
        um = state['umidita'].get(plant, 'bassa')  # Default to 'bassa' if the plant's humidity is not found in the state
        fabbisogno = state['fabbisogno'].get(plant, '?')
        x = x0 + i * 200
        y = 150
        if um == 'bassa':
            color = RED
        elif um == 'alta':
            color = GREEN
        elif um == 'media':
            color =  color = (255, 165, 0)  # Arancione per umidità media
        pygame.draw.circle(screen, color, (x, y), 40)
        plant_text = font.render(plant.capitalize(), True, BLACK)
        screen.blit(plant_text, (x - plant_text.get_width() // 2, y + 50))
        status_text = font.render("Serve irrigazione" if um == 'bassa' else "In salute", True, BLACK)
        screen.blit(status_text, (x - status_text.get_width() // 2, y + 70))
        fabbisogno_text = font.render(f"Acqua richiesta: {fabbisogno}", True, BLACK)
        screen.blit(fabbisogno_text, (x - fabbisogno_text.get_width() // 2, y + 90))

  # Calcola la posizione iniziale per centrare gli irrigatori
    # Calcola la posizione iniziale per centrare gli irrigatori
    for i, (irr, man) in enumerate(state['manutenzione'].items()):  # Itera solo sugli irrigatori effettivi
        if i==1:
            continue
        x = x0 + (i - 1) * 200 if i > 1 else x0  # Trasla di una posizione indietro per irrigatori successivi al primo
        y = 300  # Posizione verticale degli irrigatori
        col = (160, 160, 160) if man else (230, 230, 250)
        # Disegna il rettangolo dell'irrigatore
        pygame.draw.rect(screen, col, (x - 50, y, 100, 45), border_radius=8)
        screen.blit(font.render("Irrigatore", True, BLACK), (x - 35, y + 5))
        screen.blit(font.render("MAN" if man else "OK!", True, BLACK), (x - 15, y + 27))
        # Mostra il valore di "utilizzo irrigatore" sotto il rettangolo
        usage = state['utilizzi'].get(irr, 0)
        usage_text = font.render(f"N.utilizzi: {usage}", True, BLACK)
        screen.blit(usage_text, (x - usage_text.get_width() // 2, y + 50))
        # Mostra il valore di "Manutenzione eseguita" sotto il rettangolo
        manutention = state['Manutenzione eseguita'].get(irr, 0)
        manutention_text = font.render(f"N. manutenzioni: {manutention}", True, BLACK)
        screen.blit(manutention_text, (x - manutention_text.get_width() // 2, y + 65))


    # Disegna i pulsanti
    for rect, text, hovering in [(avanti_rect, "Avanti", hovering_avanti),
                                 (indietro_rect, "Indietro", hovering_indietro),
                                 (inizio_rect, "Inizio", hovering_inizio),
                                 (fine_rect, "Fine", hovering_fine)]:
        color = (200, 200, 200) if hovering else GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        btn_text = font.render(text, True, BLACK)
        screen.blit(btn_text, (rect.x + (rect.width - btn_text.get_width()) // 2,
                               rect.y + (rect.height - btn_text.get_height()) // 2))

    # Azione corrente
    pygame.draw.rect(screen, (230, 230, 250), (30, 470, width - 60, 40), border_radius=10)
    screen.blit(font.render(f"Azione successiva mostrata: {action_text}", True, BLACK), (40, 480))

    pygame.display.flip()

def animate_serbatoio(screen, font, state, action_text):
    """Anima il cambiamento del livello del serbatoio durante la simulazione."""
    if '_serbatoio_transizione' not in state:
        return
    old, new = state['_serbatoio_transizione']
    steps = 10
    for i in range(steps + 1):
        interpolato = old + (new - old) * i / steps
        state['serbatoio'] = interpolato
        draw(state, action_text, screen, font)
        time.sleep(0.05)
    state['serbatoio'] = new
    del state['_serbatoio_transizione']

def main():
    """Funzione principale per eseguire la simulazione e visualizzare il piano in Pygame."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Simulazione Irrigazione Serra")
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    simulation_started = False
    plan = []
    state = {}
    idx = 0

    running = True

    while running:
        width, height = screen.get_size()
        avanti_rect = pygame.Rect(width // 2 + 60, height - 60, 100, 40)
        indietro_rect = pygame.Rect(width // 2 - 160, height - 60, 100, 40)
        inizio_rect = pygame.Rect(width // 2 - 270, height - 60, 100, 40)
        fine_rect = pygame.Rect(width // 2 + 170, height - 60, 100, 40)
        button_rect = pygame.Rect(width // 2 - 100, height // 2 - 30, 200, 60)  # Spostato qui

        mouse_pos = pygame.mouse.get_pos()

        # Determina se il mouse è sopra i pulsanti
        hovering_avanti = avanti_rect.collidepoint(mouse_pos)
        hovering_indietro = indietro_rect.collidepoint(mouse_pos)
        hovering_inizio = inizio_rect.collidepoint(mouse_pos)
        hovering_fine = fine_rect.collidepoint(mouse_pos)
        hovering_button = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not simulation_started and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Mostra schermata di caricamento
                    screen.fill((240, 255, 240))
                    loading_text = font.render("Caricamento piano in corso...", True, BLACK)
                    screen.blit(loading_text, (screen.get_width() // 2 - loading_text.get_width() // 2, screen.get_height() // 2 - 80))
                    pygame.display.flip()

                    # Esegui il planner
                    output = run_planner()
                    plan = parse_plan(output)
                    state = parse_initial_state()

                    simulation_started = True

            if simulation_started and event.type == pygame.MOUSEBUTTONDOWN:
                 if avanti_rect.collidepoint(event.pos) and idx < len(plan) - 1:
                 # Avanza al passo successivo
                     action = plan[idx]
                     state = update_state(state, action)
                     idx += 1
                 elif indietro_rect.collidepoint(event.pos) and idx > 0:
                   # Torna al passo precedente
                     idx -= 1
                     state = parse_initial_state()
                     for i in range(idx):
                         state = update_state(state, plan[i])
                 elif inizio_rect.collidepoint(event.pos):
                 # Vai all'inizio
                     idx = 0
                     state = parse_initial_state()
                 elif fine_rect.collidepoint(event.pos):
                    # Vai alla fine
                     idx = len(plan) - 1
                     state = parse_initial_state()
                     for i in range(idx):
                       state = update_state(state, plan[i])

        # Disegna lo stato e i pulsanti
        if simulation_started:
           action_text = plan[idx] if idx < len(plan) else "Fine del piano"
           draw(state, action_text, screen, font, avanti_rect, indietro_rect, inizio_rect, fine_rect, idx, plan)
        else:
            # Disegna solo il bottone per avviare la simulazione
            screen.fill((240, 255, 240))
            pygame.draw.rect(screen, (150, 250, 150) if hovering_button else (100, 200, 100), button_rect, border_radius=10)
            screen.blit(font.render("Avvia Simulazione", True, WHITE), (button_rect.x + 30, button_rect.y + 20))

        # Cambia il cursore in una mano se il mouse è sopra un pulsante
        if hovering_button or hovering_avanti or hovering_indietro or hovering_inizio or hovering_fine:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
if __name__ == '__main__':
    main()
