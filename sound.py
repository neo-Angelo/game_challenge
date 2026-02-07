from pgzero.builtins import sounds, music

class SoundManager:
    def __init__(self):
        self.sfx_enabled = True
        self.music_enabled = True
        self.music_volume = 0.4 

    def play_player_damage(self):
        if self.sfx_enabled:
            try:
                if hasattr(sounds, 'player_damage'):
                    sounds.player_damage.stop()
                    sounds.player_damage.play()
            except: pass

    def play_enemy_damage(self):
        if self.sfx_enabled:
            try:
                if hasattr(sounds, 'enemy_damage'):
                    sounds.enemy_damage.play()
            except: pass

    
    def play_background_music(self):

        if self.music_enabled:
            try:
                music.play('level') 
                music.set_volume(self.music_volume)
            except: pass

    def play_menu_music(self):

        if self.music_enabled:
            try:
                music.play('menu')
                music.set_volume(self.music_volume)
            except: pass

    def play_gameover_music(self):
 
        if self.music_enabled:
            try:
                music.play('gameover')
                music.set_volume(self.music_volume)
            except: pass

    def play_win_music(self):

        if self.music_enabled:
            try:
                music.play('win')
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