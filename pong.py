import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes pour la taille de l'écran
LARGEUR_ECRAN, HAUTEUR_ECRAN = 858, 525

# Création de l'écran
écran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

# Définition des constantes pour les raquettes et la balle
LARGEUR_RAQUETTE, HAUTEUR_RAQUETTE = 15, 80
DIMENSION_BALLE = 15
VITESSE_RAQUETTE = 2
VITESSE_BALLE = 1
nombre_de_rebond_debut = random.randint(8, 10)  # Corrigé : "rebond" est au singulier
nombre_de_rebond = nombre_de_rebond_debut  # Corrigé : "rebond" est au singulier
nombre_de_rebond_additionnel_max = 8  # Corrigé : "rebond" est au singulier
nombre_de_rebond_additionnel_min = 3  # Corrigé : "rebond" est au singulier
nombre_de_rebond_additionnel = random.randint(nombre_de_rebond_additionnel_min, nombre_de_rebond_additionnel_max)
verritable_nombre_de_rebond = 0
# Création des raquettes et de la balle
raquette1 = pygame.Rect(0, HAUTEUR_ECRAN // 2, LARGEUR_RAQUETTE, HAUTEUR_RAQUETTE)
raquette2 = pygame.Rect(LARGEUR_ECRAN - LARGEUR_RAQUETTE, HAUTEUR_ECRAN // 2, LARGEUR_RAQUETTE, HAUTEUR_RAQUETTE)
balle = pygame.Rect(LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2, DIMENSION_BALLE, DIMENSION_BALLE)

# Définition de la direction de la balle
dx_balle = VITESSE_BALLE
dy_balle = VITESSE_BALLE

# Initialisation des compteurs de points
score_joueur1 = 0
score_joueur2 = 0

# Création d'une police pour afficher le texte des points et de la vitesse
font = pygame.font.Font(None, 36)

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    nombre_de_rebond_additionnel = random.randint(nombre_de_rebond_additionnel_min, nombre_de_rebond_additionnel_max)

    # Mouvement des raquettes
    touches = pygame.key.get_pressed()
    if touches[pygame.K_z] and raquette1.top > 0:
        raquette1.move_ip(0, -VITESSE_RAQUETTE)
    if touches[pygame.K_s] and raquette1.bottom < HAUTEUR_ECRAN:
        raquette1.move_ip(0, VITESSE_RAQUETTE)
    if touches[pygame.K_UP] and raquette2.top > 0:
        raquette2.move_ip(0, -VITESSE_RAQUETTE)
    if touches[pygame.K_DOWN] and raquette2.bottom < HAUTEUR_ECRAN:
        raquette2.move_ip(0, VITESSE_RAQUETTE)
    if touches[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Mouvement de la balle
    balle.move_ip(dx_balle, dy_balle)

    # Collision de la balle avec les ligne blanc en haut et en bas de l'écran
    if balle.top <= 0 or balle.bottom >= HAUTEUR_ECRAN:
        dy_balle *= -1
        # lance le song ping_pong_8bit_beeep.ogg
        pygame.mixer.music.load('ping_pong_8bit_beeep.ogg')
        pygame.mixer.music.play(0)

    # Si la balle sort de l'écran, réinitialiser et ajouter un point au joueur opposé
    if balle.left < 0:
        balle.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)
        dx_balle *= -1
        score_joueur2 += 1
        #ajoute un nombre de rebond additionnel entre 1 et 5 random
        nombre_de_rebond = nombre_de_rebond_debut
        # lance le song ping_pong_8bit_plop.ogg
        pygame.mixer.music.load('ping_pong_8bit_plop.ogg')
        pygame.mixer.music.play(0)
    elif balle.right > LARGEUR_ECRAN:
        balle.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)
        dx_balle *= -1
        score_joueur1 += 1
        nombre_de_rebond = nombre_de_rebond_debut
        # lance le song ping_pong_8bit_plop.ogg
        pygame.mixer.music.load('ping_pong_8bit_plop.ogg')
        pygame.mixer.music.play(0)

    # Collision de la balle avec les raquettes
    if balle.colliderect(raquette1) or balle.colliderect(raquette2):
        dx_balle *= -1
        nombre_de_rebond += nombre_de_rebond_additionnel
        verritable_nombre_de_rebond += 1
        # lance le song ping_pong_8bit_beeep.ogg
        pygame.mixer.music.load('ping_pong_8bit_beeep.ogg')
        pygame.mixer.music.play(0)

    # Calcul de la vitesse de la balle en fonction du nombre de rebonds
    vitesse_balle = VITESSE_BALLE + nombre_de_rebond * 0.1  # Corrigé : "vitesse_balle" au lieu de "vitesse_texte"

    # Dessin de l'écran, des raquettes, de la balle et des compteurs de points
    écran.fill((0, 0, 0))
    pygame.draw.rect(écran, (255, 255, 255), raquette1)
    pygame.draw.rect(écran, (255, 255, 255), raquette2)
    pygame.draw.ellipse(écran, (255, 255, 255), balle)

# Utilisation d'une police fixe pour le texte des scores
    font_scores = pygame.font.Font("minecraft_font.ttf", 64)

# Affichage des scores avec la nouvelle police
    score_texte = font_scores.render(f"{score_joueur1}    {score_joueur2}", True, (255, 255, 255))
    écran.blit(score_texte, (LARGEUR_ECRAN // 2 - score_texte.get_width() // 2, 10))


    #affichage du de deux ligne blanc en bas et en haut de l'écran
    pygame.draw.line(écran, (255, 255, 255), (0, 0), (LARGEUR_ECRAN, 0), 10)
    pygame.draw.line(écran, (255, 255, 255), (0, HAUTEUR_ECRAN), (LARGEUR_ECRAN, HAUTEUR_ECRAN), 10)

    # Affichage de la vitesse de la balle en bas de l'écran
    #vitesse_texte = font.render(f"Vitesse : {vitesse_balle:.1f}", True, (255, 255, 255))
    #écran.blit(vitesse_texte, (LARGEUR_ECRAN // 2 - vitesse_texte.get_width() // 2, HAUTEUR_ECRAN - 40))
    # Affichage du nombre véritable de rebond en bas de l'écran au dessus de la vitesse
    #nombre_rebond_texte = font.render(f"Nombre de rebond : {verritable_nombre_de_rebond}", True, (255, 255, 255))
    #écran.blit(nombre_rebond_texte, (LARGEUR_ECRAN // 2 - nombre_rebond_texte.get_width() // 2, HAUTEUR_ECRAN - 80))

# Dessin d'une ligne discontinue au milieu de l'écran
    espacement = 10  # Espacement entre chaque segment de la ligne
    for y in range(0, HAUTEUR_ECRAN, espacement*2):
        pygame.draw.line(écran, (255, 255, 255), (LARGEUR_ECRAN // 2, y), (LARGEUR_ECRAN // 2, y + espacement), 5)



    pygame.display.flip()

    # Limite le taux de rafraîchissement à 60 images par seconde
    pygame.time.Clock().tick(vitesse_balle * 60)
