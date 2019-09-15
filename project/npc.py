from lib.utools import *

NPC_START_NUM = 121
NPC_IMG = crop_images(load_image("img/npc.png"), NPC_START_NUM, pygame.Rect(0, 0, BLOCK_UNIT*2, BLOCK_UNIT))