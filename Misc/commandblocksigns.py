# coding unicode-escape
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String

displayName = "Command Block Signs"

def perform(level, box, options):
	waypoints = []
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz and t["id"].value == "Sign":
				waypoint = None
				validWaypoint = False
				for linenum in range(1, 5):
					line = t["Text" + str(linenum)].value
					if len(line) == 0:
						continue
					if line.find(" ") != -1:
						validWaypoint = False
						break
					if waypoint != None:
						validWaypoint = False
						break
						
					waypoint = line
					validWaypoint = True
				
				if validWaypoint:
					waypoints.append((waypoint, x, y, z, t, chunk))
	
	print waypoints
	
	waypoints.sort(key=lambda (w, x, y, z, t, c): -len(w))
	
	print waypoints
	
	signsToRemove = []
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz and t["id"].value == "Control":
				command = t["Command"].value
				
				for (waypoint, sx, sy, sz, sign, signChunk) in waypoints:
					coords = [str(sx), str(sy), str(sz)]
					shortCoords = ",".join(coords)
					frags = command.split("#" + waypoint)
					if len(frags) > 1:
						command = shortCoords.join(frags)
						signsToRemove.append((sx, sy, sz, sign, signChunk))
					
					longCoords = " ".join(coords)
					frags = command.split("$" + waypoint)
					if len(frags) > 1:
						command = longCoords.join(frags)
						signsToRemove.append((sx, sy, sz, sign, signChunk))
				
				t["Command"] = TAG_String(command)
				
				chunk.dirty = True
	
	for signData in signsToRemove:
		print "SignData:" + str(signData)
		(x, y, z, sign, signChunk) = signData
		if sign in signChunk.TileEntities:
			signChunk.TileEntities.remove(sign)
			level.setBlockAt(x, y, z, 0)
			signChunk.dirty = True
		