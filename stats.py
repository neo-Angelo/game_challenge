
class PlayerStats:
    def __init__(self, max_hp=5):
        self.max_hp = max_hp
        self.current_hp = max_hp
        
        # Posição inicial da HUD na tela
        self.start_x = 10
        self.start_y = 10
        # Espaçamento entre os corações
        self.spacing = 25 

    def take_damage(self, amount):
        """Reduz a vida do jogador. Retorna True se morreu."""
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0
            
        print(f"Dano recebido! Vida restante: {self.current_hp}/{self.max_hp}")
        
        return self.current_hp <= 0

    def heal(self, amount):
        """Cura o jogador sem passar do máximo."""
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def draw(self, screen, images):
        """Desenha os corações na tela (HUD)."""
        # Como é HUD, desenhamos em posição fixa da TELA, ignorando a câmera.
        
        for i in range(self.max_hp):
            # Calcula posição X de cada coração
            pos_x = self.start_x + (i * self.spacing)
            pos_y = self.start_y
            
            # Se o índice for menor que a vida atual, desenha coração cheio
            # Ex: HP=3. Indices 0, 1, 2 são Cheios. Indices 3, 4 são Vazios.
            if i < self.current_hp:
                screen.blit(images.heart, (pos_x, pos_y))
            else:
                screen.blit(images.background, (pos_x, pos_y))