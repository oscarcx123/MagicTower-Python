from lib.utools import *
from lib import global_var
from project.block import BlockData


ITEMS_START_NUM = 21
ITEMS_IMG = crop_images(load_image("img/items.png"), ITEMS_START_NUM, create_rect(BLOCK_UNIT, BLOCK_UNIT))

# TODO： 写各个物品的类别或效果
ITEMS_DATA = {
	"items": {
		"yellowKey": {
			"cls": "keys",
			"name": "黄钥匙"
		},
		"blueKey": {
			"cls": "keys",
			"name": "蓝钥匙"
		},
		"redKey": {
			"cls": "keys",
			"name": "红钥匙"
		},
		"redJewel": {
			"cls": "items",
			"name": "红宝石",
			"text": "'，攻击+'+core.values.redJewel"
		},
		"blueJewel": {
			"cls": "items",
			"name": "蓝宝石",
			"text": "'，防御+'+core.values.blueJewel"
		},
		"greenJewel": {
			"cls": "items",
			"name": "绿宝石",
			"text": "'，魔防+'+core.values.greenJewel"
		},
		"yellowJewel": {
			"cls": "items",
			"name": "黄宝石",
			"text": "可以进行加点"
		},
		"redPotion": {
			"cls": "items",
			"name": "红血瓶",
			"text": "'，生命+'+core.values.redPotion"
		},
		"bluePotion": {
			"cls": "items",
			"name": "蓝血瓶",
			"text": "'，生命+'+core.values.bluePotion"
		},
		"yellowPotion": {
			"cls": "items",
			"name": "黄血瓶",
			"text": "'生命+'+core.values.yellowPotion"
		},
		"greenPotion": {
			"cls": "items",
			"name": "绿血瓶",
			"text": "'，生命+'+core.values.greenPotion"
		},
		"sword0": {
			"cls": "items",
			"name": "破旧的剑",
			"text": "一把已经生锈的剑",
			"equip": {
				"type": 0,
				"atk": 0,
				"animate": "sword"
			}
		},
		"sword1": {
			"cls": "items",
			"name": "铁剑",
			"text": "一把很普通的铁剑",
			"equip": {
				"type": 0,
				"atk": SWORD_1,
				"animate": "sword"
			}
		},
		"sword2": {
			"cls": "items",
			"name": "银剑",
			"text": "一把很普通的银剑",
			"equip": {
				"type": 0,
				"atk": SWORD_2,
				"animate": "sword"
			}
		},
		"sword3": {
			"cls": "items",
			"name": "骑士剑",
			"text": "一把很普通的骑士剑",
			"equip": {
				"type": 0,
				"atk": SWORD_3,
				"animate": "sword"
			}
		},
		"sword4": {
			"cls": "items",
			"name": "圣剑",
			"text": "一把很普通的圣剑",
			"equip": {
				"type": 0,
				"atk": SWORD_4,
				"animate": "sword"
			}
		},
		"sword5": {
			"cls": "items",
			"name": "神圣剑",
			"text": "一把很普通的神圣剑",
			"equip": {
				"type": 0,
				"atk": SWORD_5,
				"animate": "sword"
			}
		},
		"shield0": {
			"cls": "items",
			"name": "破旧的盾",
			"text": "一个很破旧的铁盾",
			"equip": {
				"type": 1,
				"def": 0
			}
		},
		"shield1": {
			"cls": "items",
			"name": "铁盾",
			"text": "一个很普通的铁盾",
			"equip": {
				"type": 1,
				"def": SHIELD_1
			}
		},
		"shield2": {
			"cls": "items",
			"name": "银盾",
			"text": "一个很普通的银盾",
			"equip": {
				"type": 1,
				"def": SHIELD_2
			}
		},
		"shield3": {
			"cls": "items",
			"name": "骑士盾",
			"text": "一个很普通的骑士盾",
			"equip": {
				"type": 1,
				"def": SHIELD_3
			}
		},
		"shield4": {
			"cls": "items",
			"name": "圣盾",
			"text": "一个很普通的圣盾",
			"equip": {
				"type": 1,
				"def": SHIELD_4
			}
		},
		"shield5": {
			"cls": "items",
			"name": "神圣盾",
			"text": "一个很普通的神圣盾",
			"equip": {
				"type": 1,
				"def": SHIELD_5,
				"mdef": SHIELD_5
			}
		},
		"superPotion": {
			"cls": "items",
			"name": "圣水"
		},
		"moneyPocket": {
			"cls": "items",
			"name": "金钱袋"
		},
		"book": {
			"cls": "constants",
			"name": "怪物手册",
			"text": "可以查看当前楼层各怪物属性"
		},
		"fly": {
			"cls": "constants",
			"name": "楼层传送器",
			"text": "可以自由往来去过的楼层",
			"hideInReplay": True
		},
		"coin": {
			"cls": "constants",
			"name": "幸运金币",
			"text": "持有时打败怪物可得双倍金币"
		},
		"snow": {
			"cls": "constants",
			"name": "冰冻徽章",
			"text": "可以将面前的熔岩变成平地"
		},
		"cross": {
			"cls": "constants",
			"name": "十字架",
			"text": "持有后无视怪物的无敌属性"
		},
		"knife": {
			"cls": "constants",
			"name": "屠龙匕首",
			"text": "该道具尚未被定义"
		},
		"shoes": {
			"cls": "constants",
			"name": "绿鞋",
			"text": "持有时无视负面地形"
		},
		"bigKey": {
			"cls": "tools",
			"name": "大黄门钥匙",
			"text": "可以开启当前层所有黄门"
		},
		"greenKey": {
			"cls": "tools",
			"name": "绿钥匙",
			"text": "可以打开一扇绿门"
		},
		"steelKey": {
			"cls": "tools",
			"name": "铁门钥匙",
			"text": "可以打开一扇铁门"
		},
		"pickaxe": {
			"cls": "tools",
			"name": "破墙镐",
			"text": "可以破坏勇士面前的墙"
		},
		"icePickaxe": {
			"cls": "tools",
			"name": "破冰镐",
			"text": "可以破坏勇士面前的一堵冰墙"
		},
		"bomb": {
			"cls": "tools",
			"name": "炸弹",
			"text": "可以炸掉勇士面前的怪物"
		},
		"centerFly": {
			"cls": "tools",
			"name": "中心对称飞行器",
			"text": "可以飞向当前楼层中心对称的位置"
		},
		"upFly": {
			"cls": "tools",
			"name": "上楼器",
			"text": "可以飞往楼上的相同位置"
		},
		"downFly": {
			"cls": "tools",
			"name": "下楼器",
			"text": "可以飞往楼下的相同位置"
		},
		"earthquake": {
			"cls": "tools",
			"name": "地震卷轴",
			"text": "可以破坏当前层的所有墙"
		},
		"poisonWine": {
			"cls": "tools",
			"name": "解毒药水",
			"text": "可以解除中毒状态"
		},
		"weakWine": {
			"cls": "tools",
			"name": "解衰药水",
			"text": "可以解除衰弱状态"
		},
		"curseWine": {
			"cls": "tools",
			"name": "解咒药水",
			"text": "可以解除诅咒状态"
		},
		"superWine": {
			"cls": "tools",
			"name": "万能药水",
			"text": "可以解除所有不良状态"
		},
		"hammer": {
			"cls": "tools",
			"name": "圣锤",
			"text": "可以炸掉勇士面前的怪物"
		},
		"lifeWand": {
			"cls": "tools",
			"name": "生命魔杖",
			"text": "可以恢复100点生命值"
		},
		"jumpShoes": {
			"cls": "tools",
			"name": "跳跃靴",
			"text": "能跳跃到前方两格处"
		},
		"skill1": {
			"cls": "constants",
			"name": "技能：二倍斩",
			"text": "可以打开或关闭主动技能二倍斩",
			"hideInReplay": True
		},
		"I321": {
			"cls": "items",
			"name": "新物品"
		},
		"I334": {
			"cls": "constants",
			"name": "生命之叶",
			"equip": None,
			"text": "大森林的宝物。持有后吸收生命能量"
		}
	},

	"itemEffect": {
		"redJewel": "PlayerCon.attack += RED_JEWEL",
		"blueJewel": "PlayerCon.defend += BLUE_JEWEL",
		"greenJewel": "PlayerCon.mdefend += GREEN_JEWEL",
		"yellowJewel": "PlayerCon.attack += YELLOW_JEWEL\nPlayerCon.defend += YELLOW_JEWEL\nPlayerCon.mdefend += YELLOW_JEWEL * GREEN_JEWEL\nPlayerCon.hp += YELLOW_JEWEL * RED_POTION",
		"redPotion": "PlayerCon.hp += RED_POTION",
		"bluePotion": "PlayerCon.hp += BLUE_POTION",
		"yellowPotion": "PlayerCon.hp += GREEN_POTION",
		"greenPotion": "PlayerCon.hp += YELLOW_POTION",
		"sword0": "pass",
		"sword1": "PlayerCon.attack += SWORD_1",
		"sword2": "PlayerCon.attack += SWORD_2",
		"sword3": "PlayerCon.attack += SWORD_3",
		"sword4": "PlayerCon.attack += SWORD_4",
		"sword5": "PlayerCon.attack += SWORD_5",
		"shield0": "pass",
		"shield1": "PlayerCon.defend += SHIELD_1",
		"shield2": "PlayerCon.defend += SHIELD_2",
		"shield3": "PlayerCon.defend += SHIELD_3",
		"shield4": "PlayerCon.defend += SHIELD_4",
		"shield5": "PlayerCon.defend += SHIELD_5",
		"superPotion": "PlayerCon.hp *= 2",
		"moneyPocket": "PlayerCon.gold += 500"
	},
	"itemEffectTip": {
		"redJewel": "'，攻击+'+core.values.redJewel * ratio",
		"blueJewel": "'，防御+'+core.values.blueJewel * ratio",
		"greenJewel": "'，魔防+'+core.values.greenJewel * ratio",
		"yellowJewel": "'，全属性提升'",
		"redPotion": "'，生命+'+core.values.redPotion * ratio",
		"bluePotion": "'，生命+'+core.values.bluePotion * ratio",
		"yellowPotion": "'，生命+'+core.values.yellowPotion * ratio",
		"greenPotion": "'，生命+'+core.values.greenPotion * ratio",
		"sword0": "'，攻击+0'",
		"sword1": "'，攻击+10'",
		"sword2": "'，攻击+20'",
		"sword3": "'，攻击+40'",
		"sword4": "'，攻击+80'",
		"sword5": "'，攻击+100'",
		"shield0": "'，防御+0'",
		"shield1": "'，防御+10'",
		"shield2": "'，防御+20'",
		"shield3": "'，防御+40'",
		"shield4": "'，防御+80'",
		"shield5": "'，防御+100，魔防+100'",
		"bigKey": "'，全钥匙+1'",
		"superPotion": "'，生命值翻倍'",
		"moneyPocket": "'，金币+500'"
	},
	"useItemEffect": {
		"book": "book()",
		"fly": "fly()",
		"earthquake": "earthquake()",
		"pickaxe": "pickaxe()",
		"icePickaxe": "icePickaxe()",
		"snow": "snow()",
		"bigKey": "bigKey()",
		"bomb": "bomb()",
		"hammer": "hammer()",
		"centerFly": "centerFly()",
		"upFly": "upFly()",
		"downFly": "downFly()",
		"poisonWine": "poisonWine()",
		"weakWine": "weakWine()",
		"curseWine": "curseWine()",
		"superPotion": "superPotion()",
		"lifeWand": "lifeWand()",
		"jumpShoes": "jumpShoes()",
		"skill1": "skill1()",
		
	},
	"canEquip": {}
}

def book():
	pass
	
def fly():
	pass

# 地震卷轴，可以破坏当前层的所有墙
def earthquake():
	CurrentMap = global_var.get_value("CurrentMap")
	temp_x = 0
	temp_y = 0
	while temp_y < HEIGHT / BLOCK_UNIT:
		while temp_x < WIDTH / BLOCK_UNIT - 4:
			temp_block = CurrentMap.get_block(temp_x, temp_y)
			 # 可能破坏的是三种墙，编号是1-3
			if temp_block in range(1,4):
				if BlockData[str(temp_block)]["canBreak"]:
					CurrentMap.remove_block(temp_x, temp_y)
			temp_x += 1
		temp_y += 1
		temp_x = 0
	return {"result": True}

# 破墙镐，可以破坏勇士面前的墙
def pickaxe():
	Music = global_var.get_value("Music")
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	x_coord = PlayerCon.pos[0]
	y_coord = PlayerCon.pos[1]
	if PlayerCon.face[0] == 0 and y_coord + 1 < int(HEIGHT / BLOCK_UNIT):
		y_coord += 1
		temp_block = CurrentMap.get_block(x_coord, y_coord)
		# 可能破坏的是三种墙，编号是1-3
		if temp_block in range(1,4):
			if BlockData[str(temp_block)]["canBreak"]:
				Music.play_SE("pickaxe.ogg")
				CurrentMap.remove_block(x_coord, y_coord)
				return {"result": True}
	elif PlayerCon.face[0] == 1 and x_coord - 1 >= 0:
		x_coord -= 1
		temp_block = CurrentMap.get_block(x_coord, y_coord)
		# 可能破坏的是三种墙，编号是1-3
		if temp_block in range(1,4):
			if BlockData[str(temp_block)]["canBreak"]:
				Music.play_SE("pickaxe.ogg")
				CurrentMap.remove_block(x_coord, y_coord)
				return {"result": True}
	elif PlayerCon.face[0] == 2 and x_coord + 1 < int(WIDTH / BLOCK_UNIT):
		x_coord += 1
		temp_block = CurrentMap.get_block(x_coord, y_coord)
		# 可能破坏的是三种墙，编号是1-3
		if temp_block in range(1,4):
			if BlockData[str(temp_block)]["canBreak"]:
				Music.play_SE("pickaxe.ogg")
				CurrentMap.remove_block(x_coord, y_coord)
				return {"result": True}
	elif PlayerCon.face[0] == 3 and y_coord - 1 >= 0:
		y_coord -= 1
		temp_block = CurrentMap.get_block(x_coord, y_coord)
		# 可能破坏的是三种墙，编号是1-3
		if temp_block in range(1,4):
			if BlockData[str(temp_block)]["canBreak"]:
				Music.play_SE("pickaxe.ogg")
				CurrentMap.remove_block(x_coord, y_coord)
				return {"result": True}
	return {"result": False, "msg": "玩家面对的不是墙！"}

def icePickaxe():
	pass

def snow():
	pass

# 大钥匙，默认开启当前层所有黄门
# 另一效果为全钥匙+1，在全塔属性提供启用另一效果的开关
# 启用另一效果只需将“BIG_KEY_OPEN_YELLOW_DOORS”从True改为False即可
def bigKey():
	from project.function import add_item, remove_item
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	if BIG_KEY_OPEN_YELLOW_DOORS:
		temp_x = 0
		temp_y = 0
		while temp_y < HEIGHT / BLOCK_UNIT:
			while temp_x < WIDTH / BLOCK_UNIT - 4:
				# 81 = Yellow Door
				if CurrentMap.get_block(temp_x, temp_y) == 81:
					CurrentMap.remove_block(temp_x, temp_y)
				temp_x += 1
			temp_y += 1
			temp_x = 0
	else:
		add_item(21, 1)
		add_item(22, 1)
		add_item(23, 1)
	return {"result": True}

# 炸弹，可以炸掉勇士面前的怪物
def bomb():
	Music = global_var.get_value("Music")
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	x_coord = PlayerCon.pos[0]
	y_coord = PlayerCon.pos[1]
	if PlayerCon.face[0] == 0 and y_coord + 1 < int(HEIGHT / BLOCK_UNIT):
		y_coord += 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			Music.play_SE("bomb.ogg")
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	elif PlayerCon.face[0] == 1 and x_coord - 1 >= 0:
		x_coord -= 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			Music.play_SE("bomb.ogg")
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	elif PlayerCon.face[0] == 2 and x_coord + 1 < int(WIDTH / BLOCK_UNIT):
		x_coord += 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			Music.play_SE("bomb.ogg")
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	elif PlayerCon.face[0] == 3 and y_coord - 1 >= 0:
		y_coord -= 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			Music.play_SE("bomb.ogg")
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	return {"result": False, "msg": "玩家面对的不是怪物！"}

# 圣锤，在样板中的作用跟炸弹完全一样
def hammer():
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	x_coord = PlayerCon.pos[0]
	y_coord = PlayerCon.pos[1]
	if PlayerCon.face[0] == 0 and y_coord + 1 < int(HEIGHT / BLOCK_UNIT):
		y_coord += 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	elif PlayerCon.face[0] == 1 and x_coord - 1 >= 0:
		x_coord -= 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	elif PlayerCon.face[0] == 2 and x_coord + 1 < int(WIDTH / BLOCK_UNIT):
		x_coord += 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	elif PlayerCon.face[0] == 3 and y_coord - 1 >= 0:
		y_coord -= 1
		if CurrentMap.get_block(x_coord, y_coord) > 200:
			CurrentMap.remove_block(x_coord, y_coord)
			return {"result": True}
	return {"result": False, "msg": "玩家面对的不是怪物！"}

# 中心对称飞行器，可以飞向当前楼层中心对称的位置
def centerFly():
	Music = global_var.get_value("Music")
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	x_coordinate = PlayerCon.pos[0]
	y_coordinate = PlayerCon.pos[1]
	x_max_index = int(WIDTH / BLOCK_UNIT) - 5
	y_max_index = int(HEIGHT / BLOCK_UNIT) - 1
	x_center = x_max_index / 2
	y_center = y_max_index / 2
	x_after_fly = int(x_coordinate - (2 * (x_coordinate - x_center)))
	y_after_fly = int(y_coordinate - (2 * (y_coordinate - y_center)))
	if CurrentMap.get_block(x_after_fly, y_after_fly) == 0:
		Music.play_SE("centerFly.ogg")
		PlayerCon.pos[0] = x_after_fly
		PlayerCon.pos[1] = y_after_fly
		PlayerCon.change_hero_loc(PlayerCon.pos[0], PlayerCon.pos[1])
		return {"result": True}
	else:
		return {"result": False, "msg": "落点有障碍物！"}

# 上楼器，可以飞往楼上的相同位置
def upFly():
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	if PlayerCon.floor + 1 > len(CurrentMap.floor_index["index"]):
		return {"result": False, "msg": "玩家已经在最高层"}
	elif CurrentMap.get_block(PlayerCon.pos[0], PlayerCon.pos[1], floor=PlayerCon.floor + 1) == 0:
		PlayerCon.floor += 1
		CurrentMap.set_map(PlayerCon.floor)
		return {"result": True}
	else:
		return {"result": False, "msg": "落点有障碍物！"}

# 下楼器，可以飞往楼下的相同位置
def downFly():
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	if PlayerCon.floor - 1 < 0:
		return {"result": False, "msg": "玩家已经在最低层"}
	elif CurrentMap.get_block(PlayerCon.pos[0], PlayerCon.pos[1], floor=PlayerCon.floor - 1) == 0:
		PlayerCon.floor -= 1
		CurrentMap.set_map(PlayerCon.floor)
		return {"result": True}
	else:
		return {"result": False, "msg": "落点有障碍物！"}

def poisonWine():
	pass

def weakWine():
	pass

def curseWine():
	pass

# 圣水，使用后生命翻倍
def superPotion():
	PlayerCon = global_var.get_value("PlayerCon")
	PlayerCon.hp *= 2
	return {"result": True}

# 生命魔杖，可以恢复100点生命值
def lifeWand():
	PlayerCon = global_var.get_value("PlayerCon")
	PlayerCon.hp += 100
	return {"result": True}

# 跳跃靴，能跳跃到前方两格处
def jumpShoes():
	Music = global_var.get_value("Music")
	PlayerCon = global_var.get_value("PlayerCon")
	CurrentMap = global_var.get_value("CurrentMap")
	x_coord = PlayerCon.pos[0]
	y_coord = PlayerCon.pos[1]
	if PlayerCon.face[0] == 0 and y_coord + 2 < int(HEIGHT / BLOCK_UNIT):
		y_coord += 2
		if CurrentMap.get_block(x_coord, y_coord) == 0:
			Music.play_SE("jump.ogg")
			PlayerCon.pos[1] += 2
			PlayerCon.change_hero_loc(PlayerCon.pos[0], PlayerCon.pos[1])
			return {"result": True}
	elif PlayerCon.face[0] == 1 and x_coord - 2 >= 0:
		x_coord -= 2
		if CurrentMap.get_block(x_coord, y_coord) == 0:
			Music.play_SE("jump.ogg")
			PlayerCon.pos[0] -= 2
			PlayerCon.change_hero_loc(PlayerCon.pos[0], PlayerCon.pos[1])
			return {"result": True}
	elif PlayerCon.face[0] == 2 and x_coord + 2 < int(WIDTH / BLOCK_UNIT):
		x_coord += 2
		if CurrentMap.get_block(x_coord, y_coord) == 0:
			Music.play_SE("jump.ogg")
			PlayerCon.pos[0] += 2
			PlayerCon.change_hero_loc(PlayerCon.pos[0], PlayerCon.pos[1])
			return {"result": True}
	elif PlayerCon.face[0] == 3 and y_coord - 2 >= 0:
		y_coord -= 2
		if CurrentMap.get_block(x_coord, y_coord) == 0:
			Music.play_SE("jump.ogg")
			PlayerCon.pos[1] -= 2
			PlayerCon.change_hero_loc(PlayerCon.pos[0], PlayerCon.pos[1])
			return {"result": True}
	return {"result": False, "msg": "落点有障碍物！"}

def skill1():
	pass

# !insert! === 在这里注册额外物品（items.png之外的特殊素材） ===
