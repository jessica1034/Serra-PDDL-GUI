import subprocess
import sys
import pygame 
import time

# Configurazione file
DOMAIN_FILE = "serrairrigazionev5_domain.pddl"
PROBLEM_FILE = "serrairrigazionev5_problem3.pddl"
ENHSP_JAR = "enhsp.jar"

# Colori
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,128,255)
GREEN = (0,200,0)
RED = (200,0,0)
GRAY = (200,200,200)
CYAN = (0,255,255)

# Dimensioni finestra
WIDTH, HEIGHT = 1000, 600

def run_planner():
    cmd = ["java", "-jar", ENHSP_JAR, "-o", DOMAIN_FILE, "-f", PROBLEM_FILE, "-planner", "sat-hadd"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

def parse_plan(output_text):
    plan = []
    reading = False
    for line in output_text.splitlines():
        if "Found Plan:" in line:
            reading = True
            continue
        if reading:
            if not line.strip() or line.startswith("Plan-Length"):
                break
            parts = line.split(":",1)
            if len(parts)>1:
                action = parts[1].strip().strip("()")
                plan.append(action)
    return plan

def parse_initial_state():
    with open(PROBLEM_FILE, 'r') as f:
        text = f.read().lower()
    state = {
        'umidita': {},
        'manutenzione': {},
        'serbatoio': 4,
        'fabbisogno': {}
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
                line = line.replace('(',' ').replace(')',' ')
                parts = line.split()
                plant = parts[2]
                qty = int(parts[3])
                state['fabbisogno'][plant] = qty
            except:
                pass
    # Estrarre nomi irrigatori dalla sezione :objects
    if ':objects' in text:
        block = text.split(':objects')[1].split(':init')[0]
        for token in block.replace('\n',' ').split():
            if 'irrigatore' in token:
                state['manutenzione'][token] = False
    return state

def update_state(state, action):
    if action.startswith('irrigazione'):
        plant = action.split()[1]
        qty = state['fabbisogno'].get(plant, 1)
        old = state['serbatoio']
        new = max(0, old - qty)
        state['serbatoio'] = new
        state['_serbatoio_transizione'] = (old, new)

        # L'irrigazione porta sempre l'umidità a "alta"
        state['umidita'][plant] = 'alta'

    elif action.startswith('ricarica-serbatoio'):
        state['_serbatoio_transizione'] = (state['serbatoio'], 4)
        state['serbatoio'] = 4
    elif action.startswith('esegui-manutenzione'):
        irr = action.split()[1]
        state['manutenzione'][irr] = True
    elif action.startswith('manutenzione-finita'):
        irr = action.split()[1]
        state['manutenzione'][irr] = False
    elif action.startswith('resetta-umidita'):
        plant = action.split()[1]
        if state['umidita'].get(plant) == 'alta':
            state['umidita'][plant] = 'bassa'

    return state

def draw(state, action_text, screen, font):
    screen.fill((245, 255, 250))  # verde molto chiaro

    # Titolo
    title_font = pygame.font.SysFont(None, 36)
    screen.blit(title_font.render("Simulazione Irrigazione Serra", True, BLACK), (WIDTH//2 - 160, 10))

    # Serbatoio
    pygame.draw.rect(screen, BLACK, (60, 100, 50, 300), 2)
    max_livello = 4
    h = int(300 * state['serbatoio']/max_livello)
    pygame.draw.rect(screen, BLUE, (60, 100+300-h, 50, h))
    screen.blit(font.render(f"Acqua", True, BLACK), (65, 410))
    screen.blit(font.render(f"{round(state['serbatoio'],1)}/4", True, BLACK), (65, 430))

    # Piante e irrigatori
    x0 = 180
    for i, (plant, um) in enumerate(state['umidita'].items()):
        x = x0 + i*200
        y = 150
        color = GREEN if um == 'alta' else RED
        pygame.draw.circle(screen, color, (x, y), 40)
        screen.blit(font.render(f"{plant.capitalize()}", True, BLACK), (x - 40, y + 50))

        stato = "In salute" if um == 'alta' else "Serve irrigazione"
        screen.blit(font.render(stato, True, BLACK), (x - 60, y + 70))

    # Irrigatori
    for i, (irr, man) in enumerate(state['manutenzione'].items()):
        x = x0 + i*200
        y = 250
        col = (160, 160, 160) if man else (100, 200, 255)
        pygame.draw.rect(screen, col, (x - 40, y, 80, 40), border_radius=8)
        screen.blit(font.render("Irrig.", True, BLACK), (x - 20, y + 5))
        screen.blit(font.render("MAN" if man else "OK", True, BLACK), (x - 15, y + 20))

    # Azione corrente
    pygame.draw.rect(screen, (230, 230, 250), (30, 500, 740, 40), border_radius=10)
    screen.blit(font.render(f"Azione: {action_text}", True, BLACK), (40, 510))

    pygame.display.flip()

def animate_serbatoio(screen, font, state, action_text):
    if '_serbatoio_transizione' not in state:
        return
    old, new = state['_serbatoio_transizione']
    steps = 10
    for i in range(steps+1):
        interpolato = old + (new - old) * i / steps
        state['serbatoio'] = interpolato
        draw(state, action_text, screen, font)
        time.sleep(0.05)
    state['serbatoio'] = new
    del state['_serbatoio_transizione']

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulazione Irrigazione Serra")
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 36)

    simulation_started = False
    plan = []
    state = {}
    idx = 0
    clock = pygame.time.Clock()
    last_time = time.time()

    # Bottone
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hovering = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not simulation_started and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Mostra LOADING
                    screen.fill((240, 255, 240))
                    pygame.draw.rect(screen, (100, 200, 100), button_rect, border_radius=10)
                    screen.blit(font.render("Avvia Simulazione", True, WHITE), (button_rect.x + 30, button_rect.y + 20))

                    loading_font = pygame.font.SysFont(None, 32)
                    screen.blit(loading_font.render("LOADING...", True, BLACK), (WIDTH//2 - 50, HEIGHT//2 + 50))
                    pygame.display.flip()
                    pygame.time.delay(500)  # Mostra il messaggio prima dell'elaborazione

                    # Ora esegue il planner
                    output = run_planner()
                    plan = parse_plan(output)
                    state = parse_initial_state()
                    simulation_started = True
                    last_time = time.time()

        # Se la simulazione è partita, mostra il piano passo per passo
        if simulation_started:
            if idx < len(plan) and time.time() - last_time > 2:
                action = plan[idx]
                state = update_state(state, action)
                animate_serbatoio(screen, font, state, action)
                idx += 1
                last_time = time.time()

            action_text = plan[idx-1] if idx > 0 else "Start"
            draw(state, action_text, screen, font)
        else:
            # Schermata iniziale con bottone
            screen.fill((240, 255, 240))
            pygame.draw.rect(screen, (100, 200, 100), button_rect, border_radius=10)
            screen.blit(font.render("Avvia Simulazione", True, WHITE), (button_rect.x + 30, button_rect.y + 20))

        # Cambia il cursore se sopra al bottone
        if hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    
if __name__ == '__main__':
    main()