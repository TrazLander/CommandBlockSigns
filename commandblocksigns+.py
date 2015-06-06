# coding unicode-escape
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from copy import deepcopy
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Double, TAG_String
import math
displayName = "Command Block Signs +"

block_map = {
	0:"minecraft:air",1:"minecraft:stone",2:"minecraft:grass",3:"minecraft:dirt",4:"minecraft:cobblestone",5:"minecraft:planks",6:"minecraft:sapling",
	7:"minecraft:bedrock",8:"minecraft:flowing_water",9:"minecraft:water",10:"minecraft:flowing_lava",11:"minecraft:lava",12:"minecraft:sand",13:"minecraft:gravel",
	14:"minecraft:gold_ore",15:"minecraft:iron_ore",16:"minecraft:coal_ore",17:"minecraft:log",18:"minecraft:leaves",19:"minecraft:sponge",20:"minecraft:glass",
	21:"minecraft:lapis_ore",22:"minecraft:lapis_block",23:"minecraft:dispenser",24:"minecraft:sandstone",25:"minecraft:noteblock",26:"minecraft:bed",
	27:"minecraft:golden_rail",28:"minecraft:detector_rail",29:"minecraft:sticky_piston",30:"minecraft:web",31:"minecraft:tallgrass",32:"minecraft:deadbush",
	33:"minecraft:piston",34:"minecraft:piston_head",35:"minecraft:wool",36:"minecraft:piston_extension",37:"minecraft:yellow_flower",38:"minecraft:red_flower",
	39:"minecraft:brown_mushroom",40:"minecraft:red_mushroom",41:"minecraft:gold_block",42:"minecraft:iron_block",43:"minecraft:double_stone_slab",
	44:"minecraft:stone_slab",45:"minecraft:brick_block",46:"minecraft:tnt",47:"minecraft:bookshelf",48:"minecraft:mossy_cobblestone",49:"minecraft:obsidian",
	50:"minecraft:torch",51:"minecraft:fire",52:"minecraft:mob_spawner",53:"minecraft:oak_stairs",54:"minecraft:chest",55:"minecraft:redstone_wire",
	56:"minecraft:diamond_ore",57:"minecraft:diamond_block",58:"minecraft:crafting_table",59:"minecraft:wheat",60:"minecraft:farmland",61:"minecraft:furnace",
	62:"minecraft:lit_furnace",63:"minecraft:standing_sign",64:"minecraft:wooden_door",65:"minecraft:ladder",66:"minecraft:rail",67:"minecraft:stone_stairs",
	68:"minecraft:wall_sign",69:"minecraft:lever",70:"minecraft:stone_pressure_plate",71:"minecraft:iron_door",72:"minecraft:wooden_pressure_plate",
	73:"minecraft:redstone_ore",74:"minecraft:lit_redstone_ore",75:"minecraft:unlit_redstone_torch",76:"minecraft:redstone_torch",77:"minecraft:stone_button",
	78:"minecraft:snow_layer",79:"minecraft:ice",80:"minecraft:snow",81:"minecraft:cactus",82:"minecraft:clay",83:"minecraft:reeds",84:"minecraft:jukebox",
	85:"minecraft:fence",86:"minecraft:pumpkin",87:"minecraft:netherrack",88:"minecraft:soul_sand",89:"minecraft:glowstone",90:"minecraft:portal",
	91:"minecraft:lit_pumpkin",92:"minecraft:cake",93:"minecraft:unpowered_repeater",94:"minecraft:powered_repeater",95:"minecraft:stained_glass",
	96:"minecraft:trapdoor",97:"minecraft:monster_egg",98:"minecraft:stonebrick",99:"minecraft:brown_mushroom_block",100:"minecraft:red_mushroom_block",
	101:"minecraft:iron_bars",102:"minecraft:glass_pane",103:"minecraft:melon_block",104:"minecraft:pumpkin_stem",105:"minecraft:melon_stem",106:"minecraft:vine",
	107:"minecraft:fence_gate",108:"minecraft:brick_stairs",109:"minecraft:stone_brick_stairs",110:"minecraft:mycelium",111:"minecraft:waterlily",
	112:"minecraft:nether_brick",113:"minecraft:nether_brick_fence",114:"minecraft:nether_brick_stairs",115:"minecraft:nether_wart",116:"minecraft:enchanting_table",
	117:"minecraft:brewing_stand",118:"minecraft:cauldron",119:"minecraft:end_portal",120:"minecraft:end_portal_frame",121:"minecraft:end_stone",
	122:"minecraft:dragon_egg",123:"minecraft:redstone_lamp",124:"minecraft:lit_redstone_lamp",125:"minecraft:double_wooden_slab",126:"minecraft:wooden_slab",
	127:"minecraft:cocoa",128:"minecraft:sandstone_stairs",129:"minecraft:emerald_ore",130:"minecraft:ender_chest",131:"minecraft:tripwire_hook",
	132:"minecraft:tripwire",133:"minecraft:emerald_block",134:"minecraft:spruce_stairs",135:"minecraft:birch_stairs",136:"minecraft:jungle_stairs",
	137:"minecraft:command_block",138:"minecraft:beacon",139:"minecraft:cobblestone_wall",140:"minecraft:flower_pot",141:"minecraft:carrots",142:"minecraft:potatoes",
	143:"minecraft:wooden_button",144:"minecraft:skull",145:"minecraft:anvil",146:"minecraft:trapped_chest",147:"minecraft:light_weighted_pressure_plate",
	148:"minecraft:heavy_weighted_pressure_plate",149:"minecraft:unpowered_comparator",150:"minecraft:powered_comparator",151:"minecraft:daylight_detector",
	152:"minecraft:redstone_block",153:"minecraft:quartz_ore",154:"minecraft:hopper",155:"minecraft:quartz_block",156:"minecraft:quartz_stairs",
	157:"minecraft:activator_rail",158:"minecraft:dropper",159:"minecraft:stained_hardened_clay",160:"minecraft:stained_glass_pane",161:"minecraft:leaves2",
	162:"minecraft:log2",163:"minecraft:acacia_stairs",164:"minecraft:dark_oak_stairs",165:"minecraft:slime",166:"minecraft:barrier",167:"minecraft:iron_trapdoor",
	168:"minecraft:prismarine",169:"minecraft:sea_lantern",170:"minecraft:hay_block",171:"minecraft:carpet",172:"minecraft:hardened_clay",173:"minecraft:coal_block",
	174:"minecraft:packed_ice",175:"minecraft:double_plant"
}

NAME = 0
XVAL = 1
YVAL = 2
ZVAL = 3
SIGN = 4
NEXT = 5

inputs = [( ("General","title"),
			("This is a modified version of SethBling's Command Block Signs filter, "
			"edited at TrazLander's request, with the moral support and assistance of Asdjke and Moesh.\n"
			"\n"
			"$ | 0 0 0\n"
			"# | 0,0,0\n"
			"% | x:0,y:0,z:0\n"
			"& | Pos:[0d,0d,0d]\n"
			"$$ | 0 0 0 0 0 0\n"
			"## | x=0,y=0,z=0,dx=0,dy=0,dz=0\n"
			"** | minecraft:ID DATA\n"
			"**^ | minecraft:ID DATA\n"
			"*** | id:\"minecraft:ID\",Damage:DATAs\n"
			"***^ | id:\"minecraft:ID\",Damage:DATAs","label"),
			("Output progress to console",False),
			("Sign facing determines player facing for /tp",True),
			("Coordinate Mode:",("Absolute Coordinates","Relative Coordinates")),),
			  
			(("Details","title"),
			("Place a sign at the location you want the variable to output. You can have a sign point to a location by adding or subtracting from the coordinates.\n"
			"\n"
			"Sign directives are as follows:\n"
			"1st line: <variable name>\n"
			"2nd line: +/-x or ~ (optional)\n"
			"3rd line: +/-y or ~ (optional)\n"
			"4th line: +/-z or ~ (optional)\n"
			"\n"
			"Identifiers are as follows:\n"
			"$ | 0 0 0\n"
			"# | 0,0,0\n"
			"% | x:0,y:0,z:0\n"
			"& | Pos:[0d,0d,0d]\n"
			"\n"
			"To select a square area, place 2 signs with "
			"the same variable name at opposite corners:\n"
			"$$ | 0 0 0 0 0 0\n"
			"## | x=0,y=0,z=0,dx=0,dy=0,dz=0\n"
			"\n"
			"These output the block at the sign's location:\n"
			"** | minecraft:lever 1\n"
			"*** | id:\"minecraft:lever\",Damage:1s\n"
			"\n"
			"Adding ^ will output the toggled state:\n"
			"**^ | minecraft:lever 9\n"
			"***^ | id:\"minecraft:lever\",Damage:9s","label")),
			] 

levers = [28,69,77,131,143]
plates = [70,72,147,148]
tripwires = [132,]

rotvals = { 0:0,1:22.5,2:45,3:67.5,4:90,5:112.5,6:135,7:157.5,8:180,9:-157.5,10:-135,11:-112.5,12:-90,13:-67.5,14:-45,15:-22.5 }
wallval = { 2:8,3:0,4:4,5:12 }

button_vals = {0:8,1:9,2:10,3:11,4:12,5:13,6:14,7:15,8:0,9:1,10:2,11:3,12:4,13:5,14:6,15:7}
tripwire_vals = {0:1,2:3,6:7,1:0,3:2,7:6}

def to_number(s,y=False):
	try:
		a = float(s)
		return a
	except ValueError:
		return 0

signsToRemove = []
def replaceVariables(command, waypoint, coords, sign):
	frags = command.split(waypoint)
	if len(frags) > 1:
		signsToRemove.append(sign)
		return coords.join(frags)
	else:
		return command

def perform(level, box, options):
	global signsToRemove
	waypoints = []
	progress = options["Output progress to console"]
	facing = options["Sign facing determines player facing for /tp"]
	relative = True if options["Coordinate Mode:"] == "Relative Coordinates" else False
	
	for (chunk, _, _) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if (x,y,z) in box and t["id"].value == "Sign":

				#check the first line of a sign to see if it has a single word with no spaces
				if "Text1" in t:
					line = t["Text1"].value.replace("\"","")
					if len(line) == 0:
						continue
					if line.find(" ") != -1:
						continue

					#it does, so add it to the waypoint list; "line" is the variable name
					waypoints.append([line, x, y, z, t, 0])

	#go through the list of waypoints and find duplicate variable names, storing the results in a dictionary
	#called "known"; duplicate variable names indicate two signs that are corners of a cuboid volume for a $$ or ## sign
	known = {}
	for a in [b for b in waypoints]:

		#while going through the list, pre-compute the offsets, if any, stored in lines 2-4 of the sign
		ox = 0
		oy = 0
		oz = 0
		if "Text2" in a[SIGN]:
			if a[SIGN]["Text2"].value.replace("\"","")[:1] == "~":
				ox = str(a[SIGN]["Text2"].value.replace("\"",""))
			else:
				ox = to_number(a[SIGN]["Text2"].value.replace("\"",""))
		if "Text3" in a[SIGN]:
			if a[SIGN]["Text3"].value.replace("\"","")[:1] == "~":
				oy = str(a[SIGN]["Text3"].value.replace("\"",""))
			else:
				oy = to_number(a[SIGN]["Text3"].value.replace("\"",""),True)
		if "Text4" in a[SIGN]:
			if a[SIGN]["Text4"].value.replace("\"","")[:1] == "~":
				oz = str(a[SIGN]["Text4"].value.replace("\"",""))
			else:
				oz = to_number(a[SIGN]["Text4"].value.replace("\"",""))

		#check to see if the offset has decimal places; if so, add 0.5 to compensate for entity positioning,
		#since Minecraft uses the center of an entity for its positioning
		if type(ox) == str:
			a[XVAL] = ox
		else:
			a[XVAL] += ox if ox == int(ox) else ox + 0.5

		if type(oy) == str:
			a[YVAL] = oy
		else:
			a[YVAL] += oy

		if type(oz) == str:
			a[ZVAL] = oz
		else:
			a[ZVAL] += oz if oz == int(oz) else oz + 0.5

		#check to see if we've already found this sign; if so, add the sign to the existing sign at its end.  If not, add the
		#aign to the list.
		if a[NAME] in known:
			if not known[a[NAME]][NEXT]:
				known[a[NAME]][NEXT] = deepcopy(a) #deepcopy, so we don't lose signs with waypoints.remove
			else:
				print "Error: Third sign detected for variable name:",a[NAME]," Skipping."
		else:
			known[a[NAME]] = a

	sortedkeys = sorted(known.keys(),key=len, reverse=True)

	signsToRemove = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if (x,y,z) in box and t["id"].value == "Control":
				if progress:
					print "Processing command block at '",x,y,z,"'...",

				firstcommand = command = t["Command"].value

				#execute, tp, and playsound use relative coordinates that center on a player; disable relative coords for these
				if "execute" in command[:8] or "tp" in command[:3] or "playsound" in command[:10]:
					rel = False
				else:
					rel = relative

				#unpack all of the sign information we generated and sorted above
				for wp in sortedkeys:
					(waypoint, sx, sy, sz, sign, point2) = known[wp]
					
					#skip everything below if the variable isn't even in the command
					if waypoint not in command:
						continue

					#this is a tp command, and the user wants the player to face the direction the sign is
					if facing and "tp" in command[:3]:

						#only work with $ (world coordinates) directives
						if "$"+waypoint in command:
							coords = [str(sx), str(sy), str(sz)]
							command = replaceVariables(command, "$"+waypoint, " ".join(coords), sign)
							parts = command.split(" ")
							block = level.blockAt(sign["x"].value,sign["y"].value,sign["z"].value)
							blockdata = level.blockDataAt(sign["x"].value,sign["y"].value,sign["z"].value)

							#test for wall signs, which have different data values than standing signs
							if block == 68:
								blockdata = wallval[blockdata]

							#check the resulting command's parameter length, so that the Y rotation can be inserted
							#into the 6th (5th in the string from zero) slot. Also set the X rotation to 0 if it hasn't been set

							if len(parts) == 5: #no rotation values
								parts.append(str(rotvals[blockdata]))
								parts.append("0")
							elif len(parts) == 6: #just the Y rotation, add 0 for X
								if parts[5] != "~":
									parts[5] = str(rotvals[blockdata])
								parts.append("0")
							elif len(parts) == 7: #both Y and X rotation values; leave X alone
								if parts[5] != "~":
									parts[5] = str(rotvals[blockdata])

							#recombine the modified parts, now that the Y and X rotation for the TP command have been set
							command = " ".join(parts)

					if type(sx) == str:
						sx = x
					if type(sy) == str:
						sy = y
					if type(sz) == str:
						sz = z

					#if popint2 isn't an empty list, then there is a second sign that needs to be considered for a ## or $$ operation
					if point2:

						#unpack the second sign
						wp2,sx2,sy2,sz2,sign2,_ = point2

						if sx2 == None:
							sx2 = x
						if sy2 == None:
							sy2 = y
						if sz2 == None:
							sz2 = z
						
						#swap all coordinates so that sx/sy/sz are the smaller of the set
						if sx > sx2:
							sx, sx2 = sx2, sx
						if sy > sy2:
							sy, sy2 = sy2, sy
						if sz > sz2:
							sz, sz2 = sz2, sz

						block = level.blockAt(int(sx),int(sy),int(sz))
						data = level.blockDataAt(int(sx),int(sy),int(sz))
						if block in block_map:
							command = replaceVariables(command, "***"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
							command = replaceVariables(command, "**"+waypoint, str(block_map[block])+" "+str(data), sign)
							if block in levers: #levers and directional redstone blocks
								data = button_vals[data]
							elif block in plates: #pressure plates
								data ^= 1
							elif block in tripwires: #tripwire
								data = tripwire_vals[data]
							command = replaceVariables(command, "***^"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
							command = replaceVariables(command, "**^"+waypoint, str(block_map[block])+" "+str(data), sign)
						else:
							print "ERROR: Unidentified block '"+str(block)+"' at",sx,sy,sz,".  Please update the block_map variable with new block IDs."


						#handle particle commands, which use an x,y,z center point with a box width
						if "particle" in command[:9]:
							xWidth = float(sx2-sx)/4.0
							yWidth = float(sy2-sy)/4.0
							zWidth = float(sz2-sz)/4.0
							xCenter = (math.ceil(float((sx2+0.5)-(sx+0.5))/2.0))+sx
							yCenter = (math.ceil(float(sy2-sy)/2.0))+sy
							zCenter = (math.ceil(float((sz2+0.5)-(sz+0.5))/2.0))+sz
							particleCoords = str(xCenter)+" "+str(yCenter)+" "+str(zCenter)+" "+str(xWidth)+" "+str(yWidth)+" "+str(zWidth)

							oldcommand = command
							command = replaceVariables(command, "$$"+waypoint, particleCoords, sign)
							
							#if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
							if oldcommand != command:
								signsToRemove.append(sign2)

						#calculate relative coordinates
						if rel:
							rx = to_number(sx-x)
							ry = to_number(sy-y,True)
							rz = to_number(sz-z)
							rx2 = to_number(sx2-x)
							ry2 = to_number(sy2-y,True)
							rz2 = to_number(sz2-z)
							longCoords = "~"+" ~".join([str(rx), str(ry), str(rz), str(rx2), str(ry2), str(rz2)])
						else:
							longCoords = " ".join([str(sx), str(sy), str(sz), str(sx2), str(sy2), str(sz2)])
						oldcommand = command
						command = replaceVariables(command, "$$"+waypoint, longCoords, sign)
						#if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
						if oldcommand != command:
							signsToRemove.append(sign2)

						if rel:
							coords = "~"+" ~".join([str(rx2), str(ry2), str(rz2)])
						else:
							coords = " ".join([str(sx2), str(sy2), str(sz2)])
						oldcommand = command
						command = replaceVariables(command, "$>"+waypoint, coords, sign)						
						#if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
						if oldcommand != command:
							signsToRemove.append(sign2)

						if rel:
							coords = "~"+" ~".join([str(rx), str(ry), str(rz)])
						else:
							coords = " ".join([str(sx), str(sy), str(sz)])
						oldcommand = command
						command = replaceVariables(command, "$"+waypoint, coords, sign)						
						#if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
						if oldcommand != command:
							signsToRemove.append(sign2)

						oldcommand = command
						selCoords = "x="+str(int(sx))+",y="+str(int(sy))+",z="+str(int(sz))+",dx="+str(int(sx2-sx))+",dy="+str(int(sy2-sy))+",dz="+str(int(sz2-sz))
						command = replaceVariables(command, "##"+waypoint, selCoords, sign)
						if oldcommand != command:
							signsToRemove.append(sign2)

					#no second sign is associated with this one, continue on
					else:

						#the spreadplayers command only takes an X and Z coordinate; process it first here
						if "spreadplayers" in command[:14]:
							command = replaceVariables(command, "$"+waypoint, " ".join([str(sx), str(sz)]), sign)
						
						block = level.blockAt(int(sx),int(sy),int(sz))
						data = level.blockDataAt(int(sx),int(sy),int(sz))
						if block in block_map:
							command = replaceVariables(command, "***"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
							command = replaceVariables(command, "**"+waypoint, str(block_map[block])+" "+str(data), sign)
							if block in levers: #levers and directional redstone blocks
								data = button_vals[data]
							elif block in plates: #pressure plates
								data ^= 1
							elif block in tripwires: #tripwire
								data = tripwire_vals[data]
							command = replaceVariables(command, "***^"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
							command = replaceVariables(command, "**^"+waypoint, str(block_map[block])+" "+str(data), sign)
						else:
							print "ERROR: Unidentified block '"+str(block)+"' at",sx,sy,sz,".  Please update the block_map variable with new block IDs."

						#handy list for building coordinate strings using join
						coords = [str(sx), str(sy), str(sz)]

						#calculate relative coordinates
						if rel:
							rx = to_number(sx-x)
							ry = to_number(sy-y,True)
							rz = to_number(sz-z)
							longCoords = "~"+" ~".join([str(rx), str(ry), str(rz)])

						#or don't, whatever
						else:
							longCoords = " ".join(coords)

						#use the same sign for both coordinates for a $$ directive on a single sign
						command = replaceVariables(command, "$$"+waypoint, longCoords+" "+longCoords, sign)

						#do $ directives ( X Y Z )
						command = replaceVariables(command, "$"+waypoint, longCoords, sign)
						
						#use the same, zeroed coordinates for a $$ directive on a single sign
						shortCoords = "x="+str(int(sx))+",y="+str(int(sy))+",z="+str(int(sz))+",dx=0,dy=0,dz=0"
						command = replaceVariables(command, "##"+waypoint, shortCoords, sign)

						#do # directives ( X,Y,Z )
						shortCoords = ",".join([str(int(sx)), str(int(sy)), str(int(sz))])
						command = replaceVariables(command, "#"+waypoint, shortCoords, sign)

						#do % directives ( x:X,y:Y,z:Z )
						tagCoords = "x:"+str(int(sx))+",y:"+str(int(sy))+",z:"+str(int(sz))
						command = replaceVariables(command, "%"+waypoint, tagCoords, sign)

						#do & directives ( Pos:[Xf,Yf,Zf] )
						posCoords = "Pos:["+str(sx+0.5)+"d,"+str(sy)+"d,"+str(sz+0.5)+"d]"
						command = replaceVariables(command, "&"+waypoint, posCoords, sign)
				if firstcommand != command:
					if progress:
						print "modifications made."
					t["Command"] = TAG_String(command)
					chunk.dirty = True
				else:
					if progress:
						print "no modificatons made."
					pass
	
	#remove the found signs in a truly inefficient and hideously slow way, because MCEdit was leaving
	#tile entities behind for no good fucking reason
	for sign in signsToRemove:
		x = sign["x"].value
		y = sign["y"].value
		z = sign["z"].value
		chunk = level.getChunk(x/16,z/16)
		te = level.tileEntityAt(x,y,z)
		if te in chunk.TileEntities:
			chunk.TileEntities.remove(te)
			level.setBlockAt(x, y, z, 0)
			level.setBlockDataAt(x, y, z, 0)
			chunk.dirty = True
		