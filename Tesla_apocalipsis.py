import pygame 
import random

# Inicializar pygame
pygame.init()

# Definir variables globales
ancho = 1000
alto = 620
escala_player = 0.17 
escala_saw = 0.07
escala_villano = 0.13
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 143, 57)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
escala_screen = 0.3
escala_menu = 1
player_alive = True
max_score =0
# Configurar la pantalla
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Tesla Apocalipsis")

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Cargar imágenes y sonidos
fondofinal = pygame.image.load("recursos/mapa/objects/fondofinal2.png")
fondofinal = pygame.transform.scale(fondofinal, (int(fondofinal.get_width() * escala_screen),
                                                 int(fondofinal.get_height() * escala_screen)))
fondo_menu = pygame.image.load("recursos/mapa/objects/fondomenu.png")
fondo_menu = pygame.transform.scale(fondo_menu, (int(fondofinal.get_width() * escala_menu),
                                                 int(fondofinal.get_height() * escala_menu)))
fondo_go = pygame.image.load("recursos/mapa/objects/fondogo.png")
fondo_go = pygame.transform.scale(fondo_go, (int(fondofinal.get_width() * escala_menu),
                                                 int(fondofinal.get_height() * escala_menu)))
# Explosion
explosion_animacion = [pygame.image.load(f"recursos/explosion/regularExplosion0{i}.png").convert_alpha() for i in range(9)]
#Estados del jugador
estado_corriendo = [pygame.image.load(f"recursos/personajes/heroe/corriendo/Run__00{i}.png").convert_alpha() for i in range(10)]
estado_corriendo = [pygame.transform.scale(img, (int(img.get_width() * escala_player), int(img.get_height() * escala_player))) for img in estado_corriendo]

estado_esperando = [pygame.image.load(f"recursos/personajes/heroe/quieto/Idle__00{i}.png").convert_alpha() for i in range(10)]
estado_esperando = [pygame.transform.scale(img, (int(img.get_width() * escala_player), int(img.get_height() * escala_player))) for img in estado_esperando]

estado_lanzando = [pygame.image.load(f"recursos/personajes/heroe/lanzando/Throw__00{i}.png").convert_alpha() for i in range(10)]
estado_lanzando = [pygame.transform.scale(img, (int(img.get_width() * escala_player), int(img.get_height() * escala_player))) for img in estado_lanzando]

estado_muriendo = [pygame.image.load(f"recursos/personajes/heroe/muriendo/Dead__00{i}.png").convert_alpha() for i in range(10)]
estado_muriendo = [pygame.transform.scale(img, (int(img.get_width() * escala_player), int(img.get_height() * escala_player))) for img in estado_muriendo]


#Robot
robot_atacando = [pygame.image.load(f"recursos/personajes/villano/atacandosaltando/JumpMelee ({i}).png").convert_alpha() for i in range(1,9)]
estado_atacando = [pygame.transform.scale(img, (int(img.get_width() * escala_villano), int(img.get_height() * escala_villano))) for img in robot_atacando]

#Sonidos
dolor_sounds = [pygame.mixer.Sound(sound) for sound in ["recursos/sounds/dolor1.ogg", "recursos/sounds/dolor2.ogg", "recursos/sounds/dolor3.ogg", "recursos/sounds/dolor4.ogg"]]
saw_sound = pygame.mixer.Sound("recursos/sounds/Throwing.ogg")
explosion_sound = pygame.mixer.Sound("recursos/sounds/Explosion.ogg")
muerte_sound = pygame.mixer.Sound("recursos/sounds/muerte.ogg")
pygame.mixer.music.load("recursos/sounds/music.ogg")



# Funcion para resetear el juego con todas las variables y contadores inciales
def reset_game():
    global player_alive, score, max_score  # Variables globales que necesitan ser reiniciadas

    # Reiniciar variables
    player_alive = True
    score = 0

    # Reiniciar las propiedades del player
    player.animacion_actual = player.animacion_esperando
    player.frame_index = 0
    player.image = player.animacion_actual[player.frame_index]
    player.rect.center = (500, 314)
    player.speed_x = 0
    player.shield = 1000
    player.update_time = pygame.time.get_ticks()
    player.update_time_lanzando = pygame.time.get_ticks()
    player.lanzando = False
    player.muriendo = False
    player.is_jumping = False
    player.jump_count = 10
    player.last_direction = 1

    # Eliminar todos los robots existentes y crear nuevos
    
    all_sprites.empty()
    robots_list.empty()
    for _ in range(1):
        robot = Robot()
        robots_list.add(robot)
        all_sprites.add(robot)

    # Eliminar todas las sierras existentes
    saw_list.empty()

    # Reiniciar la música
    pygame.mixer.music.stop()
    pygame.mixer.music.play()

    # Reiniciar la pantalla del menú
    draw_menu()

#funcion para dibujar el menu inicial
def draw_menu():
    
    screen.blit(fondo_menu,(0,0))
    
    pygame.display.flip()


#Funciones del menu
def main_menu():
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

# Funcion para definir las propiedades del texto
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(midtop=(x + 7.5, y + 9))
    surface.blit(text_surface, text_rect)

# Mostrar game over cuando player muere
def mostrar_game_over(score):
    global max_score  # Indicar que se utilizará la variable global max_score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir del juego si se presiona la tecla ESC
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:  # Volver a comenzar el juego si se presiona la tecla R
                    return True

        screen.blit(fondo_go,(0,0))
        draw_text(screen, "Game Over", 70, ancho // 2, alto // 5)
        draw_text(screen, f"Puntuación: {score}", 40, ancho // 2, alto //3)
        draw_text(screen, f"Puntuación Máxima: {max_score}", 40, ancho // 2, alto // 3 + 50)  # Mostrar la puntuación máxima
        draw_text(screen, "Presiona R para volver a empezar", 30, ancho // 2, alto * 1 //2 + 50 )
        draw_text(screen, "Presiona ESC para salir", 30, ancho // 2, alto *1/2 + 100)
        pygame.display.flip()




# Función para crear la barra de escudo o vida    
def draw_shield_bar(surface, x, y, percentage):
    bar_length = 100
    bar_height = 10
    
    # Calcular la longitud del relleno y el color de la barra de vida
    fill = (percentage / 100) * bar_length
    if percentage <= 300:
        color = RED
    elif percentage <= 600:
        color = YELLOW
    else:
        color = GREEN
    
    # Dibujar la barra de vida
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)



# Clase de la explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_animacion[0]
        self.rect = self.image.get_rect(center=center)
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index += 1
            if self.frame_index == len(explosion_animacion):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animacion[self.frame_index]
                self.rect = self.image.get_rect(center=center)

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animacion_corriendo = estado_corriendo
        self.animacion_esperando = estado_esperando
        self.animacion_lanzando = estado_lanzando
        self.animacion_muriendo = estado_muriendo
        self.animacion_actual = self.animacion_esperando
        self.frame_index = 0
        self.image = self.animacion_actual[self.frame_index]
        self.rect = self.image.get_rect(center=(500, 314))
        self.rect.inflate_ip(-30, -30)  # Reducir el rectángulo de colisión
        self.speed_x = 0
        self.shield = 1000
        self.update_time = pygame.time.get_ticks()
        self.update_time_lanzando = pygame.time.get_ticks()
        self.lanzando = False
        self.muriendo = False
        self.is_jumping = False
        self.jump_count = 10
        self.last_direction = 1

    def corriendo(self):
        now = pygame.time.get_ticks()
        cooldown_animacion = 40
        if now - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = now

            if self.frame_index >= len(self.animacion_corriendo):
                self.frame_index = 0

            if self.frame_index >= len(self.animacion_actual):
                self.frame_index = 0

            # Actualizar la imagen de acuerdo a la dirección de movimiento
            if self.speed_x < 0:  # Si se está moviendo hacia la izquierda
                self.image = self.animacion_actual[self.frame_index]
                self.image = pygame.transform.flip(self.image, True, False)
            else:  # Si se está moviendo hacia la derecha o está quieto
                self.image = self.animacion_actual[self.frame_index]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True

    def dead(self):
        muerte_sound.play()
        if not self.muriendo:
            self.muriendo = True
            # Determinar la dirección de la animación de muerte
            if self.speed_x < 0:
                self.animacion_muriendo = [pygame.transform.flip(img, True, False) for img in estado_muriendo]
            else:
                self.animacion_muriendo = estado_muriendo

    def throw(self):
        self.lanzando = True
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction_x = mouse_x - self.rect.centerx
        direction_y = mouse_y - self.rect.centery
        length = max(1, abs(direction_x) + abs(direction_y))
        direction_x /= length
        direction_y /= length

        # Determinar la dirección de la animación de lanzamiento
        if direction_x < 0:
            self.animacion_lanzando = [pygame.transform.flip(img, True, False) for img in estado_lanzando]
        else:
            self.animacion_lanzando = estado_lanzando

        saw = Saw(self.rect.centerx, self.rect.top, pygame.Vector2(direction_x * 10, direction_y * 10))
        all_sprites.add(saw)
        saw_list.add(saw)
        saw_sound.play() 

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_d]:  
            self.animacion_actual = self.animacion_corriendo
            
            if keystate[pygame.K_a]:
                self.speed_x = -5
                self.last_direction = 'left'  # Actualizar la última dirección
            elif keystate[pygame.K_d]:
                self.speed_x = 5
                self.last_direction = 'right'  # Actualizar la última dirección
        else:
            # Si no se está presionando ninguna tecla de movimiento,
            # verificar si el jugador está moviéndose y establecer la animación en consecuencia
            if self.speed_x != 0:  # Verificar si el jugador está moviéndose
                # Si el jugador está moviéndose, establecer la animación actual de acuerdo a la dirección
                if self.speed_x < 0:  # Si se está moviendo hacia la izquierda
                    self.animacion_actual = self.animacion_esperando
                else:  # Si se está moviendo hacia la derecha
                    self.animacion_actual = self.animacion_esperando
            else:
                # Si el jugador no se está moviendo, establecer la animación de espera
                if self.last_direction == 'left':
                    self.animacion_actual = [pygame.transform.flip(img, True, False) for img in self.animacion_esperando]
                else:
                    self.animacion_actual = self.animacion_esperando
            self.speed_x = 0  # Detener el movimiento lateral
            
        self.rect.x += self.speed_x
        self.rect.x = max(0, min(self.rect.x, ancho-40 - self.rect.width))

            
        if self.lanzando:
            # Determinar la dirección de la animación de lanzamiento
            if self.last_direction == 'left':  # Si la última dirección fue hacia la izquierda
                self.animacion_lanzando = [pygame.transform.flip(img, True, False) for img in estado_lanzando]
            else:
                self.animacion_lanzando = estado_lanzando

            now = pygame.time.get_ticks()
            cooldown_animacion_lanzando = 30  
            if now - self.update_time > cooldown_animacion_lanzando:
                self.frame_index += 1
                self.update_time = now

                if self.frame_index >= len(self.animacion_lanzando):
                    self.frame_index = 0
                    self.lanzando = False  

                self.image = self.animacion_lanzando[self.frame_index]

        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.2 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

        if self.muriendo:
            now = pygame.time.get_ticks()
            cooldown_animacion_muriendo = 30
            if now - self.update_time > cooldown_animacion_muriendo:
                self.frame_index += 1
                self.update_time = now
                # Asegurar que la animación de muerte se ejecute mirando en la dirección correcta
                if self.last_direction == 'left':  # Si la última dirección fue hacia la izquierda
                    self.animacion_muriendo = [pygame.transform.flip(img, True, False) for img in estado_muriendo]
                else:
                    self.animacion_muriendo = estado_muriendo

                if self.frame_index >= len(self.animacion_muriendo):
                    self.frame_index = 9

                self.image = self.animacion_muriendo[self.frame_index]
                
        if self.rect.y >= 277:
            self.rect.y = 277
            
# Clase del robot
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        
        self.animacion_corriendo = estado_atacando  # Usar la animación de ataque para la animación de correr
        self.animacion_actual_robot = self.animacion_corriendo
        self.frame_index = 0
        self.image = self.animacion_actual_robot[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = random.choice([(60, 60), (900, 60), (900, 470), (60, 470)])
        self.speedx = random.randint(1, 5)
        self.speedy = random.randint(1, 5)
        self.update_time = pygame.time.get_ticks()

    

    def robot_Corriendo(self):
        now = pygame.time.get_ticks()
        cooldown_animacion_robot = 40
        if now - self.update_time > cooldown_animacion_robot:
            self.frame_index += 1
            self.update_time = now

            if self.frame_index >= len(self.animacion_actual_robot):
                self.frame_index = 0

            self.image = self.animacion_actual_robot[self.frame_index]  # Actualiza la imagen aquí
            if self.speedx < 0:
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.robot_Corriendo()  # Llamar al método robot_Corriendo en cada fotograma para actualizar la animación
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0 or self.rect.right > ancho:
            self.speedx = -self.speedx
            if self.speedx < 0:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.top < 0 or self.rect.bottom > alto:
            self.speedy = -self.speedy

# Clase de la sierra
class Saw(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = pygame.image.load("recursos/personajes/heroe/lanzando/Saw.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * escala_saw), int(self.image.get_height() * escala_saw)))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad
        
    def update(self):
        self.rect.x += self.velocidad.x
        self.rect.y += self.velocidad.y
        if self.rect.bottom < 0:
            self.kill()

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
robots_list = pygame.sprite.Group()
saw_list = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()

# Crear jugador y añadirlo al grupo de sprites
player = Player()
player_sprite.add(player)


# Crear robots y añadirlos al grupo de sprites
for _ in range(1):
    robot = Robot()
    all_sprites.add(robot)
    robots_list.add(robot) 

# Puntuación inicial
score = 0
running = True
pygame.mixer.music.play()
main_menu()
#--------------------------------------------- Bucle principal del juego.-----------------------------------------------------------------------_____________________________________________________________________________
while running:
    # Controlar la velocidad de actualización
    clock.tick(60)
    
    # Manejar eventos del teclado y ratón
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.throw()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jump()
        if not player_alive:
            max_score = max(max_score, score)
            if mostrar_game_over(score):
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not player_alive:
                reset_game()        
                
            
                
           
    # Ejecutar animaciones y actualizar todos los sprites
    player.corriendo()
    robot.robot_Corriendo()  
    all_sprites.update()
    player_sprite.update()       
    
    
    
    
    # Detectar colisiones entre robots y sierras
    hits = pygame.sprite.groupcollide(robots_list, saw_list, True, True)
    for hit in hits:
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        explosion_sound.play()
        score += 1
        for _ in range(2):
            robot = Robot()
            robot.robot_Corriendo()
            
            all_sprites.add(robot)
            robots_list.add(robot)
            
    # Detectar colisiones entre el jugador y los robots
    hits = pygame.sprite.spritecollide(player, robots_list, False)
        
    for hit in hits:
        if player_alive:  # Verificar si el jugador está vivo antes de reproducir los sonidos de dolor
            random.choice(dolor_sounds).play()
            player.shield -= 10
            if player.shield < 0:
                for sound in dolor_sounds:
                    sound.stop()  # Detener todos los sonidos de dolor si el jugador muere
                muerte_sound.play()
                player.dead()
                player_alive = False 
        
    # Dibujar la pantalla
    screen.blit(fondofinal, (0, 0))
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    draw_text(screen, str(score), 50, ancho // 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()

# Salir del juego
pygame.quit()