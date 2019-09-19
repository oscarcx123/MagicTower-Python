# MagicTower-Python

Warning: The English translation might not be up to date. If anything seems to be deprecated, post an issue.

## Intro
Magic Tower Python (a.k.a Tower of the Sorcerer) is created with Pygame module of Python. Magic Tower Python should be able to run on most of the major platforms!

Note: Magic Tower is the word by word translation of 魔法の塔(Japanese) and 魔塔(Chinese)

## Prerequisites
The following needs to be installed:

* Python 3.6 or above
* Pygame (installed from PIP)

Run test.py to play the game~

## Instructions
All the maps for the current demo tower is playable, the content is almost complete, but due to the lack of EventFlow, some features such as winning events and talking with NPCs are unavailable. After all, this demo is only for demonstration purposes. However, the items in the backpack are fully available, feel free to use them~

The content of the demo game is the easy difficulty taken from "Mid-Autumn Festival 2019: Guiyu", and it should be quite easy. The only difference between this demo and the original game is the lack of Events.

Currently available shortcuts:

* X = Monster Manual
* G = Floor Teleporter
* T = Backpack (sorted by category, has a secondary menu)
* S = Save File
* D = Load File
* Z = Rotate player (clockwise)
* H = Help
* B = Textbox Demo (for testing)
* ESC = generally for returning from various menus
* Input = generally for confirmation in various menus

In some interfaces such as Monster Manual, Save File, etc., you can use the left and right arrow keys to quickly navigate through pages.

## Extra Instruction

### Monster Manual

If there's no monster on the current map, it shows "No Monsters on this floor (本层无怪物)".

A typical Monster data displayed in Monster Manual should look like this:

| Icon | Name             | HP             | ATK                     | DEF                     |
|------|------------------|----------------|-------------------------|-------------------------|
|      | Possible Ability | GOLD           | EXP                     | DAMAGE                  |
|      | Possible Ability | Critical Point | Decrease Damage by +ATK | Decrease Damage by +DEF |

Critical Point is the amount of ATK needed to see the decrease of damage.

Decrease Damage by +ATK is the amount of damaged decreased after reaching the critical point.

Decrease Damage by +DEF is the amount of damaged decreased after +1 DEF

Example for these concepts:

Hero: HP = 1000, ATK = 10, DEF = 8

Monster: HP = 50, ATK = 14, DEF = 1

Hero's effective ATK = hero's ATK - monster's DEF = 10 - 1 = 9

hero attack times = monster's HP / Hero's effective ATK = 50 / 9 = 5.56

Since we don't have 0.56 turn, the actual hero attack times should be 6. In other words, just simply take the smallest integer larger than hero attack times.

Due to the fact that hero always attack first (unless the monster has the ability to attack first), the monster can only attack 6 - 1 = 5 times.

Monster's effective ATK = monster's ATK - hero's DEF = 14 - 8 = 6

Finally, Damage = Monster's effective ATK * Monster attack times = 6 * 5 = 30

Refering to the Monster Manual, we can see that Critical Point is 1.

When we raise the hero's ATK by 1, DAMAGE = (50 / (11 - 1) - 1) * 6 = 24

You should see that NEW_DAMAGE - PREVIOUS_DAMAGE = 30 - 24 = 6

That's why 6 is shown in the "Decrease Damage by +ATK" field.

Since "Decrease Damage by +DEF" field uses basically the same approach to calculate, I am not going to do another illustration.

### Backpack

There are 5 categories and they are keys, items, permanent items, tools, equipments.

For individual items, you can try to use some translator app with OCR feature.

### Save / Load Panel

These are self-explanatory. The save file info should be in English Acronyms and numbers.

# Updates

Please refer to the Chinese Version.
