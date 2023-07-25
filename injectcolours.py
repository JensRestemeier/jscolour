import argparse
import re
import os.path

def injectColours(mapPath:str, entPath:str, outmapPath:str):
    # extract light colours from ent file:
    lights = {}
    entity = None
    with open(entPath, "rt") as f:
        entity = None
        for line in f.readlines():
            line = line.strip()
            if line == "{":
                entity = {}
            elif line == "}":
                try:
                    origin = tuple([int(x) for x in entity["origin"].split(" ")])
                    color = tuple([int(x) for x in entity["_color"].split(" ")])
                    lights[origin] = color
                except KeyError:
                    pass
            else:
                v = re.findall(r"\"([^\"]*)\"", line)
                if len(v) > 1:
                    entity[v[0]] = v[1:] if len(v) > 2 else v[1]

    # insert light colours into map file:
    level = 0
    lines = []
    with open(mapPath, "rt") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "{":
                if level == 0:
                    entity = {}
                level += 1
            elif line == "}":
                level -= 1
                if level == 0:
                    try:
                        origin = tuple([int(x) for x in entity["origin"].split(" ")])
                        if "_color" not in entity:
                            lines.append("\"_color\" \"%i %i %i\"\n" % lights[origin])
                    except KeyError:
                        pass
            elif level == 1:
                v = re.findall(r"\"([^\"]*)\"", line)
                if len(v) > 1:
                    entity[v[0]] = v[1:] if len(v) > 2 else v[1]
            lines.append("%s\n" % line)

    # write modified map:
    outmapDir = os.path.dirname(outmapPath)
    if outmapDir:
        os.makedirs(outmapDir, exist_ok=True)
    with open(outmapPath, "wt") as f:
        f.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description='Inject light colours into a map')
    parser.add_argument('mapfile', help='which map file to operate on')
    parser.add_argument('--ent', type=str, help='input entity file')
    parser.add_argument('--out', type=str, help='output map file')

    args = parser.parse_args()
    mapfile = args.mapfile
    filename,ext = os.path.splitext(mapfile)
    if args.ent:
        entfile = args.ent
    else:
        entfile = filename + ".ent"
    if args.out:
        outfile = args.out
    else:
        outfile = filename + "_out" + ext
    injectColours(mapfile, entfile, outfile)

if __name__ == "__main__":
	main()
