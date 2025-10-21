import bones
import cacti
import carrots
import hay
import mazes
import pumpkins
import weird_substances
import woods

item_module_map = {
	Items.Bone: bones,
	Items.Cactus: cacti,
	Items.Carrot: carrots,
	Items.Gold: mazes,
	Items.Hay: hay,
	Items.Pumpkin: pumpkins,
	Items.Weird_Substance: weird_substances,
	Items.Wood: woods,
}


def get_module(item):
	return item_module_map[item]


def wait(s):
	start = get_time()
	while get_time() - start >= s:
		continue
