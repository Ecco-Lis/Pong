import pygame
import random

# Colores personalizados (en formato RGB)
COLOR_OBJETOS = (255, 0, 0)   # Rojo
COLOR_FONDO = (100, 100, 100)  # Gris

# Dimensiones de la ventana del juego
ANCHO = 600
ALTO = 400

# Dimensiones de las paletas
ANCHO_PALA = 10
ALTO_PALA = 80

class Pong:
    def __init__(self):
        """
        Inicializa la instancia del juego Pong.
        Configura la pantalla, la pelota, las paletas y el reloj del juego.
        """
        pygame.init() #Inicializa la biblioteca Pygame.
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Pong")#Configura la pantalla del juego con el tamaño especificado y le da un título

        self.reloj = pygame.time.Clock()
        
        # Inicializar la pelota en el centro y establecer su velocidad inicial de forma aleatoria
        self.pelota = pygame.Rect(ANCHO // 2 - 10, ALTO // 2 - 10, 20, 20)
        self.velocidad_pelota = [random.choice((1, -1)) * 5, random.choice((1, -1)) * 5]

        # Inicializar las paletas en posiciones iniciales
        self.jugador1 = pygame.Rect(10, ALTO // 2 - ALTO_PALA // 2, ANCHO_PALA, ALTO_PALA)
        self.jugador2 = pygame.Rect(ANCHO - 20, ALTO // 2 - ALTO_PALA // 2, ANCHO_PALA, ALTO_PALA)

        # Contadores de puntos para cada jugador
        self.puntos_jugador1 = 0 #Estos atributos se utilizan para llevar  un
        self.puntos_jugador2 = 0 #registro de los puntos de cada jugador
        """  
        self.reloj: Se crea un objeto de reloj para controlar la velocidad de fotogramas.
        self.pelota: Se crea un objeto rectangular (la pelota) en el centro de la pantalla.
        self.velocidad_pelota: Se establece una velocidad inicial aleatoria para la pelota.
        self.jugador1 y self.jugador2: Se crean dos objetos rectangulares para representar las paletas de los jugadores.
        
        """
    def mover_pelota(self):
        """
        Mueve la pelota y controla su rebote en los bordes y en las paletas.
        """
        self.pelota.x += self.velocidad_pelota[0] #Actualiza la posición de la pelota en cada fotograma
        self.pelota.y += self.velocidad_pelota[1] # según su velocidad actual
        
        #Rebote en los bordes superior e inferior:
        if self.pelota.top <= 0 or self.pelota.bottom >= ALTO:
            self.velocidad_pelota[1] = -self.velocidad_pelota[1]
        """Verifica si la pelota ha alcanzado los bordes superior o inferior de la pantalla y, en caso afirmativo,
           invierte su velocidad vertical para que rebote
        """
        # Rebotar la pelota en las paletas y contar puntos
        if self.pelota.colliderect(self.jugador1):
            self.velocidad_pelota[0] = abs(self.velocidad_pelota[0])  # Usamos abs para asegurarnos de que la velocidad sea siempre positiva
            self.puntos_jugador1 += 1
        elif self.pelota.colliderect(self.jugador2):
            self.velocidad_pelota[0] = -abs(self.velocidad_pelota[0])  # Usamos abs para asegurarnos de que la velocidad sea siempre negativa
            self.puntos_jugador2 += 1
        """Verifica si la pelota colisiona con una de las paletas de los jugadores. Si colisiona con la paleta del jugador 1,
           cambia la dirección de la pelota hacia la derecha y aumenta el puntaje del jugador 1. Si colisiona con la paleta del jugador 2,
           cambia la dirección de la pelota hacia la izquierda y aumenta el puntaje del jugador 2
        """
        # Reiniciar la pelota en el centro si sale de la pantalla
        if self.pelota.left < 0 or self.pelota.right > ANCHO:
            self.pelota.x = ANCHO // 2 - 10
            self.pelota.y = ALTO // 2 - 10
            self.velocidad_pelota = [random.choice((1, -1)) * 5, random.choice((1, -1)) * 5]
        """Verifica si la pelota ha salido de la pantalla por los lados izquierdo o derecho. Si es así,
           coloca la pelota en el centro de la pantalla y le asigna una nueva velocidad inicial aleatoria
        """
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
                    """Dentro del bucle, se verifica si se ha producido un evento de salida del 
           (como cerrar la ventana xD) y, en ese caso, se sale del bucle principa
        """

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
                """Se comprueba si se han presionado las teclas correspondientes para mover las paletas
                   de los jugadores hacia arriba (K_w y K_UP) o hacia abajo (K_s y K_DOWN). Se asegura de que las paletas no salgan de la pantalla
              """

            self.mover_pelota()

            # Dibujar la pantalla y los objetos
            pygame.draw.rect(self.pantalla, COLOR_FONDO, ((0, 0), (ANCHO, ALTO)))
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, self.jugador1)
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, self.jugador2)
            pygame.draw.ellipse(self.pantalla, COLOR_OBJETOS, self.pelota)
            """Se dibuja la pantalla, las paletas y la pelota utilizando los colores definidos anteriormente"""
            # Dibujar la red en el centro
            pygame.draw.line(self.pantalla, COLOR_OBJETOS, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

            # Dibujar el cuadro de los marcadores
            pygame.draw.rect(self.pantalla, COLOR_OBJETOS, (ANCHO // 2 - 30, 10, 60, 40))#cambiar el  tamaño del marcador si sube  arriba de 20*
            """Se dibuja una línea en el centro de la pantalla para representar la red y un cuadro para los marcadores de puntos. """

            # Mostrar los puntos en pantalla dentro del cuadro
            font = pygame.font.Font(None, 36)
            puntos_texto = font.render(f"{self.puntos_jugador1} - {self.puntos_jugador2}", True, COLOR_FONDO)
            """Se crea un objeto font que representa la fuente de texto que se utilizará para mostrar los puntos y los nombres de los jugadores. None significa que se usará la fuente predeterminada, y 36 es el tamaño de la fuente en puntos
             Luego, se utiliza el método render de la fuente para crear un objeto puntos_texto que contiene el texto de los puntos
             El texto se forma concatenando los puntos de self.puntos_jugador1 y self.puntos_jugador2, separados por un guion. El parámetro True se refiere a la suavización de bordes del texto, y COLOR_FONDO se utiliza como color del texto
         """
            self.pantalla.blit(puntos_texto, (ANCHO // 2 - puntos_texto.get_width() // 2, 20))
            """Utilizando el método blit de la pantalla (self.pantalla), se coloca el texto de los puntos en la pantalla. puntos_texto contiene el texto a mostrar.
            La posición (ANCHO // 2 - puntos_texto.get_width() // 2, 20) se calcula para centrar horizontalmente el texto de los puntos en la parte superior de la pantalla. ANCHO // 2 es la mitad del ancho de la pantalla, y puntos_texto.get_width() 
             // 2 es la mitad del ancho del texto, lo que asegura que el texto esté centrado
           """

            # Mostrar nombres de los jugadores en rojo
            nombre_jugador1 = font.render("Player 1", True, COLOR_OBJETOS)
            self.pantalla.blit(nombre_jugador1, (20, ALTO - 30))
            """Se crea un objeto nombre_jugador1 que contiene el texto "Player 1". Este texto se renderiza utilizando la misma fuente y se aplica un color rojo (COLOR_OBJETOS)
            Luego, se coloca el texto en la pantalla en la posición (20, ALTO - 30) Esto coloca el nombre del jugador 1 en la parte inferior izquierda de la pantalla
        """
            nombre_jugador2 = font.render("Player 2", True, COLOR_OBJETOS)
            self.pantalla.blit(nombre_jugador2, (ANCHO - 120, ALTO - 30))
            """Se crea un objeto nombre_jugador2 que contiene el texto "Player 2" y se renderiza de manera similar al nombre del jugador 1.
               El texto se coloca en la pantalla en la posición (ANCHO - 120, ALTO - 30). Esto coloca el nombre del jugador 2 en la parte inferior derecha de la pantalla
        """
            

            pygame.display.flip()# Se actualiza la pantalla para mostrar todos los elementos dibujados
            

            self.reloj.tick(60)#Se utiliza el objeto de reloj para limitar la velocidad de fotogramas del juego a 60 fotogramas por segundo

        pygame.quit()
        """Cuando el bucle principal se sale, se llama a pygame.quit() para cerrar la biblioteca Pygame y terminar el juego
        """

if __name__ == '__main__':
    juego = Pong()
    juego.jugar()
"""Esta sección del código verifica si el script se está ejecutando directamente 
 (no importado como módulo) y, en ese caso, crea una instancia de la clase Pong y llama al método jugar() 
 para iniciar el juego""" #  tenia que hacerlo Detallarlo si funciona  , se  guarda mejor en mi mente  el tener que explicarlo >w<(ando viendo como hacerle para que salte   y pida nombre de player 1 y player 2 @-@)