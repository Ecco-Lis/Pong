import pygame
import random
import sys

# Colores personalizados (en formato RGB)
COLOR_OBJETOS = (255, 0, 0)   # Rojo
COLOR_FONDO = (100, 100, 100)  # Gris

# Dimensiones de la ventana del juego
ANCHO = 600
ALTO = 400

# Dimensiones de las paletas
ANCHO_PALA = 10
ALTO_PALA = 80

juego_en_curso = False

class Pong:
    def __init__(self):
        """
        Inicializa la instancia del juego Pong.
        Configura la pantalla, la pelota, las paletas y el reloj del juego.
        """
        pygame.init()  # Inicializa la biblioteca Pygame.
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Pong")  # Configura la pantalla del juego con el tamaño especificado y le da un título

        self.reloj = pygame.time.Clock()
        # Inicializar la pelota en el centro y establecer su velocidad inicial de forma aleatoria
        self.pelota = pygame.Rect(ANCHO // 2 - 10, ALTO // 2 - 10, 20, 20)
        self.velocidad_pelota = [random.choice((1, -1)) * 5, random.choice((1, -1)) * 5]
        self.nombre_jugador1 = ""
        self.nombre_jugador2 = ""
        # Inicializar las paletas en posiciones iniciales
        self.jugador1 = pygame.Rect(10, ALTO // 2 - ALTO_PALA // 2, ANCHO_PALA, ALTO_PALA)
        self.jugador2 = pygame.Rect(ANCHO - 20, ALTO // 2 - ALTO_PALA // 2, ANCHO_PALA, ALTO_PALA)
        # Contadores de puntos para cada jugador
        self.puntos_jugador1 = 0
        self.puntos_jugador2 = 0

    def mover_pelota(self):
        """
        Mueve la pelota y controla su rebote en los bordes y en las paletas.
        """
        self.pelota.x += self.velocidad_pelota[0] # Actualiza la posición de la pelota en cada fotograma
        self.pelota.y += self.velocidad_pelota[1] # según su velocidad actual 

        # Rebote en los bordes superior e inferior:
        if self.pelota.top <= 0 or self.pelota.bottom >= ALTO:
            self.velocidad_pelota[1] = -self.velocidad_pelota[1]
        """
        Verifica si la pelota ha alcanzado los bordes superior o inferior de la pantalla y, en caso afirmativo,
        invierte su velocidad vertical para que rebote.
        """
        
        # Verificar colisión con la paleta del jugador 1
        if self.pelota.colliderect(self.jugador1):
            if self.velocidad_pelota[0] < 0:
                self.velocidad_pelota[0] = -self.velocidad_pelota[0]
                self.puntos_jugador1 += 1
            else:
                self.velocidad_pelota[1] = -self.velocidad_pelota[1]

        # Verificar colisión con la paleta del jugador 2
        if self.pelota.colliderect(self.jugador2):
            if self.velocidad_pelota[0] > 0:
                self.velocidad_pelota[0] = -self.velocidad_pelota[0]
                self.puntos_jugador2 += 1
            else:
                self.velocidad_pelota[1] = -self.velocidad_pelota[1]

        # Reiniciar la pelota en el centro si sale de la pantalla
        if self.pelota.left < 0 or self.pelota.right > ANCHO:
            self.pelota.x = ANCHO // 2 - 10
            self.pelota.y = ALTO // 2 - 10
            self.velocidad_pelota = [random.choice((1, -1)) * 5, random.choice((1, -1)) * 5]

    def jugar(self):
        """
        Función principal que ejecuta el juego Pong.
        Controla el movimiento de las paletas de los jugadores y actualiza la pantalla.
        """
        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    salir = True

            teclas = pygame.key.get_pressed()
            # Control de movimiento para el jugador 1 (izquierda)
            if teclas[pygame.K_w] and self.jugador1.top > 0:
                self.jugador1.y -= 5
            if teclas[pygame.K_s] and self.jugador1.bottom < ALTO:
                self.jugador1.y += 5

            # Control de movimiento para el jugador 2 (derecha)
            if teclas[pygame.K_UP] and self.jugador2.top > 0:
                self.jugador2.y -= 5
            if teclas[pygame.K_DOWN] and self.jugador2.bottom < ALTO:
                self.jugador2.y += 5

            self.mover_pelota()

            # Dibujar la pantalla y los objetos
            pygame.draw.rect(self.pantalla, COLOR_FONDO, ((0, 0), (ANCHO, ALTO)))
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, self.jugador1)
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, self.jugador2)
            pygame.draw.ellipse(self.pantalla, COLOR_OBJETOS, self.pelota)

            # Dibujar la red en el centro
            pygame.draw.line(self.pantalla, COLOR_OBJETOS, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

            # Dibujar el cuadro de los marcadores
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, (ANCHO // 2 - 30, 10, 60, 40))

            # Mostrar los puntos en pantalla dentro del cuadro
            font = pygame.font.Font(None, 36)
            puntos_texto = font.render(f"{self.puntos_jugador1} - {self.puntos_jugador2}", True, COLOR_FONDO)
            self.pantalla.blit(puntos_texto, (ANCHO // 2 - puntos_texto.get_width() // 2, 20))

            # Mostrar nombres de los jugadores en rojo
            nombre_jugador1 = font.render(self.nombre_jugador1, True, COLOR_OBJETOS)
            self.pantalla.blit(nombre_jugador1, (20, ALTO - 30))
            nombre_jugador2 = font.render(self.nombre_jugador2, True, COLOR_OBJETOS)
            self.pantalla.blit(nombre_jugador2, (ANCHO - 120, ALTO - 30))

            pygame.display.flip()
            self.reloj.tick(60)

            # Verificar si hay un ganador
            if self.puntos_jugador1 >= 30 or self.puntos_jugador2 >= 30:
                self.mostrar_ganador()
                salir = True

    def mostrar_ganador(self):
        """
        Muestra al ganador en pantalla y permite volver al inicio del juego.
        """
        pantalla_ganador = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("¡Tenemos un ganador!")
        font = pygame.font.Font(None, 48)

        if self.puntos_jugador1 >= 30:
            mensaje = f"{self.nombre_jugador1} es el ganador!"
        else:
            mensaje = f"{self.nombre_jugador2} es el ganador!"

        texto_ganador = font.render(mensaje, True, COLOR_OBJETOS)
        boton_rect = pygame.Rect(ANCHO // 2 - 50, ALTO // 2 + 50, 100, 40)
        color_boton = pygame.Color('dodgerblue2')

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN and boton_rect.collidepoint(evento.pos):
                    # Volver al inicio del juego
                    self.__init__()
                    self.nombre_jugador1 = ""
                    self.nombre_jugador2 = ""
                    pygame.display.set_caption("Ingresa los nombres de los jugadores")  # Restaurar el título de la ventana
                    return

            pantalla_ganador.fill(COLOR_FONDO)
            pantalla_ganador.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2 - texto_ganador.get_height() // 2))
            pygame.draw.rect(pantalla_ganador, color_boton, boton_rect)
            texto_boton = font.render("Play Again", True, COLOR_OBJETOS)
            pantalla_ganador.blit(texto_boton, (boton_rect.centerx - texto_boton.get_width() // 2, boton_rect.centery - texto_boton.get_height() // 2))
            pygame.display.flip()

if __name__ == '__main__':
    juego = Pong()
    juego_en_curso = True

    # Ventana de ingreso de nombres de jugadores
    pygame.init()
    pantalla_nombre = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ingresa los nombres de los jugadores")
    reloj = pygame.time.Clock()

    input_rect_jugador1 = pygame.Rect(150, 150, 200, 32)
    input_rect_jugador2 = pygame.Rect(150, 250, 200, 32)

    font = pygame.font.Font(None, 32)
    color_input = pygame.Color('lightskyblue3')
    color_input_activado = pygame.Color('dodgerblue2')
    color_texto = pygame.Color('black')

    jugador1_activo = False
    jugador2_activo = False

    texto_jugador1 = ''
    texto_jugador2 = ''

    boton_aceptar_rect = pygame.Rect(250, 300, 100, 50)
    color_boton = pygame.Color('dodgerblue2')
    color_boton_hover = pygame.Color('lightskyblue3')
    texto_boton = font.render("Aceptar", True, color_texto)

    while juego_en_curso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_rect_jugador1.collidepoint(evento.pos):
                    jugador1_activo = not jugador1_activo
                else:
                    jugador1_activo = False
                if input_rect_jugador2.collidepoint(evento.pos):
                    jugador2_activo = not jugador2_activo
                else:
                    jugador2_activo = False

                if boton_aceptar_rect.collidepoint(evento.pos):
                    juego.nombre_jugador1 = texto_jugador1
                    juego.nombre_jugador2 = texto_jugador2
                    pygame.display.set_caption("Pong")  # Restaurar el título de la ventana del juego
                    juego.jugar()

            if evento.type == pygame.KEYDOWN:
                if jugador1_activo:
                    if evento.key == pygame.K_RETURN:
                        juego.nombre_jugador1 = texto_jugador1
                        jugador1_activo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_jugador1 = texto_jugador1[:-1]
                    else:
                        texto_jugador1 += evento.unicode
                if jugador2_activo:
                    if evento.key == pygame.K_RETURN:
                        juego.nombre_jugador2 = texto_jugador2
                        jugador2_activo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_jugador2 = texto_jugador2[:-1]
                    else:
                        texto_jugador2 += evento.unicode

        pantalla_nombre.fill((255, 255, 255))
        input_surface_jugador1 = font.render(texto_jugador1, True, color_texto)
        input_surface_jugador2 = font.render(texto_jugador2, True, color_texto)
        width_jugador1 = max(200, input_surface_jugador1.get_width() + 10)
        input_rect_jugador1.w = width_jugador1
        pantalla_nombre.blit(input_surface_jugador1, (input_rect_jugador1.x + 5, input_rect_jugador1.y + 5))
        pygame.draw.rect(pantalla_nombre, color_input_activado if jugador1_activo else color_input, input_rect_jugador1, 2)
        width_jugador2 = max(200, input_surface_jugador2.get_width() + 10)
        input_rect_jugador2.w = width_jugador2
        pantalla_nombre.blit(input_surface_jugador2, (input_rect_jugador2.x + 5, input_rect_jugador2.y + 5))
        pygame.draw.rect(pantalla_nombre, color_input_activado if jugador2_activo else color_input, input_rect_jugador2, 2)

        pygame.draw.rect(pantalla_nombre, color_boton_hover if boton_aceptar_rect.collidepoint(pygame.mouse.get_pos()) else color_boton, boton_aceptar_rect)
        pantalla_nombre.blit(texto_boton, (boton_aceptar_rect.centerx - texto_boton.get_width() // 2, boton_aceptar_rect.centery - texto_boton.get_height() // 2))
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()
