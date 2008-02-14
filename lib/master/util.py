#!/usr/bin/env python


def mapit(dict,map,prefix):
	"""mapit(dict,map,prefix) -> dictionary
	copy data from dictionary according to map, while prepending prefix
	"""

	infos={}
	for key in dict.keys():
		if key in map.keys():
			infos[prefix+"."+map[key]]=dict[key]

	return infos
	
def doLineParse(lines,prefix,map):
	"""doLineParse(lines,prefix,map) => dictionary

	parse out lines with colons ':' specifying the fields
	lines - list of lines.
	prefix - what to prepend to the keys in the dictionary.
	map - dictionary map of what will be on each line before the :, and what it maps to in the returned dictionary

	all lines not recognized are ignored, and if no lines are recognized the function returns an empty dictionary

	example:
		lines = ["Fun Number:  42\n","Funnyer Number: 8008"]
		map = {"Fun Number":"fun", "Funnyer Number":"funnyer"}
		prefix = "super"
		Return Value: {'super.fun':'42','super.funnyer':'8008'}
	"""

	infos={}
	for line in lines:
		try:
			(first,second) = line.split(':',1)
			infos[prefix+"."+map[first.strip()]]=second.strip()
		except (ValueError,KeyError):
			pass	#split error (no colon in line) or first not in map

	return infos
