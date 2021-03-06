#!/usr/bin/python
import subprocess #lets us run UNIX commands
import smbus #Lets us use busreads for rgb
import time #lets us use wait
from tkinter import * #lets us use kinter
import RPi.GPIO as GPIO #Lets us interface with GPIO
import PCF8591 as ADC #Lets us use ADC funcitonality for photoresistor

print("Program loaded."); #lets us know that program is loaded

class Color: #class to define "colors" as objects with r, g, and b values
  def __init__(self, r, g, b):
    self.red = r
    self.blue = b
    self.green = g


#DEFINES PAIRED LIST OF COLORS NAMES/LITERALS:

color_names = ["cloudy blue","dark pastel green","dust","electric lime","fresh green","light eggplant","nasty green","really light blue","tea","warm purple","yellowish tan","cement","dark grass green","dusty teal","grey teal","macaroni and cheese","pinkish tan","spruce","strong blue","toxic green","windows blue","blue blue","blue with a hint of purple","booger","bright sea green","dark green blue","deep turquoise","green teal","strong pink","bland","deep aqua","lavender pink","light moss green","light seafoam green","olive yellow","pig pink","deep lilac","desert","dusty lavender","purpley grey","purply","candy pink","light pastel green","boring green","kiwi green","light grey green","orange pink","tea green","very light brown","egg shell","eggplant purple","powder pink","reddish grey","baby shit brown","liliac","stormy blue","ugly brown","custard","darkish pink","deep brown","greenish beige","manilla","off blue","battleship grey","browny green","bruise","kelley green","sickly yellow","sunny yellow","azul","darkgreen","green/yellow","lichen","light light green","pale gold","sun yellow","tan green","burple","butterscotch","toupe","dark cream","indian red","light lavendar","poison green","baby puke green","bright yellow green","charcoal grey","squash","cinnamon","light pea green","radioactive green","raw sienna","baby purple","cocoa","light royal blue","orangeish","rust brown","sand brown","swamp","tealish green","burnt siena","camo","dusk blue","fern","old rose","pale light green","peachy pink","rosy pink","light bluish green","light bright green","light neon green","light seafoam","tiffany blue","washed out green","browny orange","nice blue","sapphire","greyish teal","orangey yellow","parchment","straw","very dark brown","terracota","ugly blue","clear blue","creme","foam green","grey/green","light gold","seafoam blue","topaz","violet pink","wintergreen","yellow tan","dark fuchsia","indigo blue","light yellowish green","pale magenta","rich purple","sunflower yellow","green/blue","leather","racing green","vivid purple","dark royal blue","hazel","muted pink","booger green","canary","cool grey","dark taupe","darkish purple","true green","coral pink","dark sage","dark slate blue","flat blue","mushroom","rich blue","dirty purple","greenblue","icky green","light khaki","warm blue","dark hot pink","deep sea blue","carmine","dark yellow green","pale peach","plum purple","golden rod","neon red","old pink","very pale blue","blood orange","grapefruit","sand yellow","clay brown","dark blue grey","flat green","light green blue","warm pink","dodger blue","gross green","ice","metallic blue","pale salmon","sap green","algae","bluey grey","greeny grey","highlighter green","light light blue","light mint","raw umber","vivid blue","deep lavender","dull teal","light greenish blue","mud green","pinky","red wine","shit green","tan brown","darkblue","rosa","lipstick","pale mauve","claret","dandelion","orangered","poop green","ruby","dark","greenish turquoise","pastel red","piss yellow","bright cyan","dark coral","algae green","darkish red","reddy brown","blush pink","camouflage green","lawn green","putty","vibrant blue","dark sand","purple/blue","saffron","twilight","warm brown","bluegrey","bubble gum pink","duck egg blue","greenish cyan","petrol","royal","butter","dusty orange","off yellow","pale olive green","orangish","leaf","light blue grey","dried blood","lightish purple","rusty red","lavender blue","light grass green","light mint green","sunflower","velvet","brick orange","lightish red","pure blue","twilight blue","violet red","yellowy brown","carnation","muddy yellow","dark seafoam green","deep rose","dusty red","grey/blue","lemon lime","purple/pink","brown yellow","purple brown","wisteria","banana yellow","lipstick red","water blue","brown grey","vibrant purple","baby green","barf green","eggshell blue","sandy yellow","cool green","pale","blue/grey","hot magenta","greyblue","purpley","baby shit green","brownish pink","dark aquamarine","diarrhea","light mustard","pale sky blue","turtle green","bright olive","dark grey blue","greeny brown","lemon green","light periwinkle","seaweed green","sunshine yellow","ugly purple","medium pink","puke brown","very light pink","viridian","bile","faded yellow","very pale green","vibrant green","bright lime","spearmint","light aquamarine","light sage","yellowgreen","baby poo","dark seafoam","deep teal","heather","rust orange","dirty blue","fern green","bright lilac","weird green","peacock blue","avocado green","faded orange","grape purple","hot green","lime yellow","mango","shamrock","bubblegum","purplish brown","vomit yellow","pale cyan","key lime","tomato red","lightgreen","merlot","night blue","purpleish pink","apple","baby poop green","green apple","heliotrope","yellow/green","almost black","cool blue","leafy green","mustard brown","dusk","dull brown","frog green","vivid green","bright light green","fluro green","kiwi","seaweed","navy green","ultramarine blue","iris","pastel orange","yellowish orange","perrywinkle","tealish","dark plum","pear","pinkish orange","midnight purple","light urple","dark mint","greenish tan","light burgundy","turquoise blue","ugly pink","sandy","electric pink","muted purple","mid green","greyish","neon yellow","banana","carnation pink","tomato","sea","muddy brown","turquoise green","buff","fawn","muted blue","pale rose","dark mint green","amethyst","blue/green","chestnut","sick green","pea","rusty orange","stone","rose red","pale aqua","deep orange","earth","mossy green","grassy green","pale lime green","light grey blue","pale grey","asparagus","blueberry","purple red","pale lime","greenish teal","caramel","deep magenta","light peach","milk chocolate","ocher","off green","purply pink","lightblue","dusky blue","golden","light beige","butter yellow","dusky purple","french blue","ugly yellow","greeny yellow","orangish red","shamrock green","orangish brown","tree green","deep violet","gunmetal","blue/purple","cherry","sandy brown","warm grey","dark indigo","midnight","bluey green","grey pink","soft purple","blood","brown red","medium grey","berry","poo","purpley pink","light salmon","snot","easter purple","light yellow green","dark navy blue","drab","light rose","rouge","purplish red","slime green","baby poop","irish green","pink/purple","dark navy","greeny blue","light plum","pinkish grey","dirty orange","rust red","pale lilac","orangey red","primary blue","kermit green","brownish purple","murky green","wheat","very dark purple","bottle green","watermelon","deep sky blue","fire engine red","yellow ochre","pumpkin orange","pale olive","light lilac","lightish green","carolina blue","mulberry","shocking pink","auburn","bright lime green","celadon","pinkish brown","poo brown","bright sky blue","celery","dirt brown","strawberry","dark lime","copper","medium brown","muted green","robin's egg","bright aqua","bright lavender","ivory","very light purple","light navy","pink red","olive brown","poop brown","mustard green","ocean green","very dark blue","dusty green","light navy blue","minty green","adobe","barney","jade green","bright light blue","light lime","dark khaki","orange yellow","ocre","maize","faded pink","british racing green","sandstone","mud brown","light sea green","robin egg blue","aqua marine","dark sea green","soft pink","orangey brown","cherry red","burnt yellow","brownish grey","camel","purplish grey","marine","greyish pink","pale turquoise","pastel yellow","bluey purple","canary yellow","faded red","sepia","coffee","bright magenta","mocha","ecru","purpleish","cranberry","darkish green","brown orange","dusky rose","melon","sickly green","silver","purply blue","purpleish blue","hospital green","shit brown","mid blue","amber","easter green","soft blue","cerulean blue","golden brown","bright turquoise","red pink","red purple","greyish brown","vermillion","russet","steel grey","lighter purple","bright violet","prussian blue","slate green","dirty pink","dark blue green","pine","yellowy green","dark gold","bluish","darkish blue","dull red","pinky red","bronze","pale teal","military green","barbie pink","bubblegum pink","pea soup green","dark mustard","shit","medium purple","very dark green","dirt","dusky pink","red violet","lemon yellow","pistachio","dull yellow","dark lime green","denim blue","teal blue","lightish blue","purpley blue","light indigo","swamp green","brown green","dark maroon","hot purple","dark forest green","faded blue","drab green","light lime green","snot green","yellowish","light blue green","bordeaux","light mauve","ocean","marigold","muddy green","dull orange","steel","electric purple","fluorescent green","yellowish brown","blush","soft green","bright orange","lemon","purple grey","acid green","pale lavender","violet blue","light forest green","burnt red","khaki green","cerise","faded purple","apricot","dark olive green","grey brown","green grey","true blue","pale violet","periwinkle blue","light sky blue","blurple","green brown","bluegreen","bright teal","brownish yellow","pea soup","forest","barney purple","ultramarine","purplish","puke yellow","bluish grey","dark periwinkle","dark lilac","reddish","light maroon","dusty purple","terra cotta","avocado","marine blue","teal green","slate grey","lighter green","electric green","dusty blue","golden yellow","bright yellow","light lavender","umber","poop","dark peach","jungle green","eggshell","denim","yellow brown","dull purple","chocolate brown","wine red","neon blue","dirty green","light tan","ice blue","cadet blue","dark mauve","very light blue","grey purple","pastel pink","very light green","dark sky blue","evergreen","dull pink","aubergine","mahogany","reddish orange","deep green","vomit green","purple pink","dusty pink","faded green","camo green","pinky purple","pink purple","brownish red","dark rose","mud","brownish","emerald green","pale brown","dull blue","burnt umber","medium green","clay","light aqua","light olive green","brownish orange","dark aqua","purplish pink","dark salmon","greenish grey","jade","ugly green","dark beige","emerald","pale red","light magenta","sky","light cyan","yellow orange","reddish purple","reddish pink","orchid","dirty yellow","orange red","deep red","orange brown","cobalt blue","neon pink","rose pink","greyish purple","raspberry","aqua green","salmon pink","tangerine","brownish green","red brown","greenish brown","pumpkin","pine green","charcoal","baby pink","cornflower","blue violet","chocolate","greyish green","scarlet","green yellow","dark olive","sienna","pastel purple","terracotta","aqua blue","sage green","blood red","deep pink","grass","moss","pastel blue","bluish green","green blue","dark tan","greenish blue","pale orange","vomit","forrest green","dark lavender","dark violet","purple blue","dark cyan","olive drab","pinkish","cobalt","neon purple","light turquoise","apple green","dull green","wine","powder blue","off white","electric blue","dark turquoise","blue purple","azure","bright red","pinkish red","cornflower blue","light olive","grape","greyish blue","purplish blue","yellowish green","greenish yellow","medium blue","dusty rose","light violet","midnight blue","bluish purple","red orange","dark magenta","greenish","ocean blue","coral","cream","reddish brown","burnt sienna","brick","sage","grey green","white","robin's egg blue","moss green","steel blue","eggplant","light yellow","leaf green","light grey","puke","pinkish purple","sea blue","pale purple","slate blue","blue grey","hunter green","fuchsia","crimson","pale yellow","ochre","mustard yellow","light red","cerulean","pale pink","deep blue","rust","light teal","slate","goldenrod","dark yellow","dark grey","army green","grey blue","seafoam","puce","spring green","dark orange","sand","pastel green","mint","light orange","bright pink","chartreuse","deep purple","dark brown","taupe","pea green","puke green","kelly green","seafoam green","blue green","khaki","burgundy","dark teal","brick red","royal purple","plum","mint green","gold","baby blue","yellow green","bright purple","dark red","pale blue","grass green","navy","aquamarine","burnt orange","neon green","bright blue","rose","light pink","mustard","indigo","lime","sea green","periwinkle","dark pink","olive green","peach","pale green","light brown","hot pink","black","lilac","navy blue","royal blue","beige","salmon","olive","maroon","bright green","dark purple","mauve","forest green","aqua","cyan","tan","dark blue","lavender","turquoise","dark green","violet","light purple","lime green","grey","sky blue","yellow","magenta","light green","orange","teal","light blue","red","brown","pink","blue","green","purple"]

color_list = [Color(172,194,217),Color(86,174,87),Color(178,153,110),Color(168,255,4),Color(105,216,79),Color(137,69,133),Color(112,178,63),Color(212,255,255),Color(101,171,124),Color(149,46,143),Color(252,252,129),Color(165,163,145),Color(56,128,4),Color(76,144,133),Color(94,155,138),Color(239,180,53),Color(217,155,130),Color(10,95,56),Color(12,6,247),Color(97,222,42),Color(55,120,191),Color(34,66,199),Color(83,60,198),Color(155,181,60),Color(5,255,166),Color(31,99,87),Color(1,115,116),Color(12,181,119),Color(255,7,137),Color(175,168,139),Color(8,120,127),Color(221,133,215),Color(166,200,117),Color(167,255,181),Color(194,183,9),Color(231,142,165),Color(150,110,189),Color(204,173,96),Color(172,134,168),Color(148,126,148),Color(152,63,178),Color(255,99,233),Color(178,251,165),Color(99,179,101),Color(142,229,63),Color(183,225,161),Color(255,111,82),Color(189,248,163),Color(211,182,131),Color(255,252,196),Color(67,5,65),Color(255,178,208),Color(153,117,112),Color(173,144,13),Color(196,142,253),Color(80,123,156),Color(125,113,3),Color(255,253,120),Color(218,70,125),Color(65,2,0),Color(201,209,121),Color(255,250,134),Color(86,132,174),Color(107,124,133),Color(111,108,10),Color(126,64,113),Color(0,147,55),Color(208,228,41),Color(255,249,23),Color(29,93,236),Color(5,73,7),Color(181,206,8),Color(143,182,123),Color(200,255,176),Color(253,222,108),Color(255,223,34),Color(169,190,112),Color(104,50,227),Color(253,177,71),Color(199,172,125),Color(255,243,154),Color(133,14,4),Color(239,192,254),Color(64,253,20),Color(182,196,6),Color(157,255,0),Color(60,65,66),Color(242,171,21),Color(172,79,6),Color(196,254,130),Color(44,250,31),Color(154,98,0),Color(202,155,247),Color(135,95,66),Color(58,46,254),Color(253,141,73),Color(139,49,3),Color(203,165,96),Color(105,131,57),Color(12,220,115),Color(183,82,3),Color(127,143,78),Color(38,83,141),Color(99,169,80),Color(200,127,137),Color(177,252,153),Color(255,154,138),Color(246,104,142),Color(118,253,168),Color(83,254,92),Color(78,253,84),Color(160,254,191),Color(123,242,218),Color(188,245,166),Color(202,107,2),Color(16,122,176),Color(33,56,171),Color(113,159,145),Color(253,185,21),Color(254,252,175),Color(252,246,121),Color(29,2,0),Color(203,104,67),Color(49,102,138),Color(36,122,253),Color(255,255,182),Color(144,253,169),Color(134,161,125),Color(253,220,92),Color(120,209,182),Color(19,187,175),Color(251,95,252),Color(32,249,134),Color(255,227,110),Color(157,7,89),Color(58,24,177),Color(194,255,137),Color(215,103,173),Color(114,0,88),Color(255,218,3),Color(1,192,141),Color(172,116,52),Color(1,70,0),Color(153,0,250),Color(2,6,111),Color(142,118,24),Color(209,118,143),Color(150,180,3),Color(253,255,99),Color(149,163,166),Color(127,104,78),Color(117,25,115),Color(8,148,4),Color(255,97,99),Color(89,133,86),Color(33,71,97),Color(60,115,168),Color(186,158,136),Color(2,27,249),Color(115,74,101),Color(35,196,139),Color(143,174,34),Color(230,242,162),Color(75,87,219),Color(217,1,102),Color(1,84,130),Color(157,2,22),Color(114,143,2),Color(255,229,173),Color(78,5,80),Color(249,188,8),Color(255,7,58),Color(199,121,134),Color(214,255,254),Color(254,75,3),Color(253,89,86),Color(252,225,102),Color(178,113,61),Color(31,59,77),Color(105,157,76),Color(86,252,162),Color(251,85,129),Color(62,130,252),Color(160,191,22),Color(214,255,250),Color(79,115,142),Color(255,177,154),Color(92,139,21),Color(84,172,104),Color(137,160,176),Color(126,160,122),Color(27,252,6),Color(202,255,251),Color(182,255,187),Color(167,94,9),Color(21,46,255),Color(141,94,183),Color(95,158,143),Color(99,247,180),Color(96,102,2),Color(252,134,170),Color(140,0,52),Color(117,128,0),Color(171,126,76),Color(3,7,100),Color(254,134,164),Color(213,23,78),Color(254,208,252),Color(104,0,24),Color(254,223,8),Color(254,66,15),Color(111,124,0),Color(202,1,71),Color(27,36,49),Color(0,251,176),Color(219,88,86),Color(221,214,24),Color(65,253,254),Color(207,82,78),Color(33,195,111),Color(169,3,8),Color(110,16,5),Color(254,130,140),Color(75,97,19),Color(77,164,9),Color(190,174,138),Color(3,57,248),Color(168,143,89),Color(93,33,208),Color(254,178,9),Color(78,81,139),Color(150,78,2),Color(133,163,178),Color(255,105,175),Color(195,251,244),Color(42,254,183),Color(0,95,106),Color(12,23,147),Color(255,255,129),Color(240,131,58),Color(241,243,63),Color(177,210,123),Color(252,130,74),Color(113,170,52),Color(183,201,226),Color(75,1,1),Color(165,82,230),Color(175,47,13),Color(139,136,248),Color(154,247,100),Color(166,251,178),Color(255,197,18),Color(117,8,81),Color(193,74,9),Color(254,47,74),Color(2,3,226),Color(10,67,122),Color(165,0,85),Color(174,139,12),Color(253,121,143),Color(191,172,5),Color(62,175,118),Color(199,71,103),Color(185,72,78),Color(100,125,142),Color(191,254,40),Color(215,37,222),Color(178,151,5),Color(103,58,63),Color(168,125,194),Color(250,254,75),Color(192,2,47),Color(14,135,204),Color(141,132,104),Color(173,3,222),Color(140,255,158),Color(148,172,2),Color(196,255,247),Color(253,238,115),Color(51,184,100),Color(255,249,208),Color(117,141,163),Color(245,4,201),Color(119,161,181),Color(135,86,228),Color(136,151,23),Color(194,126,121),Color(1,115,113),Color(159,131,3),Color(247,213,96),Color(189,246,254),Color(117,184,79),Color(156,187,4),Color(41,70,91),Color(105,96,6),Color(173,248,2),Color(193,198,252),Color(53,173,107),Color(255,253,55),Color(164,66,160),Color(243,97,150),Color(148,119,6),Color(255,244,242),Color(30,145,103),Color(181,195,6),Color(254,255,127),Color(207,253,188),Color(10,221,8),Color(135,253,5),Color(30,248,118),Color(123,253,199),Color(188,236,172),Color(187,249,15),Color(171,144,4),Color(31,181,122),Color(0,85,90),Color(164,132,172),Color(196,85,8),Color(63,130,157),Color(84,141,68),Color(201,94,251),Color(58,229,127),Color(1,103,149),Color(135,169,34),Color(240,148,77),Color(93,20,81),Color(37,255,41),Color(208,254,29),Color(255,166,43),Color(1,180,76),Color(255,108,181),Color(107,66,71),Color(199,193,12),Color(183,255,250),Color(174,255,110),Color(236,45,1),Color(118,255,123),Color(115,0,57),Color(4,3,72),Color(223,78,200),Color(110,203,60),Color(143,152,5),Color(94,220,31),Color(217,79,245),Color(200,253,61),Color(7,13,13),Color(73,132,184),Color(81,183,59),Color(172,126,4),Color(78,84,129),Color(135,110,75),Color(88,188,8),Color(47,239,16),Color(45,254,84),Color(10,255,2),Color(156,239,67),Color(24,209,123),Color(53,83,10),Color(24,5,219),Color(98,88,196),Color(255,150,79),Color(255,171,15),Color(143,140,231),Color(36,188,168),Color(63,1,44),Color(203,248,95),Color(255,114,76),Color(40,1,55),Color(179,111,246),Color(72,192,114),Color(188,203,122),Color(168,65,91),Color(6,177,196),Color(205,117,132),Color(241,218,122),Color(255,4,144),Color(128,91,135),Color(80,167,71),Color(168,164,149),Color(207,255,4),Color(255,255,126),Color(255,127,167),Color(239,64,38),Color(60,153,146),Color(136,104,6),Color(4,244,137),Color(254,246,158),Color(207,175,123),Color(59,113,159),Color(253,193,197),Color(32,192,115),Color(155,95,192),Color(15,155,142),Color(116,40,2),Color(157,185,44),Color(164,191,32),Color(205,89,9),Color(173,165,135),Color(190,1,60),Color(184,255,235),Color(220,77,1),Color(162,101,62),Color(99,139,39),Color(65,156,3),Color(177,255,101),Color(157,188,212),Color(253,253,254),Color(119,171,86),Color(70,65,150),Color(153,1,71),Color(190,253,115),Color(50,191,132),Color(175,111,9),Color(160,2,92),Color(255,216,177),Color(127,78,30),Color(191,155,12),Color(107,163,83),Color(240,117,230),Color(123,200,246),Color(71,95,148),Color(245,191,3),Color(255,254,182),Color(255,253,116),Color(137,91,123),Color(67,107,173),Color(208,193,1),Color(198,248,8),Color(244,54,5),Color(2,193,77),Color(178,95,3),Color(42,126,25),Color(73,6,72),Color(83,98,103),Color(90,6,239),Color(207,2,52),Color(196,166,97),Color(151,138,132),Color(31,9,84),Color(3,1,45),Color(43,177,121),Color(195,144,155),Color(166,111,181),Color(119,0,1),Color(146,43,5),Color(125,127,124),Color(153,15,75),Color(143,115,3),Color(200,60,185),Color(254,169,147),Color(172,187,13),Color(192,113,254),Color(204,253,127),Color(0,2,46),Color(130,131,68),Color(255,197,203),Color(171,18,57),Color(176,5,75),Color(153,204,4),Color(147,124,0),Color(1,149,41),Color(239,29,231),Color(0,4,53),Color(66,179,149),Color(157,87,131),Color(200,172,169),Color(200,118,6),Color(170,39,4),Color(228,203,255),Color(250,66,36),Color(8,4,249),Color(92,178,0),Color(118,66,78),Color(108,122,14),Color(251,221,126),Color(42,1,52),Color(4,74,5),Color(253,70,89),Color(13,117,248),Color(254,0,2),Color(203,157,6),Color(251,125,7),Color(185,204,129),Color(237,200,255),Color(97,225,96),Color(138,184,254),Color(146,10,78),Color(254,2,162),Color(154,48,1),Color(101,254,8),Color(190,253,183),Color(177,114,97),Color(136,95,1),Color(2,204,254),Color(193,253,149),Color(131,101,57),Color(251,41,67),Color(132,183,1),Color(182,99,37),Color(127,81,18),Color(95,160,82),Color(109,237,253),Color(11,249,234),Color(199,96,255),Color(255,255,203),Color(246,206,252),Color(21,80,132),Color(245,5,79),Color(100,84,3),Color(122,89,1),Color(168,181,4),Color(61,153,115),Color(0,1,51),Color(118,169,115),Color(46,90,136),Color(11,247,125),Color(189,108,72),Color(172,29,184),Color(43,175,106),Color(38,247,253),Color(174,253,108),Color(155,143,85),Color(255,173,1),Color(198,156,4),Color(244,208,84),Color(222,157,172),Color(5,72,13),Color(201,174,116),Color(96,70,15),Color(152,246,176),Color(138,241,254),Color(46,232,187),Color(17,135,93),Color(253,176,192),Color(177,96,2),Color(247,2,42),Color(213,171,9),Color(134,119,95),Color(198,159,89),Color(122,104,127),Color(4,46,96),Color(200,141,148),Color(165,251,213),Color(255,254,113),Color(98,65,199),Color(255,254,64),Color(211,73,78),Color(152,94,43),Color(166,129,76),Color(255,8,232),Color(157,118,81),Color(254,255,202),Color(152,86,141),Color(158,0,58),Color(40,124,55),Color(185,105,2),Color(186,104,115),Color(255,120,85),Color(148,178,28),Color(197,201,199),Color(102,26,238),Color(97,64,239),Color(155,229,170),Color(123,88,4),Color(39,106,179),Color(254,179,8),Color(140,253,126),Color(100,136,234),Color(5,110,238),Color(178,122,1),Color(15,254,249),Color(250,42,85),Color(130,7,71),Color(122,106,79),Color(244,50,12),Color(161,57,5),Color(111,130,138),Color(165,90,244),Color(173,10,253),Color(0,69,119),Color(101,141,109),Color(202,123,128),Color(0,82,73),Color(43,93,52),Color(191,241,40),Color(181,148,16),Color(41,118,187),Color(1,65,130),Color(187,63,63),Color(252,38,71),Color(168,121,0),Color(130,203,178),Color(102,124,62),Color(254,70,165),Color(254,131,204),Color(148,166,23),Color(168,137,5),Color(127,95,0),Color(158,67,162),Color(6,46,3),Color(138,110,69),Color(204,122,139),Color(158,1,104),Color(253,255,56),Color(192,250,139),Color(238,220,91),Color(126,189,1),Color(59,91,146),Color(1,136,159),Color(61,122,253),Color(95,52,231),Color(109,90,207),Color(116,133,0),Color(112,108,17),Color(60,0,8),Color(203,0,245),Color(0,45,4),Color(101,140,187),Color(116,149,81),Color(185,255,102),Color(157,193,0),Color(250,238,102),Color(126,251,179),Color(123,0,44),Color(194,146,161),Color(1,123,146),Color(252,192,6),Color(101,116,50),Color(216,134,59),Color(115,133,149),Color(170,35,255),Color(8,255,8),Color(155,122,1),Color(242,158,142),Color(111,194,118),Color(255,91,0),Color(253,255,82),Color(134,111,133),Color(143,254,9),Color(238,207,254),Color(81,10,201),Color(79,145,83),Color(159,35,5),Color(114,134,57),Color(222,12,98),Color(145,110,153),Color(255,177,109),Color(60,77,3),Color(127,112,83),Color(119,146,111),Color(1,15,204),Color(206,174,250),Color(143,153,251),Color(198,252,255),Color(85,57,204),Color(84,78,3),Color(1,122,121),Color(1,249,198),Color(201,176,3),Color(146,153,1),Color(11,85,9),Color(160,4,152),Color(32,0,177),Color(148,86,140),Color(194,190,14),Color(116,139,151),Color(102,95,209),Color(156,109,165),Color(196,66,64),Color(162,72,87),Color(130,95,135),Color(201,100,59),Color(144,177,52),Color(1,56,106),Color(37,163,111),Color(89,101,109),Color(117,253,99),Color(33,252,13),Color(90,134,173),Color(254,198,21),Color(255,253,1),Color(223,197,254),Color(178,100,0),Color(127,94,0),Color(222,126,93),Color(4,130,67),Color(255,255,212),Color(59,99,140),Color(183,148,0),Color(132,89,126),Color(65,25,0),Color(123,3,35),Color(4,217,255),Color(102,126,44),Color(251,238,172),Color(215,255,254),Color(78,116,150),Color(135,76,98),Color(213,255,255),Color(130,109,140),Color(255,186,205),Color(209,255,189),Color(68,142,228),Color(5,71,42),Color(213,134,157),Color(61,7,52),Color(74,1,0),Color(248,72,28),Color(2,89,15),Color(137,162,3),Color(224,63,216),Color(213,138,148),Color(123,178,116),Color(82,101,37),Color(201,76,190),Color(219,75,218),Color(158,54,35),Color(181,72,93),Color(115,92,18),Color(156,109,87),Color(2,143,30),Color(177,145,110),Color(73,117,156),Color(160,69,14),Color(57,173,72),Color(182,106,80),Color(140,255,219),Color(164,190,92),Color(203,119,35),Color(5,105,107),Color(206,93,174),Color(200,90,83),Color(150,174,141),Color(31,167,116),Color(122,151,3),Color(172,147,98),Color(1,160,73),Color(217,84,77),Color(250,95,247),Color(130,202,252),Color(172,255,252),Color(252,176,1),Color(145,9,81),Color(254,44,84),Color(200,117,196),Color(205,197,10),Color(253,65,30),Color(154,2,0),Color(190,100,0),Color(3,10,167),Color(254,1,154),Color(247,135,154),Color(136,113,145),Color(176,1,73),Color(18,225,147),Color(254,123,124),Color(255,148,8),Color(106,110,9),Color(139,46,22),Color(105,97,18),Color(225,119,1),Color(10,72,30),Color(52,56,55),Color(255,183,206),Color(106,121,247),Color(93,6,233),Color(61,28,2),Color(130,166,125),Color(190,1,25),Color(201,255,39),Color(55,62,2),Color(169,86,30),Color(202,160,255),Color(202,102,65),Color(2,216,233),Color(136,179,120),Color(152,0,2),Color(203,1,98),Color(92,172,45),Color(118,153,88),Color(162,191,254),Color(16,166,116),Color(6,180,139),Color(175,136,74),Color(11,139,135),Color(255,167,86),Color(162,164,21),Color(21,68,6),Color(133,103,152),Color(52,1,63),Color(99,45,233),Color(10,136,138),Color(111,118,50),Color(212,106,126),Color(30,72,143),Color(188,19,254),Color(126,244,204),Color(118,205,38),Color(116,166,98),Color(128,1,63),Color(177,209,252),Color(255,255,228),Color(6,82,255),Color(4,92,90),Color(87,41,206),Color(6,154,243),Color(255,0,13),Color(241,12,69),Color(81,112,215),Color(172,191,105),Color(108,52,97),Color(94,129,157),Color(96,30,249),Color(176,221,22),Color(205,253,2),Color(44,111,187),Color(192,115,122),Color(214,180,252),Color(2,0,53),Color(112,59,231),Color(253,60,6),Color(150,0,86),Color(64,163,104),Color(3,113,156),Color(252,90,80),Color(255,255,194),Color(127,43,10),Color(176,78,15),Color(160,54,35),Color(135,174,115),Color(120,155,115),Color(255,255,255),Color(152,239,249),Color(101,139,56),Color(90,125,154),Color(56,8,53),Color(255,254,122),Color(92,169,4),Color(216,220,214),Color(165,165,2),Color(214,72,215),Color(4,116,149),Color(183,144,212),Color(91,124,153),Color(96,124,142),Color(11,64,8),Color(237,13,217),Color(140,0,15),Color(255,255,132),Color(191,144,5),Color(210,189,10),Color(255,71,76),Color(4,133,209),Color(255,207,220),Color(4,2,115),Color(168,60,9),Color(144,228,193),Color(81,101,114),Color(250,194,5),Color(213,182,10),Color(54,55,55),Color(75,93,22),Color(107,139,164),Color(128,249,173),Color(165,126,82),Color(169,249,113),Color(198,81,2),Color(226,202,118),Color(176,255,157),Color(159,254,176),Color(253,170,72),Color(254,1,177),Color(193,248,10),Color(54,1,63),Color(52,28,2),Color(185,162,129),Color(142,171,18),Color(154,174,7),Color(2,171,46),Color(122,249,171),Color(19,126,109),Color(170,166,98),Color(97,0,35),Color(1,77,78),Color(143,20,2),Color(75,0,110),Color(88,15,65),Color(143,255,159),Color(219,180,12),Color(162,207,254),Color(192,251,45),Color(190,3,253),Color(132,0,0),Color(208,254,254),Color(63,155,11),Color(1,21,62),Color(4,216,178),Color(192,78,1),Color(12,255,12),Color(1,101,252),Color(207,98,117),Color(255,209,223),Color(206,179,1),Color(56,2,130),Color(170,255,50),Color(83,252,161),Color(142,130,254),Color(203,65,107),Color(103,122,4),Color(255,176,124),Color(199,253,181),Color(173,129,80),Color(255,2,141),Color(0,0,0),Color(206,162,253),Color(0,17,70),Color(5,4,170),Color(230,218,166),Color(255,121,108),Color(110,117,14),Color(101,0,33),Color(1,255,7),Color(53,6,62),Color(174,113,129),Color(6,71,12),Color(19,234,201),Color(0,255,255),Color(209,178,111),Color(0,3,91),Color(199,159,239),Color(6,194,172),Color(3,53,0),Color(154,14,234),Color(191,119,246),Color(137,254,5),Color(146,149,145),Color(117,187,253),Color(255,255,20),Color(194,0,120),Color(150,249,123),Color(249,115,6),Color(2,147,134),Color(149,208,252),Color(229,0,0),Color(101,55,0),Color(255,129,192),Color(3,67,223),Color(21,176,26),Color(126,30,156)]

DO = 17; #no valid board num.
TRIG = 26; #Board: 11
ECHO = 18; #Board: 12
BtnPin = 13; #Board: 33
Gpin   = 23; #Board: 12
Rpin   = 20; #Board: 13
Bpin   = 27; #Board: 15
button_pressed_var = False;
buttonPressed = 0

def setColor(col):   #sets the color of the light with a hex
   R_val = (col & 0xff0000) >> 16
   G_val = (col & 0x00ff00) >> 8
   B_val = (col & 0x0000ff) >> 0

   R_val = map(R_val, 0, 255, 0, 100)
   G_val = map(G_val, 0, 255, 0, 100)
   B_val = map(B_val, 0, 255, 0, 100)

   p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
   p_G.ChangeDutyCycle(100-G_val)
   p_B.ChangeDutyCycle(100-B_val)

def setup(): #Sets up all values
    GPIO.setmode(GPIO.BCM); #use BCM Mode
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP);
    GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200); #sets up detect function as button press function
    GPIO.setup(TRIG, GPIO.OUT);
    GPIO.setup(ECHO, GPIO.IN);
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    for i in pins:
      GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
      GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
    p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)

    p_R.start(100)      # Initial duty Cycle = 0(leds off)
    p_G.start(100)
    p_B.start(100)

def detect(chn): #Detects button pressed
    buttonInputManage(GPIO.input(BtnPin))
    return

def buttonInputManage(buttonIn): #MAIN FUNCTIONALITY HERE
  global buttonPressed
  buttonPressed = buttonIn
  print("awefawef") #just a flag to ensure button is working
  if (button_pressed()):
      if (distance_ok()):
        if (not lighting_ok()):
          read_text("light activated");
          turn_on_light(); 
        else:
          setColor(0x000000); #turns light off
        input_color_val = input_color() ; #gets the value of the color sensor
        read_text(color_name(input_color_val));
      else:
        send_distance_error(); #if distance is too high, say "move closer"
  time.sleep(0.3)

def get_distance(): #uses time recorded between bounces to estimate distance
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100 


def color_distance(c1, c2):
  return (c1.red-c2.red)**2+(c1.blue-c2.blue)**2+(c1.green-c2.green)**2


def color_name(col):
  min_distance = color_distance(col,color_list[0]);
  ret_i = 0;
  for i in range(1,len(color_list)-1):
    c_check = color_list[i]
    distance = color_distance(col, c_check);
    if (distance<min_distance):
      #print(str(distance) + " is new d. "+color_names[i]);
      min_distance=distance;
      ret_i=i;
  return color_names[ret_i];

def read_text(str):
  #cmd_beg= 'espeak ';
  #cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null'; # To play back the stored .wav file and to dump the std errors to /dev/null
  #cmd_out= '--stdout > /home/pi/Desktop/Text.wav '; # To store the voice file
  #str = str.replace(' ', '_');
  #call([cmd_beg+cmd_out+str+cmd_end], shell=True);
  str = str.replace(' ','_');
  subprocess.run(("espeak \""+str+"\" 2>/dev/null").split(" "));

def lighting_ok(): #checks if the lighting val is in a resonable range
    lighting_value = ADC.read(0); 
    return (lighting_value < 254);
    
def distance_ok(): #checks if the distance is under a threshhold
    distance = get_distance(); 
    threshhold = 10;
    return distance<threshhold;

def send_distance_error(): #says "move closer"
    read_text("move closer");

def input_color(): #gets the imput color
  bus = smbus.SMBus(1)
  data = bus.read_i2c_block_data(0x44, 0x09, 6);
  greenIn = int((data[1] * 256 + data[0])/256);
  redIn = int((data[3] * 256 + data[2])/256);
  blueIn = int((data[5] * 256 + data[4])/256);
  #print(str(redIn)+","+str(greenIn)+","+str(blueIn));
  return Color(redIn, greenIn, blueIn);

def button_pressed(): 
  return GPIO.input(BtnPin)==0;

def turn_on_light():
  setColor(0xffffff);

def map(x, in_min, in_max, out_min, out_max):
   return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def main_loop():
  while True:
    #print("lighting OK?: "+str(lighting_ok()))
    #print("button pressed?: "+GPIO.output(btnPin))
    print("lighting value: "+str(ADC.read(0)));
    print("color read: "+str(input_color().red)+","+str(input_color().green)+","+str(input_color().blue))
    time.sleep(.3);
    

def destroy(): #ends processes
    #GPIO.output(Gpin, GPIO.HIGH)
    #GPIO.output(Rpin, GPIO.HIGH)  
    p_R.stop()
    p_G.stop()
    p_B.stop()
    for i in pins:
      GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
      GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
    GPIO.cleanup() 

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        main_loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()


#colorTest = input_color();
#print(color_name(colorTest));
#Converts rgb to an appropriate natural-language name, then speaks it aloud
#read_text(color_name(colorTest));

#bus = smbus.SMBus(1)
#bus.write_byte_data(0x44, 0x01, 0x05)
#time.sleep(1)

#BtnPin = 11
#Gpin   = 12
#Rpin   = 13
