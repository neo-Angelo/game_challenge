from pgzero.builtins import sounds, music

class SoundManager:
    def __init__(self):
        self.sfx_enabled = True
        self.music_enabled = True
        self.music_volume = 0.4 

    # --- EFEITOS SONOROS (SFX) ---
    def play_player_damage(self):
        if self.sfx_enabled and hasattr(sounds, 'player_damage'):
            sounds.player_damage.stop()
            sounds.player_damage.play()

    def play_enemy_damage(self):
        if self.sfx_enabled and hasattr(sounds, 'enemy_damage'):
            sounds.enemy_damage.play()

    # --- MÚSICAS (BGM) ---
    
    def play_background_music(self):
        """Música da fase (Jogo)"""
        if self.music_enabled:
            try:
                music.play('level') # level.mp3
                music.set_volume(self.music_volume)
            except: pass

    def play_menu_music(self):
        """Música do Menu Principal"""
        if self.music_enabled:
            try:
                music.play('menu') # menu.mp3
                music.set_volume(self.music_volume)
            except: pass

    def play_gameover_music(self):
        """Música de Game Over"""
        if self.music_enabled:
            try:
                music.play('gameover') # gameover.mp3
                music.set_volume(self.music_volume)
            except: pass

    def stop_music(self):
        music.stop()

    def toggle_sound(self):
        self.sfx_enabled = not self.sfx_enabled
        if not self.sfx_enabled:
            music.pause()
        else:
            music.unpause()
        return self.sfx_enabled