import pygame
import sys

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

class UIManager:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.current_state = "menu"  # Estados: "menu", "game", "game_over", "win"
        
        # Centro da tela (baseado em 800x600)
        self.cx = 400
        self.cy = 300

        # --- BOTÕES DO MENU PRINCIPAL ---
        # Rect(x, y, largura, altura)
        self.btn_start = pygame.Rect(0, 0, 200, 50)
        self.btn_start.center = (self.cx, 250)

        self.btn_music = pygame.Rect(0, 0, 200, 50)
        self.btn_music.center = (self.cx, 320)

        self.btn_sound = pygame.Rect(0, 0, 200, 50)
        self.btn_sound.center = (self.cx, 390)

        self.btn_quit_menu = pygame.Rect(0, 0, 200, 50)
        self.btn_quit_menu.center = (self.cx, 460)

        # --- BOTÕES DE GAME OVER / WIN ---
        self.btn_main_menu = pygame.Rect(0, 0, 200, 50)
        self.btn_main_menu.center = (self.cx, 350)

        self.btn_quit_end = pygame.Rect(0, 0, 200, 50)
        self.btn_quit_end.center = (self.cx, 420)

    def draw(self, screen):
        """Desenha a tela atual baseada no estado."""
        
        if self.current_state == "menu":
            self._draw_menu(screen)
        elif self.current_state == "game_over":
            self._draw_game_over(screen)
        elif self.current_state == "win":
            self._draw_win(screen)
        # Se for "game", a UI não desenha nada (o main desenha o jogo)

    def _draw_button(self, screen, rect, text, color=GRAY):
        """Função auxiliar para desenhar um botão bonito."""
        screen.draw.filled_rect(rect, color)
        screen.draw.rect(rect, WHITE) # Borda
        screen.draw.text(text, center=rect.center, fontsize=30, color=WHITE, shadow=(1,1))

    def _draw_menu(self, screen):
        screen.fill(DARK_GRAY)
        screen.draw.text("ROGUE ADVENTURE", center=(self.cx, 100), fontsize=60, color=RED, shadow=(2,2))
        screen.draw.text("Derrote todos os inimigos!", center=(self.cx, 160), fontsize=30, color=WHITE)

        self._draw_button(screen, self.btn_start, "INICIAR", BLUE)
        
        # Texto dinâmico para Música
        txt_music = "MUSIC: ON" if self.sound_manager.music_enabled else "MUSIC: OFF"
        color_music = GREEN if self.sound_manager.music_enabled else RED
        self._draw_button(screen, self.btn_music, txt_music, color_music)

        # Texto dinâmico para Sons
        txt_sound = "SOUND: ON" if self.sound_manager.sfx_enabled else "SOUND: OFF"
        color_sound = GREEN if self.sound_manager.sfx_enabled else RED
        self._draw_button(screen, self.btn_sound, txt_sound, color_sound)

        self._draw_button(screen, self.btn_quit_menu, "SAIR", GRAY)

    def _draw_game_over(self, screen):
        # Fundo semi-transparente
        screen.draw.filled_rect(pygame.Rect(0, 0, 800, 600), (0, 0, 0)) 
        
        screen.draw.text("GAME OVER", center=(self.cx, 150), fontsize=80, color=RED, shadow=(2,2))
        screen.draw.text("Voce morreu...", center=(self.cx, 220), fontsize=40, color=WHITE)

        self._draw_button(screen, self.btn_main_menu, "MENU PRINCIPAL", BLUE)
        self._draw_button(screen, self.btn_quit_end, "SAIR", GRAY)

    def _draw_win(self, screen):
        screen.draw.filled_rect(pygame.Rect(0, 0, 800, 600), (0, 0, 0)) 
        
        screen.draw.text("YOU WIN!", center=(self.cx, 150), fontsize=80, color=GREEN, shadow=(2,2))
        screen.draw.text("Todos os inimigos derrotados!", center=(self.cx, 220), fontsize=40, color=WHITE)

        self._draw_button(screen, self.btn_main_menu, "MENU PRINCIPAL", BLUE)
        self._draw_button(screen, self.btn_quit_end, "SAIR", GRAY)

    def handle_click(self, pos):
        """Retorna uma ação (string) baseada no clique."""
        x, y = pos

        if self.current_state == "menu":
            if self.btn_start.collidepoint(x, y):
                self.current_state = "game"
                return "reset_game" # Iniciar Jogo
            
            elif self.btn_music.collidepoint(x, y):
                self.sound_manager.music_enabled = not self.sound_manager.music_enabled
                if self.sound_manager.music_enabled:
                    self.sound_manager.play_menu_music() # Toca música do menu se reativar
                else:
                    self.sound_manager.stop_music()

            elif self.btn_sound.collidepoint(x, y):
                self.sound_manager.sfx_enabled = not self.sound_manager.sfx_enabled
            
            elif self.btn_quit_menu.collidepoint(x, y):
                sys.exit()

        elif self.current_state in ["game_over", "win"]:
            if self.btn_main_menu.collidepoint(x, y):
                self.current_state = "menu"
                return "goto_menu" # <--- NOVO: Avisa para tocar música do menu
            
            elif self.btn_quit_end.collidepoint(x, y):
                sys.exit()
        
        return None