

#Import Modules
import os, pygame, numpy
from classes import Tree, Smasher, Dino, Bear
from pygame.locals import *
from random import randint, uniform
from functions import load_image, load_sound, change_image

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


#function for title screen
def title_screen():
    screen = pygame.display.set_mode((1600, 900), FULLSCREEN)
    pygame.display.set_caption('Ogre vs Dino')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 72)
        text = font.render("Eat the Evil Teddy Bears", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/10)
        background.blit(text, textpos)
        font = pygame.font.Font(None, 36)
        text = font.render("Player1: use mouse/button to make Dino eat bears(+10)", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 15)
        background.blit(text, textpos)
        text = font.render("Player2: use arrows to move Ogre and eat bears(+10)", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 65)
        background.blit(text, textpos)
        text = font.render("Press ESC to QUIT", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 115)
        background.blit(text, textpos)
        text = font.render("Press SPACE to play single player as Dino", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 165)
        background.blit(text, textpos)
        text = font.render("Press any other key to play 2 player", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 215)
        background.blit(text, textpos)
        text = font.render("Ogre launches trees at small cost(-2)", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 265)
        background.blit(text, textpos)
        text = font.render("Dino gets hit by launched trees at greater cost(-10)", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 315)
        background.blit(text, textpos)
        text = font.render("Ten additional bears for each game after the 1st", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 365)
        background.blit(text, textpos)
        text = font.render("In game press ESC to return here", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/5 + 415)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True, True
                elif event.key == pygame.K_SPACE:
                    return False, True
                else:
                    return False, False

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    numbears = 10

#Loop once for each game
    
    while 1:
        
    #Initialize Everything
        period = 0
        numbears += 10
        single_player = True
        playing = True
        done = False
        pygame.init()
        done, single_player = title_screen()
        if done == True:
            return
        screen = pygame.display.set_mode((1600, 900), FULLSCREEN)
        pygame.display.set_caption('Ogre Fever')
        pygame.mouse.set_visible(0)

    #Create The Backgound
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background_image, background_rect = load_image('012.bmp', -1)
        for x in range(0,background.get_width(),background_image.get_width()):
            for y in range(0,background.get_height(),background_image.get_height()):
                background.blit(background_image,(x,y))
    #   background.fill((250, 250, 250))

    #Put Text On The Background, Centered
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Smash the Evil Teddy Bears", 1, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width()/2)
            background.blit(text, textpos)

    #Display The Background
        screen.blit(background, (0, 0))
        pygame.display.flip()
        
    #Global Sprite Groups
        Sprites = pygame.sprite.RenderPlain()
        Bear_sprites = pygame.sprite.RenderPlain()
        Tree_sprites = pygame.sprite.RenderPlain()

    #Prepare Game Objects
        w,h = screen.get_size()
        clock = pygame.time.Clock()
        punch_sound = load_sound('explosion.wav')
        whiff_sound = load_sound('whiff.wav')
        eat_sound = load_sound('eat.wav')
        tree_sound = load_sound('tree.wav')
        dino_hurt_sound = load_sound('dino_hurt.wav')
        smasher = Smasher()
        for trees in range(0, 10):
            Tree_sprites.add(Tree(trees))
        Sprites.add(Tree_sprites)
        for bears in range(0,numbears):
            Bear_sprites.add(Bear())
        Sprites.add(Bear_sprites)
        dino = Dino()
        allsprites = pygame.sprite.RenderPlain((dino, Bear_sprites, smasher, Tree_sprites))
        
    #Main In Game Loop

        while playing:
            clock.tick(60)

            period += 1
            if period == 120:
                smasher.aiv = randint(-1, 1)
                smasher.aih = randint(-1, 1)
                period = 0
                dino.image = change_image('attack n0006.bmp', -1)     
                smasher.image = change_image('looking n0000.bmp', -1)

            for bear in pygame.sprite.spritecollide(smasher, Bear_sprites, 1):
                eat_sound.play()
                smasher.show_score(background, 10)
                smasher.image = change_image('ogre_eat.bmp', -1)

            for tree in pygame.sprite.spritecollide(smasher, Tree_sprites, 0):
                tree.jump()
                if tree.damager == 2:
                    tree_sound.play()
                    smasher.show_score(background, -2)
                    tree.damager -= 1
            for tree in pygame.sprite.spritecollide(dino, Tree_sprites, 0):
                if tree.damager == 1:
                    dino_hurt_sound.play()
                    dino.show_score(background, -10)
                    tree.damager -= 1



        #Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if title_screen():
                            return
                    elif event.key == K_SPACE:
                        for tree in Tree_sprites:
                            tree.jump()
                    elif event.key == K_RIGHT:
                        smasher.hmove += 1
                    elif event.key == K_LEFT:
                        smasher.hmove -= 1
                    elif event.key == K_UP:
                        smasher.vmove -= 1
                    elif event.key == K_DOWN:
                        smasher.vmove += 1
                elif event.type == MOUSEBUTTONDOWN:
                    for bear in pygame.sprite.spritecollide(dino, Bear_sprites, 1):
                        eat_sound.play()
                        if single_player == True:
                            dino.show_score(background, 8)
                        else:
                            dino.show_score(background, 10)
                        dino.image = change_image('dino_eat.bmp', -1)

            # Event polling:
            pressed = pygame.key.get_pressed()
            if pressed[K_LEFT]:
                smasher.hmove -= .5
            if pressed[K_RIGHT]:
                smasher.hmove += .5
            if pressed[K_DOWN]:
                smasher.vmove += .5
            if pressed[K_UP]:
                smasher.vmove -= .5

    #AI for smasher in single player mode
            if single_player == True:
                smasher.vmove += smasher.aiv
                smasher.hmove += smasher.aih
                
            allsprites.update()

        #Draw Everything
            screen.blit(background, (0, 0))
            allsprites.draw(screen)
            pygame.display.flip()
            
        #Do you win?
            if not pygame.sprite.Group(Bear_sprites):
                if pygame.font:
                    font = pygame.font.Font(None, 196)
                    text = font.render("Ogre score: " + str(smasher.score), 1, (200, 200, 200))
                    textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/3)
                    background.blit(text, textpos)
                    screen.blit(background, (0, 0))
                    font = pygame.font.Font(None, 196)
                    text = font.render("Dino score: " + str(dino.score), 1, (200, 200, 200))
                    textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/2)
                    background.blit(text, textpos)
                    screen.blit(background, (0, 0))
                    font = pygame.font.Font(None, 36)
                    text = font.render("ESC: quit, Any other key: play again", 1, (200, 200, 200))
                    textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/1.5)
                    background.blit(text, textpos)
                    screen.blit(background, (0, 0))
                    allsprites.draw(screen)
                    pygame.display.flip()
                while not done:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                return
                            playing = False
                            done = True
                        

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
