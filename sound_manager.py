from PPlay.sound import Sound
import os

class SoundManager:
    def __init__(self):
        # Músicas de fundo
        self.menu_music = Sound("sons/music/menu_theme.ogg")
        self.gameplay_music = Sound("sons/music/gameplay_theme.ogg")
        
        # Configurar músicas para loop
        self.menu_music.set_repeat(True)
        self.gameplay_music.set_repeat(True)
        
        # Efeitos sonoros do player
        self.sword_attack_sound = Sound("sons/sfx/player/sword_attack.ogg")
        self.game_over_sound = Sound("sons/sfx/player/game_over.wav")
        self.player_hurt_sound = Sound("sons/sfx/player/player_hurt.wav")
        self.player_levelup_sound = Sound("sons/sfx/player/player_levelup.wav")
        
        # Efeitos sonoros dos inimigos
        self.bat_death_sound = Sound("sons/sfx/enemies/bat_death.wav")
        self.bat_hurt_sound = Sound("sons/sfx/enemies/bat_hurt.wav")
        
        # Efeitos sonoros de UI
        self.botao_click_sound = Sound("sons/sfx/ui/botao_click.wav")
        self.botao_hover_sound = Sound("sons/sfx/ui/botao_hover.wav")
        self.atributo_up_sound = Sound("sons/sfx/ui/atributo_up.wav")
        self.atributo_confirm_sound = Sound("sons/sfx/ui/atributo_confirm.wav")
        
        # Volume padrão
        self.set_music_volume(30)
        self.set_sfx_volume(30)
        self.set_ui_volume(70)
        
        self.current_music = None
        
    def set_music_volume(self, volume):
        """Define o volume das músicas de fundo"""
        self.menu_music.set_volume(volume)
        self.gameplay_music.set_volume(volume)
        
    def set_sfx_volume(self, volume):
        """Define o volume dos efeitos sonoros"""
        self.sword_attack_sound.set_volume(volume)
        self.game_over_sound.set_volume(volume)
        self.bat_death_sound.set_volume(volume)
        self.bat_hurt_sound.set_volume(volume)
        self.player_hurt_sound.set_volume(volume)
        self.player_levelup_sound.set_volume(volume)
        
    def set_ui_volume(self, volume):
        self.botao_click_sound.set_volume(volume)
        self.botao_hover_sound.set_volume(volume)
        self.atributo_up_sound.set_volume(volume)
        self.atributo_confirm_sound.set_volume(volume)

    def play_menu_music(self):
        """Toca a música do menu"""
        if self.current_music != "menu":
            self.stop_all_music()
            self.menu_music.play()
            self.current_music = "menu"
            
    def play_gameplay_music(self):
        """Toca a música do gameplay"""
        if self.current_music != "gameplay":
            self.stop_all_music()
            self.gameplay_music.play()
            self.current_music = "gameplay"
            
    def stop_gameplay_music(self):
        self.gameplay_music.stop()        
    
    def stop_all_music(self):
        """Para todas as músicas"""
        self.menu_music.stop()
        self.gameplay_music.stop()
        self.current_music = None
        
    def play_sword_attack(self):
        """Toca o som de ataque da espada"""
        self.sword_attack_sound.play()
        
    def play_game_over(self):
        """Toca o som de game over"""
        self.game_over_sound.play()
        
    def play_bat_death(self):
        """Toca o som de morte do morcego"""
        self.bat_death_sound.play()
        
    def play_bat_hurt(self):
        """Toca o som de dano do morcego"""
        self.bat_hurt_sound.play() 

    def play_botao_click(self):
        self.botao_click_sound.play()

    def play_botao_hover(self):
        self.botao_hover_sound.play()

    def play_atributo_up(self):
        self.atributo_up_sound.play()

    def play_atributo_confirm(self):
        self.atributo_confirm_sound.play() 

    def play_player_hurt(self):
        self.player_hurt_sound.play()

    def play_player_levelup(self):
        self.player_levelup_sound.play() 