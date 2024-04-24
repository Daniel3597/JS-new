import pygame
import sys

# Definición de nodos y conexiones
graph = {
    1: [2, 3, 4],
    2: [1, 3, 6],
    3: [1, 2, 5],
    4: [1, 5],
    5: [3, 4, 7],
    6: [2, 7, 8],
    7: [5, 6, 8],
    8: [6, 7]
}

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_size = (600, 400)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Juego de Movimiento en Grafos')

# Definición de colores
white = (255, 255, 255)
blue = (0, 0, 255)
aqua_marine = (127, 255, 212)
red = (255, 0, 0)
black = (0, 0, 0)

# Definición de nodos
node_radius = 20
nodes = {
    1: (50, 200),
    2: (150, 100),
    3: (150, 300),
    4: (250, 200),
    5: (350, 300),
    6: (350, 100),
    7: (450, 200),
    8: (550, 200)
}

# Posición inicial del jugador y enemigo
player_position = 1
enemy_position = 8

# Variable para registrar si una tecla está siendo presionada
key_pressed = False

# Inicialización de la fuente
font = pygame.font.Font(None, 36)

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key_pressed = True
            if event.key == pygame.K_LEFT and player_position in graph:
                player_position = graph[player_position][0]
            elif event.key == pygame.K_RIGHT and player_position in graph:
                player_position = graph[player_position][-1]
            elif event.key == pygame.K_UP and player_position in graph:
                player_position = graph[player_position][1]
            elif event.key == pygame.K_DOWN and player_position in graph:
                player_position = graph[player_position][-2]

    if key_pressed:  # Resetear la variable después de procesar el evento
        key_pressed = False

        # Lógica de movimiento del enemigo
        possible_moves = graph[enemy_position]

        # Verificar si el jugador y el enemigo están en el mismo nodo
        if player_position == enemy_position:
            print("¡Has perdido!")
            pygame.quit()
            sys.exit()

        # Asegurarse de que haya movimientos posibles antes de calcular distancias
        if possible_moves:
            # Calcular distancias y mover hacia el jugador
            distances = [pygame.math.Vector2(nodes[move][0] - nodes[player_position][0], nodes[move][1] - nodes[player_position][1]).length() for move in possible_moves]

            # Verificar si la lista de distancias no está vacía
            if distances:
                min_distance_index = distances.index(min(distances))
                next_enemy_position = possible_moves[min_distance_index]

                # Verificar si el jugador ha llegado al nodo 8
                if player_position == 8:
                    print("¡Has ganado!")
                    pygame.quit()
                    sys.exit()

                # Verificar si el enemigo y el jugador están en el mismo nodo después del movimiento
                if next_enemy_position == player_position:
                    print("¡Has perdido!")
                    pygame.quit()
                    sys.exit()
                else:
                    enemy_position = next_enemy_position

    # Dibujar nodos y conexiones
    screen.fill(white)
    for node, position in nodes.items():
        pygame.draw.circle(screen, blue, position, node_radius)
        for neighbor in graph[node]:
            pygame.draw.line(screen, blue, nodes[node], nodes[neighbor])

    # Dibujar números de los nodos
    for node, position in nodes.items():
        text = font.render(str(node), True, black)
        text_rect = text.get_rect(center=position)
        screen.blit(text, text_rect)

    # Dibujar jugador y enemigo
    pygame.draw.circle(screen, aqua_marine, nodes[player_position], node_radius)
    pygame.draw.circle(screen, red, nodes[enemy_position], node_radius)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
