from pygame import mixer


def init_music():
    mixer.init()

    mixer.music.load('music/background.mp3')
    mixer.music.set_volume(0.6)
    mixer.music.play(-1)
    bullet_sound = mixer.Sound('music/laser.wav')
    explosion_sound = mixer.Sound('music/explosion.wav')

    return bullet_sound, explosion_sound

