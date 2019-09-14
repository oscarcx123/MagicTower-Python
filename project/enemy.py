from lib.utools import *

# --- Monster Data START ---

MONSTER_DATA = {
	"greenSlime": {"name":"绿豆糕","hp":50,"atk":14,"def":1,"money":1,"experience":0,"point":0,"special":0},
	"redSlime": {"name":"红豆沙","hp":60,"atk":15,"def":2,"money":1,"experience":0,"point":0,"special":0,"value":10},
	"blackSlime": {"name":"龟苓膏","hp":100,"atk":25,"def":3,"money":2,"experience":0,"point":0,"special":0},
	"slimelord": {"name":"冰皮月饼","hp":500,"atk":80,"def":18,"money":10,"experience":0,"point":0,"special":0},
	"bat": {"name":"小菱角","hp":48,"atk":24,"def":0,"money":1,"experience":0,"point":0,"special":4},
	"bigBat": {"name":"大菱角","hp":84,"atk":42,"def":2,"money":2,"experience":0,"point":0,"special":4},
	"redBat": {"name":"红菱角","hp":188,"atk":88,"def":8,"money":4,"experience":0,"point":0,"special":5},
	"vampire": {"name":"芝麻糊","hp":400,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":10},
	"skeleton": {"name":"冰棍","hp":124,"atk":24,"def":4,"money":2,"experience":0,"point":0,"special":0},
	"skeletonSoilder": {"name":"老冰棍","hp":168,"atk":38,"def":12,"money":2,"experience":0,"point":0,"special":0},
	"skeletonCaptain": {"name":"哈密冰棍","hp":246,"atk":68,"def":18,"money":3,"experience":0,"point":0,"special":0},
	"ghostSkeleton": {"name":"冥队长","hp":100,"atk":120,"def":0,"money":8,"experience":0,"point":0,"special":7},
	"zombie": {"name":"猪扒","hp":200,"atk":40,"def":16,"money":2,"experience":0,"point":0,"special":0},
	"zombieKnight": {"name":"黑椒猪扒","hp":350,"atk":75,"def":16,"money":3,"experience":0,"point":0,"special":0},
	"rock": {"name":"曲奇饼","hp":22,"atk":62,"def":44,"money":4,"experience":0,"point":0,"special":3},
	"slimeMan": {"name":"青柠冰沙","hp":333,"atk":53,"def":3,"money":3,"experience":0,"point":0,"special":0,"atkValue":2,"defValue":3},
	"bluePriest": {"name":"牛肉","hp":177,"atk":17,"def":7,"money":2,"experience":0,"point":1,"special":2},
	"redPriest": {"name":"血牛肉","hp":777,"atk":17,"def":17,"money":3,"experience":0,"point":0,"special":2},
	"brownWizard": {"name":"初级巫师","hp":100,"atk":120,"def":0,"money":16,"experience":0,"point":0,"special":15,"value":100,"range":2},
	"redWizard": {"name":"高级巫师","hp":1000,"atk":1200,"def":0,"money":160,"experience":0,"point":0,"special":15,"value":200,"zoneSquare":true},
	"yellowGuard": {"name":"莲蓉包","hp":300,"atk":35,"def":20,"money":3,"experience":0,"point":0,"special":8},
	"blueGuard": {"name":"蓝莓淮山","hp":400,"atk":85,"def":20,"money":0,"experience":0,"point":0,"special":8},
	"redGuard": {"name":"烤乳猪","hp":950,"atk":175,"def":45,"money":0,"experience":0,"point":0,"special":0},
	"swordsman": {"name":"双手剑士","hp":100,"atk":120,"def":0,"money":6,"experience":0,"point":0,"special":[5,23]},
	"soldier": {"name":"冥战士","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"yellowKnight": {"name":"奶黄包","hp":288,"atk":85,"def":30,"money":4,"experience":0,"point":0,"special":1},
	"redKnight": {"name":"岭南荔枝","hp":488,"atk":115,"def":55,"money":5,"experience":0,"point":0,"special":0},
	"darkKnight": {"name":"山竹","hp":588,"atk":135,"def":56,"money":6,"experience":0,"point":0,"special":0},
	"blackKing": {"name":"黑衣魔王","hp":1000,"atk":500,"def":0,"money":1000,"experience":1000,"point":0,"special":0,"notBomb":true},
	"yellowKing": {"name":"桂花蜜","hp":235,"atk":415,"def":135,"money":5,"experience":0,"point":0,"special":0},
	"greenKing": {"name":"冬瓜糖","hp":433,"atk":155,"def":8,"money":3,"experience":0,"point":0,"special":11,"value":0.01},
	"blueKnight": {"name":"蓝骑士","hp":100,"atk":120,"def":0,"money":9,"experience":0,"point":0,"special":8},
	"goldSlime": {"name":"黄头怪","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"poisonSkeleton": {"name":"紫骷髅","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"poisonBat": {"name":"马蹄糕","hp":360,"atk":150,"def":60,"money":3,"experience":0,"point":0,"special":5},
	"steelRock": {"name":"田螺","hp":50,"atk":120,"def":100,"money":0,"experience":0,"point":0,"special":3},
	"skeletonPriest": {"name":"骷髅法师","hp":100,"atk":100,"def":0,"money":0,"experience":0,"point":0,"special":18,"value":20},
	"skeletonKing": {"name":"桂花糕","hp":688,"atk":255,"def":75,"money":5,"experience":0,"point":0,"special":0},
	"skeletonWizard": {"name":"骷髅巫师","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"redSkeletonCaption": {"name":"骷髅武士","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"badHero": {"name":"迷失勇者","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"demon": {"name":"魔神武士","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"demonPriest": {"name":"魔神法师","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"goldHornSlime": {"name":"金角怪","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"redKing": {"name":"红衣魔王","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"whiteKing": {"name":"白衣武士","hp":100,"atk":120,"def":0,"money":17,"experience":0,"point":0,"special":16},
	"blackMagician": {"name":"黑暗大法师","hp":100,"atk":120,"def":0,"money":12,"experience":0,"point":0,"special":11,"value":0.3333333333333333,"add":true,"notBomb":true},
	"silverSlime": {"name":"叉烧包","hp":320,"atk":63,"def":10,"money":3,"experience":0,"point":0,"special":0},
	"swordEmperor": {"name":"剑圣","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"whiteHornSlime": {"name":"尖角怪","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"badPrincess": {"name":"痛苦魔女","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"badFairy": {"name":"黑暗仙子","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"grayPriest": {"name":"中级法师","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"redSwordsman": {"name":"剑王","hp":100,"atk":120,"def":0,"money":7,"experience":0,"point":0,"special":6,"n":8},
	"whiteGhost": {"name":"水银战士","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"poisonZombie": {"name":"绿兽人","hp":100,"atk":120,"def":0,"money":13,"experience":0,"point":0,"special":12},
	"magicDragon": {"name":"魔龙","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"octopus": {"name":"血影","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"darkFairy": {"name":"仙子","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"greenKnight": {"name":"强盾骑士","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"angel": {"name":"天使","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":0},
	"elemental": {"name":"桂花魂","hp":33300,"atk":399,"def":40,"money":1314,"experience":0,"point":0,"special":[11,22],"value":0.1314,"damage":815},
	"steelGuard": {"name":"铁守卫","hp":0,"atk":0,"def":0,"money":0,"experience":0,"point":0,"special":18,"value":20},
	"evilBat": {"name":"邪恶蝙蝠","hp":1000,"atk":1,"def":0,"money":0,"experience":0,"point":0,"special":[2,3]}
}
MONSTER_START_NUM = 201
MONSTER_IMG = crop_images(load_image("img/enemys.png"),
                          MONSTER_START_NUM,
                          pygame.Rect(0, 0, BLOCK_UNIT*2, BLOCK_UNIT))

'''
# :TODO:
def register_monster(enemy_id, info):
    pass


def get_damage_info(enemy_id):
    pass

# --- Monster Data END ---
'''
# !insert! === 在这里写敌人相关的自定义操作 ===
