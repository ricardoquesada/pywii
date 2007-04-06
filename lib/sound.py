import data
import pygame
pygame.mixer.pre_init(44100, -16, False, 1024)

def buildSounds():
    ret = []
    for n in range(12*5):
        filename = data.filepath("sonidos/tonos%03d.ogg"%n)
        ret.append(pygame.mixer.Sound(filename))
    return ret

sounds = buildSounds()
def playSound(n, vol):
    n = int(n*len(sounds))%len(sounds)
    chan = pygame.mixer.find_channel(True)
    chan.play(sounds[n])
    # podriamos Jugar con el stereo!
    chan.set_volume(vol)
