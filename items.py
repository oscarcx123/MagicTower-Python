from sysconf import *
ITEM_PROPERTY = {
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
		"I322": {
			"cls": "items",
			"name": "新物品"
		},
		"I323": {
			"cls": "items",
			"name": "新物品"
		},
		"I324": {
			"cls": "items",
			"name": "新物品"
		},
		"I325": {
			"cls": "items",
			"name": "新物品"
		},
		"I326": {
			"cls": "items",
			"name": "新物品"
		},
		"I327": {
			"cls": "items",
			"name": "新物品"
		},
		"I328": {
			"cls": "items",
			"name": "新物品"
		},
		"I329": {
			"cls": "items",
			"name": "新物品"
		},
		"I330": {
			"cls": "items",
			"name": "新物品"
		},
		"I331": {
			"cls": "items",
			"name": "新物品"
		},
		"I332": {
			"cls": "items",
			"name": "新物品"
		},
		"I333": {
			"cls": "equips",
			"name": "新物品",
			"equip": {
				"type": 0
			}
		},
		"I334": {
			"cls": "constants",
			"name": "生命之叶",
			"equip": None,
			"text": "大森林的宝物。持有后吸收生命能量"
		}
	},

	"itemEffect": {
		"redJewel": "player.attack += RED_JEWEL\nplayer.defend += BLUE_JEWEL",
		"blueJewel": "player.defend += BLUE_JEWEL",
		"greenJewel": "player.mdefend += GREEN_JEWEL",
		"yellowJewel": "player.attack += YELLOW_JEWEL\nplayer.defend += YELLOW_JEWEL\nplayer.mdefend += YELLOW_JEWEL * GREEN_JEWEL\nplayer.hp += YELLOW_JEWEL * RED_POTION",
		"redPotion": "player.hp += RED_POTION",
		"bluePotion": "player.hp += BLUE_POTION",
		"yellowPotion": "player.hp += GREEN_POTION",
		"greenPotion": "player.hp += YELLOW_POTION",
		"sword0": "pass",
		"sword1": "player.attack += SWORD_1",
		"sword2": "player.attack += SWORD_2",
		"sword3": "player.attack += SWORD_3",
		"sword4": "player.attack += SWORD_4",
		"sword5": "player.attack += SWORD_5",
		"shield0": "pass",
		"shield1": "player.defend += SHIELD_1",
		"shield2": "player.defend += SHIELD_2",
		"shield3": "player.defend += SHIELD_3",
		"shield4": "player.defend += SHIELD_4",
		"shield5": "player.defend += SHIELD_5",
		"superPotion": "player.hp *= 2",
		"moneyPocket": "player.gold += 500"
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
		"superWine": "superWine()",
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
	
def pickaxe():
	pass

def earthquake():
	temp_x = 0
	temp_y = 0
	map_read(player.floor)
	while temp_y < HEIGHT / BLOCK_UNIT:
		while temp_x < WIDTH / BLOCK_UNIT - 4:
			if map_temp[temp_y][temp_x] == 1: # Only Yellow Wall by default
				map_write(player.floor, temp_x, temp_y, 0)
			temp_x += 1
		temp_y += 1
		temp_x = 0
	return {"result": True}

def pickaxe():
	pass

def icePickaxe():
	pass

def snow():
	pass

def bigKey():
	player.yellowkey += 1
	player.bluekey += 1
	player.redkey += 1
	return {"result": True}

def bomb():
	pass

def hammer():
	pass

def centerFly():
	x_coordinate = player.pos[0]
	y_coordinate = player.pos[1]
	x_max_index = int(WIDTH / BLOCK_UNIT) - 5
	y_max_index = int(HEIGHT / BLOCK_UNIT) - 1
	x_center = x_max_index / 2
	y_center = y_max_index / 2
	x_after_fly = x_coordinate - (2 * (x_coordinate - x_center))
	y_after_fly = y_coordinate - (2 * (y_coordinate - y_center))
	if check_map(player.floor, 0):
		player.pos[0] = x_after_fly
		player.pos[1] = y_after_fly
		return {"result": True}
	else:
		return {"result": False, "msg": "Obstacle blocking"}
    
def upFly():
	if player.floor + 1 > len(map_database):
		return {"result": False, "msg": "You are on top floor"}
	elif check_map(player.floor + 1, 0):
		player.floor += 1
		return {"result": True}
	else:
		return {"result": False, "msg": "Obstacle blocking"}
		
def downFly():
	if player.floor - 1 < 0:
		return {"result": False, "msg": "You are on bottom floor"}
	elif check_map(player.floor - 1, 0):
		player.floor -= 1
		return {"result": True}
	else:
		return {"result": False, "msg": "Obstacle blocking"}

def poisonWine():
	pass

def weakWine():
	pass

def curseWine():
	pass

def superWine():
	pass

def lifeWand():
	pass

def jumpShoes():
	pass

def skill1():
	pass
