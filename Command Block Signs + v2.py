# coding unicode-escape
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from copy import deepcopy
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Double, TAG_String
import math
## displayName = ""

VERSION = "v2"
UPDATE_URL = ""

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
            (
            "\n"
            "Outputs:\n"
            "\t$\t0 0 0\n"
            "\t$$\t 0 0 0 0 0 0\n"
            "\n"
            "\t#\t 0,0,0\n"
            "\t##\tx=0,y=0,z=0,dx=0,dy=0,dz=0\n"
            "\n"
            "\t%\tx:0,y:0,z:0\n"
            "\t&\t Pos:[0d,0d,0d]\n"
            "\n"
            "\t*\t minecraft:ID DATA\n"
            "\t**\t id:\"minecraft:ID\",Damage:DATAs\n"
            ,"label"),
            ("Sign facing determines [<y-rot> <x-rot>] for /tp",True),
            ("Mode:",("Absolute Coordinates","Relative Coordinates")),
            ("","label"),
            ),
              
            (("Details","title"),
            (
            "Output:\n"
            "\t$<VARIABLE>\n"
            "\n"
            "Sign format:\n"
            "\t1st line:\t<VARIABLE>\n"
            "\t2nd line:\t+/-x or ~ [optional]\n"
            "\t3rd line:\t+/-y or ~ [optional]\n"
            "\t4th line:\t+/-z or ~ [optional]\n"
            "\n"
            "-----------------------\n"
            "\n"
            "Adding + or - (for $):\n"
            "\t$\tAverage\n"
            "\t$-\t Lowest point\n"
            "\t$+\tHighest point\n"
            "\t$$\t Square area\n"
            "\n"
            "Adding + or - (for *, **):\n"
            "\t*\t Block\n"
            "\t*+\tBlock's powered state\n"
            "\t*-\t  Block's unpowered state\n"
            "\t*^\t Block's toggled state\n"
            "","label")),
            
            (("About","title"),
            (
            "To Use:\n"
            "Place a sign at the location you want the output to work for."
            "<VARIABLE> can be anything you want (eg. TEST)."
            "You can also have a sign \"point\" to a location by adding or subtracting "
            "from the coordinates using the sign's 2nd, 3rd, and/or 4th lines.\n"
            "\n"
            "There can be 2 OR MORE signs with <VARIABLE> "
            "and all signs found will be taken into account.\n"
            "\n"
            "-----------------------\n"
            "\n"
            "This is a modified version of SethBling's Command Block Signs filter "
            "edited at TrazLander's request. It has gone through several iterations, "
            "with work done by texelelf, Asdjke, texelelf again, and Naor2013. \n"
            "Thanks for all their help making this, and all other's feedback in creating this.\n"
            "\n"
            "","label"),
            ("Output progress to console",False),),
            ] 

levers = [28,69,77,131,143]
plates = [70,72,147,148]
tripwires = [132]

rotvals = [0,22.5,45,67.5,90,112.5,135,157.5,180,-157.5,-135,-112.5,-90,-67.5,-45,-22.5]
wallval = {2:8,3:0,4:4,5:12}

lever_vals = [8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7]
tripwire_vals = {0:1,2:3,6:7,1:0,3:2,7:6}

def to_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return 0

def fixCoords(x, y, z):
    try:
        if int(y) == float(y):
            y = int(y)
        else:
            y = float(y)
    except:
        pass

    try:
        if int(x) == float(x)-0.5:
            x = int(x)
        else:
            x = float(x)
    except:
        pass

    try:
        if int(z) == float(z)-0.5:
            z = int(z)
        else:
            z = float(z)
    except:
        pass

    finally:
        return x, y, z

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
    facing = options["Sign facing determines [<y-rot> <x-rot>] for /tp"]
    relative = True if options["Mode:"] == "Relative Coordinates" else False
    
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
    for a in waypoints:
        if "Text2" in a[SIGN]:
            if a[SIGN]["Text2"].value.replace("\"","")[:1] == "~":
                a[XVAL] = str(a[SIGN]["Text2"].value.replace("\"",""))
            else:
                ox = to_number(a[SIGN]["Text2"].value.replace("\"",""))
                a[XVAL] += ox if ox == int(ox) else ox + 0.5
        if "Text3" in a[SIGN]:
            if a[SIGN]["Text3"].value.replace("\"","")[:1] == "~":
                a[YVAL] = str(a[SIGN]["Text3"].value.replace("\"",""))
            else:
                a[YVAL] += to_number(a[SIGN]["Text3"].value.replace("\"",""))
        if "Text4" in a[SIGN]:
            if a[SIGN]["Text4"].value.replace("\"","")[:1] == "~":
                a[ZVAL] = str(a[SIGN]["Text4"].value.replace("\"",""))
            else:
                oz = to_number(a[SIGN]["Text4"].value.replace("\"",""))
                a[ZVAL] += oz if oz == int(oz) else oz + 0.5


        #check to see if we've already found this sign; if so, add the sign to the existing sign at its end.  If not, add the
        #sign to the list.
        if a[NAME] in known:
            if not known[a[NAME]][NEXT]:
                known[a[NAME]][NEXT] = [deepcopy(a), ] #deepcopy, so we don't lose signs with waypoints.remove
            else:
                known[a[NAME]][NEXT].append(deepcopy(a))
        else:
            known[a[NAME]] = a

    sortedkeys = sorted(known.keys(),key=len, reverse=True)

    signsToRemove = []
    parameters = relative, sortedkeys, known, progress, facing, level
    for (chunk, _, _) in level.getChunkSlices(box):
        for t in chunk.TileEntities:
            x = t["x"].value
            y = t["y"].value
            z = t["z"].value
            
            if (x,y,z) in box and t["id"].value == "Sign":
                if "Text1" in t:
                    line = t["Text1"].value.replace("\"", "")
                    if "run_command" in line:
                        result = useLine(t["Text1"].value, chunk, (x, y, z), parameters)
                        if result:
                            t["Text1"] = result
                if "Text2" in t:
                    line = t["Text2"].value.replace("\"", "")
                    if "run_command" in line:
                        result = useLine(t["Text2"].value, chunk, (x, y, z), parameters)
                        if result:
                            t["Text2"] = result
                if "Text3" in t:
                    line = t["Text3"].value.replace("\"", "")
                    if "run_command" in line:
                        result = useLine(t["Text3"].value, chunk, (x, y, z), parameters)
                        if result:
                            t["Text3"] = result
                if "Text4" in t:
                    line = t["Text4"].value.replace("\"", "")
                    if "run_command" in line:
                        result = useLine(t["Text4"].value, chunk, (x, y, z), parameters)
                        if result:
                            t["Text4"] = result

            if (x,y,z) in box and t["id"].value == "Control":
                if progress:
                    print "Processing command block at '",x,y,z,"'...",
                result = useLine(t["Command"].value, chunk, (x, y, z), parameters)
                if result:
                        t["Command"] = result

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

def removeSigns(signs):
    for sign in signs:
        signsToRemove.append(sign)

                
def useLine(command, chunk, (x, y, z), (relative, sortedkeys, known, progress, facing, level)):
    global signsToRemove
    firstcommand = command

    #execute and tp use relative coordinates that center on a player; disable relative coords for these
    if "execute" in command[:8] or "tp" in command[:3]:
        rel = False
    else:
        rel = relative

    #unpack all of the sign information we generated and sorted above
    for wp in sortedkeys:
        (waypoint, sx, sy, sz, sign, point2) = known[wp]
        
        #skip everything below if the variable isn't even in the command
        if waypoint not in command:
            continue

        tpIndex = command.find("tp ")

        #this is a tp command, and the user wants the player to face the direction the sign is
        if facing and tpIndex != -1:

            #only work with $ directives
            if "$"+waypoint in command:
                block = level.blockAt(sign["x"].value,sign["y"].value,sign["z"].value)
                blockdata = level.blockDataAt(sign["x"].value,sign["y"].value,sign["z"].value)

                #test for wall signs, which have different data values than standing signs
                if block == 68:
                    blockdata = wallval[blockdata]

                #check the resulting command's parameter length, so that the Y rotation can be inserted
                #into the 6th (5th in the string from zero) slot. Also set the X rotation to 0 if it hasn't been set

                before = command[:tpIndex]
                tempCommand = command[tpIndex:]
                parts = tempCommand.split(" ")
                partsLen = len(parts)
                if partsLen >= 3 and "$" in parts[2]:
                    if partsLen >= 4 and len(parts[3]) > 0 and parts[3][0] in "~0123456789":
                        if partsLen >= 5 and len(parts[4]) > 0 and parts[4][0] in "~0123456789":
                            pass
                        else:
                            for i, c in enumerate(parts[3]):
                                if c not in "~0123456789":
                                    parts[3] = parts[3][:i] + " 0" + parts[i:]
                                    break;
                    else:
                        parts[2] = parts[2].replace("$"+waypoint, "$"+waypoint+" "+str(rotvals[blockdata])+" 0")

                #recombine the modified parts, now that the Y and X rotation for the TP command have been set
                command = before + " ".join(parts)

        if type(sx) == str and sx != "~":
            sx = x
        if type(sy) == str and sy != "~":
            sy = y
        if type(sz) == str and sz != "~":
            sz = z

        #if point2 isn't an empty list, then there is a second sign that needs to be considered for a ## or $$ operation
        if point2:
            #unpack the second sign
            sx2 = sy2 = sz2 = None
            signsToMayRemove = []

            for p in point2:
                _, tsx ,tsy ,tsz, sign2, _ = p
                if tsx == None or (type(tsx) == str and tsx != "~"):
                    tsx = x
                if tsy == None or (type(tsy) == str and tsy != "~"):
                  tsy = y
                if tsz == None or (type(tsz) == str and tsz != "~"):
                   tsz = z

                if sx2 is None:
                    if sx == "~" or tsx == "~":
                        sx = sx2 = "~"
                    elif sx > tsx:
                        sx, sx2 = tsx, sx
                    else:
                        sx2 = tsx
                if sy2 is None:
                    if sy == "~" or tsy == "~":
                        sy = sy2 = "~"
                    elif sy > tsy:
                        sy, sy2 = tsy, sy
                    else:
                        sy2 = tsy
                if sz2 is None:
                    if sz == "~" or tsz == "~":
                        sz = sz2 = "~"
                    elif sz > tsz:
                        sz, sz2 = tsz, sz
                    else:
                        sz2 = tsz

                if sx2 != "~" and tsx != "~" and tsx > sx2:
                    sx2 = tsx
                if sy2 != "~" and tsy != "~" and tsy > sy2:
                    sy2 = tsy
                if sz2 != "~" and tsz != "~" and tsz > sz2:
                    sz2 = tsz

                if sx != "~" and tsx != "~" and tsx < sx:
                    sx = tsx
                if sy != "~" and tsy != "~" and tsy < sy:
                    sy = tsy
                if sz != "~" and tsz != "~" and tsz < sz:
                    sz = tsz

                signsToMayRemove.append(sign2)

            average = []
            if sx == "~" or sx2 == "~":
                average.append("~")
            else:
                average.append((float(sx)+float(sx2)+1)/2)
            if sy == "~" or sy2 == "~":
                average.append("~")
            else:
                average.append((float(sy)+float(sy2))/2)
            if sz == "~" or sz2 == "~":
                average.append("~")
            else:
                average.append((float(sz)+float(sz2)+1)/2)
            average = fixCoords(average[0], average[1], average[2])
            
            if sx == "~" or sx2 == "~" or sy == "~" or sy2 == "~" or sz == "~" or sz2 == "~":
                telda = True
            else:
                telda = False
            if not telda:
                block = level.blockAt(int(sx),int(sy),int(sz))
                data = level.blockDataAt(int(sx),int(sy),int(sz))
                if block in block_map:
                    if block in levers and data>=0 and data<=7:
                        positive = False
                    elif block in plates and data==0:
                        positive = False
                    elif block in tripwires and data>=0 and data<=14 and data%2==0:
                        positive = False
                    else:
                        positive = True

                    if positive:
                        command = replaceVariables(command, "**+"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                        command = replaceVariables(command, "*+"+waypoint, str(block_map[block])+" "+str(data), sign)
                        if block in levers: #levers and directional redstone blocks
                            tempData = lever_vals[data]
                        elif block in plates: #pressure plates
                            tempData = data ^ 1
                        elif block in tripwires: #tripwire
                            tempData = tripwire_vals[data]
                        else:
                            tempData = data
                        command = replaceVariables(command, "**-"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(tempData)+"s", sign)
                        command = replaceVariables(command, "*-"+waypoint, str(block_map[block])+" "+str(tempData), sign)
                    else:
                        command = replaceVariables(command, "**-"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                        command = replaceVariables(command, "*-"+waypoint, str(block_map[block])+" "+str(data), sign)
                        if block in levers: #levers and directional redstone blocks
                            tempData = lever_vals[data]
                        elif block in plates: #pressure plates
                            tempData = data ^ 1
                        elif block in tripwires: #tripwire
                            tempData = tripwire_vals[data]
                        else:
                            tempData = data
                        command = replaceVariables(command, "**+"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(tempData)+"s", sign)
                        command = replaceVariables(command, "*+"+waypoint, str(block_map[block])+" "+str(tempData), sign)

                    command = replaceVariables(command, "**"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                    command = replaceVariables(command, "*"+waypoint, str(block_map[block])+" "+str(data), sign)
                    if block in levers: #levers and directional redstone blocks
                        data = lever_vals[data]
                    elif block in plates: #pressure plates
                        data ^= 1
                    elif block in tripwires: #tripwire
                        data = tripwire_vals[data]
                    command = replaceVariables(command, "**^"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                    command = replaceVariables(command, "*^"+waypoint, str(block_map[block])+" "+str(data), sign)
                else:
                    print "ERROR: Unidentified block '"+str(block)+"' at",sx,sy,sz,".  Please update the block_map variable with new block IDs."

            #handle particle commands, which use an x,y,z center point with a box width
            if "particle" in command[:9]:
                if sx == "~" or sx2 == "~":
                    xWidth = 0
                    xCenter = "~"
                else:
                    xWidth = float(sx2-sx)/4.0
                    xCenter = (math.ceil(float((sx2+0.5)-(sx+0.5))/2.0))+sx
                if sy == "~" or sy2 == "~":
                    yWidth = 0
                    yCenter = "~"
                else:
                    yWidth = float(sy2-sy)/4.0
                    yCenter = (math.ceil(float(sy2-sy)/2.0))+sy
                if sz == "~" or sz2 == "~":
                    zWidth = 0
                    zCenter = "~"
                else:
                    zWidth = float(sz2-sz)/4.0
                    zCenter = (math.ceil(float((sz2+0.5)-(sz+0.5))/2.0))+sz                

                particleCoords = str(xCenter)+" "+str(yCenter)+" "+str(zCenter)+" "+str(xWidth)+" "+str(yWidth)+" "+str(zWidth)

                oldcommand = command
                command = replaceVariables(command, "$$"+waypoint, particleCoords, sign)
                
                #if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
                if oldcommand != command:
                    removeSigns(signsToMayRemove)

            #calculate relative coordinates
            if rel:
                if sx == "~" or sx2 == "~":
                    rx = "~"
                    rx2 = "~"
                else:
                    rx = "~" + str(to_number(sx-x))
                    rx2 = "~" + str(to_number(sx2-x))
                if sy == "~" or sy2 == "~":
                    ry = "~"
                    ry2 = "~"
                else:
                    ry = "~" + str(to_number(sy-y))
                    ry2 = "~" + str(to_number(sy2-y))
                if sz == "~" or sz2 == "~":
                    rz = "~"
                    rz2 = "~"
                else:
                    rz = "~" + str(to_number(sz-z))
                    rz2 = "~" + str(to_number(sz2-z))
                longCoords = " ".join([rx, ry, rz, rx2, ry2, rz2])
            else:
                longCoords = " ".join([str(sx), str(sy), str(sz), str(sx2), str(sy2), str(sz2)])
            oldcommand = command
            command = replaceVariables(command, "$$"+waypoint, longCoords, sign)

            #if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
            if oldcommand != command:
                removeSigns(signsToMayRemove)

            if rel:
                coords = " ".join([rx2, ry2, rz2])
            else:
                coords = " ".join([str(sx2), str(sy2), str(sz2)])
            oldcommand = command
            command = replaceVariables(command, "$+"+waypoint, coords, sign)

            #if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
            if oldcommand != command:
                removeSigns(signsToMayRemove)

            if rel:
                coords = " ".join([rx, ry, rz])
            else:
                coords = " ".join([str(sx), str(sy), str(sz)])
            oldcommand = command
            command = replaceVariables(command, "$-"+waypoint, coords, sign)

            #if modified, add the second sign to the list of signs to be removed as well (replaceVariable handles the first)
            if oldcommand != command:
                removeSigns(signsToMayRemove)

            if rel:
                if average[0] == "~":
                    rx = "~"
                else:
                    rx = "~" + str(to_number(average[0]-x))
                if average[1] == "~":
                    ry = "~"
                else:
                    ry = "~" + str(to_number(average[1]-y))
                if average[2] == "~":
                    rz = "~"
                else:
                    rz = "~" + str(to_number(average[2]-z))
                coords = " ".join([rx, ry, rz])
            else:
                coords = " ".join([str(average[0]), str(average[1]), str(average[2])])
            oldcommand = command
            command = replaceVariables(command, "$"+waypoint, coords, sign)
            if oldcommand != command:
                removeSigns(signsToMayRemove)

            oldcommand = command
            if not telda:
                selCoords = "x="+str(int(sx))+",y="+str(int(sy))+",z="+str(int(sz))+",dx="+str(int(sx2)-int(sx))+",dy="+str(int(sy2)-int(sy))+",dz="+str(int(sz2)-int(sz))
                command = replaceVariables(command, "##"+waypoint, selCoords, sign)
                if oldcommand != command:
                    removeSigns(signsToMayRemove)

                oldcommand = command
                shortCoords = ",".join([str(int(average[0])), str(int(average[1])), str(int(average[2]))])
                command = replaceVariables(command, "#"+waypoint, shortCoords, sign)
                if oldcommand != command:
                    removeSigns(signsToMayRemove)

                oldcommand = command
                tagCoords = "x:"+str(int(average[0]))+",y:"+str(int(average[1]))+",z:"+str(int(average[2]))
                command = replaceVariables(command, "%"+waypoint, tagCoords, sign)
                if oldcommand != command:
                    removeSigns(signsToMayRemove)

                oldcommand = command
                posCoords = "Pos:["+str(average[0]+0.5)+"d,"+str(average[1])+"d,"+str(average[2]+0.5)+"d]"
                command = replaceVariables(command, "&"+waypoint, posCoords, sign)
                if oldcommand != command:
                    removeSigns(signsToMayRemove)

        #no second sign is associated with this one, continue on
        else:
            #the spreadplayers command only takes an X and Z coordinate; process it first here
            if "spreadplayers" in command[:14]:
                command = replaceVariables(command, "$"+waypoint, " ".join([str(sx), str(sz)]), sign)
            
            if sx == "~" or sy == "~" or sz == "~":
                telda = True
            else:
                telda = False

            if not telda:
                block = level.blockAt(int(sx),int(sy),int(sz))
                data = level.blockDataAt(int(sx),int(sy),int(sz))
                if block in block_map:
                    if block in levers and data>=0 and data<=7:
                        positive = False
                    elif block in plates and data==0:
                        positive = False
                    elif block in tripwires and data>=0 and data<=14 and data%2==0:
                        positive = False
                    else:
                        positive = True

                    if positive:
                        command = replaceVariables(command, "**+"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                        command = replaceVariables(command, "*+"+waypoint, str(block_map[block])+" "+str(data), sign)
                        if block in levers: #levers and directional redstone blocks
                            tempData = lever_vals[data]
                        elif block in plates: #pressure plates
                            tempData = data ^ 1
                        elif block in tripwires: #tripwire
                            tempData = tripwire_vals[data]
                        else:
                            tempData = data
                        command = replaceVariables(command, "**-"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(tempData)+"s", sign)
                        command = replaceVariables(command, "*-"+waypoint, str(block_map[block])+" "+str(tempData), sign)
                    else:
                        command = replaceVariables(command, "**-"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                        command = replaceVariables(command, "*-"+waypoint, str(block_map[block])+" "+str(data), sign)
                        if block in levers: #levers and directional redstone blocks
                            tempData = lever_vals[data]
                        elif block in plates: #pressure plates
                            tempData = data ^ 1
                        elif block in tripwires: #tripwire
                            tempData = tripwire_vals[data]
                        else:
                            tempData = data
                        command = replaceVariables(command, "**+"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(tempData)+"s", sign)
                        command = replaceVariables(command, "*+"+waypoint, str(block_map[block])+" "+str(tempData), sign)
                    command = replaceVariables(command, "**"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                    command = replaceVariables(command, "*"+waypoint, str(block_map[block])+" "+str(data), sign)
                    if block in levers: #levers and directional redstone blocks
                        data = lever_vals[data]
                    elif block in plates: #pressure plates
                        data ^= 1
                    elif block in tripwires: #tripwire
                        data = tripwire_vals[data]
                    command = replaceVariables(command, "**^"+waypoint, "id:\""+str(block_map[block])+"\",Damage:"+str(data)+"s", sign)
                    command = replaceVariables(command, "*^"+waypoint, str(block_map[block])+" "+str(data), sign)
                else:
                    print "ERROR: Unidentified block '"+str(block)+"' at",sx,sy,sz,".  Please update the block_map variable with new block IDs."

            #handy list for building coordinate strings using join
            coords = [str(sx), str(sy), str(sz)]

            #calculate relative coordinates
            if rel:
                if sx == "~":
                    rx = "~"
                else:
                    rx = "~" + str(to_number(sx-x))
                if sy == "~":
                    ry = "~"
                else:
                    ry = "~" + str(to_number(sy-y))
                if sz == "~":
                    rz = "~"
                else:
                    rz = "~" + str(to_number(sz-z))
                longCoords = " ".join([rx, ry, rz])
            #or don't, whatever
            else:
                longCoords = " ".join(coords)

            #use the same sign for both coordinates for a $$ directive on a single sign
            command = replaceVariables(command, "$$"+waypoint, longCoords+" "+longCoords, sign)

            if rel:
                coords = " ".join([rx, ry, rz])
            else:
                coords = " ".join(coords)

            command = replaceVariables(command, "$+"+waypoint, coords, sign)

            command = replaceVariables(command, "$-"+waypoint, coords, sign)

            #do $ directives ( X Y Z )
            command = replaceVariables(command, "$"+waypoint, longCoords, sign)
            
            if not telda:
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
        chunk.dirty = True
        return TAG_String(command)
    if progress:
        print "no modificatons made."
    return None