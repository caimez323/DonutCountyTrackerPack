import re
import json
import html
from pathlib import Path


def display_name_item_from_subregion(list):
    for elem in list:
        print(elem[5])

# Json Path is the json path to location
#this region is :{
# "region" : "code"
# "sub1" : [row]
# "sub2" : [row]

def normalise(s):
    return re.sub(r"[^a-z0-9]", "", html.unescape(s).lower())

def add_acces_rule(section,codes):
    if isinstance(codes,str):
        codes = [codes]
    rules = [r for r in (section.get("access_rules") or []) if r.strip()]
    #emtpy
    if not rules:
        section["access_rules"] = [",".join(codes)]
        return
    #else
    new_rules = []
    for r in rules:
        parts = [p.strip() for p in r.split(",")]
        missing = [c for c in codes if c not in parts]
        new_rules.append(",".join([r] + missing) if missing else r)
    section["access_rules"] = new_rules


#Manually is easier for now
ZONE_ORDER ={
    "Potters Rock" : ["Intro","Front","Potter","Pots","Launch","Collect"]
}

CHILD_TO_KEY = {
        "Pile": "Intro"
}


def zone_codes(zone,order,lookup):
    if zone not in order:
        return []
    codes = set()
    for prev in order[:order.index(zone)]:
        for trash_type in lookup.get(prev, {}).values():
            codes.add("trash_" + trash_type.lower())
    return sorted(codes)


def update_level(jsonPath,thisRegion):
    #ONLY TRASH FOR NOW
    #Need to add another
     
    INDEX_NAME = 5
    INDEX_TYPE = 6
    jsonData=[]
    with open(jsonPath,encoding="utf-8") as f:
        jsonData = json.load(f)
    path = Path(jsonPath)
    lookup = {}
    for zone, rows in thisRegion.items():
        if not isinstance(rows,list):
            continue #For the first one eg
        lookup[zone] = {normalise(r[INDEX_NAME]): r[INDEX_TYPE] for r in rows}
    print(lookup)

    for loc in jsonData:
        order = ZONE_ORDER.get(loc["name"],[])
        
        
        for child in loc.get("children", []):
            zone = CHILD_TO_KEY.get(child["name"], child["name"])
            zone_map = lookup.get(zone, {})

            own_all = sorted({"trash_" + t.lower() for t in zone_map.values()})
            prev = zone_codes(zone, order, lookup)

            for section in child.get("sections", []):
                # if it is the header, it need all below
                if normalise(section["name"]) == normalise(child["name"]):
                    add_acces_rule(section, own_all + [c for c in prev if c not in own_all])
                    continue

                trash_type = zone_map.get(normalise(section["name"]))
                if trash_type is None:
                    continue
                #trash_flour_icingbag
                if trash_type.lower() == "flourbag": trash_type = "flour_icingbag"
                own_code = "trash_" + trash_type.lower()
                add_acces_rule(section, [own_code] + [c for c in prev if c != own_code])

    with open(jsonPath,'w',encoding="utf-8") as f:
        json.dump(jsonData,f,indent=4)
        f.write("\n")







def get_connection_logic():
    logic_lines = []
    # GET FROM REGIONSLOGIC.JSON, MANUALLY UPDATE IT

    # with open("logic.xml") as logic_file:
    #     logic_lines = logic_file.readlines()
    # startIndex = 0
    # while "ss:Name=\"regions\"" not in logic_lines[startIndex]: startIndex+=1
    # currIndex = startIndex+10

    # regions_rows = []
    # thisRow= []
    # while "Worksheet" not in logic_lines[currIndex]:
    #     thisLine = logic_lines[currIndex]
    #     if "Row" in thisLine:
    #         regions_rows.append(thisRow)
    #         thisRow = []
        
    #     if "<Cell" in thisLine:
    #         if "<Cell ss:StyleID=\"" in thisLine:
    #             currIndex+=1
    #             continue
    #         indexGetted = None
    #         if "ss:Index=" in thisLine:
    #             indexGetted = int(thisLine.split("Index=\"")[1][0])
    #         if indexGetted and len(thisRow) != indexGetted:
    #             #On rajoute la diff
    #             for i in range(indexGetted-len(thisRow)-1):
    #                 thisRow.append("")
    #         content = thisLine.split(">")[2].split("<")[0]
    #         thisRow.append(content)
    #     currIndex+=1

    # #filter
    # regions_rows_filtered = []
    # for row in list(regions_rows):
    #     print(len(row))
    #     print(row)
    #     if len(row)<4 or row[3] not in ["Segment","Delivry","Logic"]:
    #         continue
    #     regions_rows_filtered.append(row)
    # print(regions_rows_filtered)


    # # [ {Zone : Contrainte}, [{sub : contrainte},{sub}],
    # regions_organized = []
    # organizedIndex = -1
    # for region in regions_rows_filtered:
    #     if region[6].strip() is not "":
    #         organizedIndex +=1
    #         regions_organized[regions_organized]


## FIRST WE PARSE THE LOGIC FILE

#Get the file
logic_lines = []
with open("logic.xml") as logic_file:
    logic_lines = logic_file.readlines()

# Get to the trashsanity part, for now I just want to stick to that
startIndex = 0
while "ss:Name=\"trashsanity\"" not in logic_lines[startIndex]: startIndex+=1

# Get to first row
while "<Row>" not in logic_lines[startIndex]: startIndex+=1

reconstructed_rows = []
thisRow = []
currIndex = startIndex + 1
#To get 1 row

while "999ft" not in logic_lines[currIndex]:
    # For each group
    if thisRow :
        reconstructed_rows.append(thisRow)
    thisRow = []
    while "<Row>" not in logic_lines[currIndex]: 
        thisLine = logic_lines[currIndex]
        if thisLine.strip() in ["<Cell>","</Cell>"] :
            continue
        if "</Row>" in thisLine:
            break


        # Si à côté de la cell on voit ss:Index ="X", on doit calculer la différence par rapport à la taille de thisRow
        indexGetted = None
        if "ss:Index=" in thisLine:
            indexGetted = int(thisLine.split("Index=\"")[1][0])
        if indexGetted and len(thisRow) != indexGetted:
            #On rajoute la diff
            for i in range(indexGetted-len(thisRow)-1):
                thisRow.append("")
        content = thisLine.split(">")[2].split("<")[0]
        thisRow.append(content)
        currIndex+=1
    currIndex+=1

print("==== End of Parsing")

with open("Rows.txt", "w") as f:
  for r in reconstructed_rows:
    thisLine = ",".join(r)
    f.write(thisLine+"\n")


#Now we need to build the logic

print("==== Starting logic")

# Id, scene (or parent), index (osef), name, parent, visual, type, region, dependant, rules

REGION_CODE_CORRESPONDANCE = {
    "scn_mom_house_merged" : "mirashouse",
    "scn_home_potter": "pottersrock",
    "scn_leaving_desert_snakes": "rangerstation",
    "scn_river" : "riverbed",
    "scn_popcorn_simple" : "campground",
    "scn_bunnies"  :"hopperspring",
    "scn_joshuatrees" : "joshuatree",
    "scn_fireworks" : "beachlotc",
    "scn_coco_house" : "geckopark",
    "scn_chickenbarn" : "chickenbarn",
    "scn_frog2" : "honeynutforest",
    "sbx_soup" : "catsoup",
    "scn_donutshop" : "donutshop",
    "scn_flashlight" : "abandonedhouse",
    "scn_waterpark" : "raccoonlagoon",
    "scn_405" : "the405",
    "scn_hq_interior" : "raccoonhq",
    }

regions_list = []
for row in reconstructed_rows :
    thisRegion = {}
    thisRegionName = None
    if row[1]:
        regions_list.append(thisRegion)
        #start of this regions
        thisRegionName = row[1]
        if thisRegionName in ["scene","titlescreen"]:
            thisRegionName = None
            continue
        thisRegion[thisRegionName] = []
    else:
        if not thisRegionName:
            continue
        thisRegion[thisRegionName].append(row)

#Add the regions items levels

regions_levels = []
for region in regions_list:
    if region == {}:
        continue
    thisDict = {}
    for k,v in region.items():
        if k :
            thisDict[k] = REGION_CODE_CORRESPONDANCE[k]
    regions_levels.append(thisDict)


#Now we need to add the content (could be doable early but it is easier to structure that way)

lastRegionName = None
brokenRows= []
SUB_REGION_CORRECTION = {
    "hs1" : "Bunnies 1 & 2", 
    "hs2" : "Bunnies 3 & 4",
    "hs3" : "Bunnies 5 & 6", 
    "tko1" : "Donut 1-3",
    "tko2" : "Donut 4-6",
    "tko3" : "Donut 7-8",
    "tkoCollect" : "Final Donut",
    "bf1" : "Phase 1",
    "bf2" : "Phase 2",
    }
    

for row in reconstructed_rows[1:]:
    if row[1]: #if there is a region
        lastRegionName = row[1]

    # Each row look for its parent
    if len(row)<=7: #We need to skip this row, it is probably a joint, or a broken props
        brokenRows.append(row)
        continue
    subRegion = row[7]

    for region_content in regions_levels:
        if lastRegionName in region_content:
            # Get subregion
            if subRegion in SUB_REGION_CORRECTION:
                subRegion = SUB_REGION_CORRECTION[subRegion]
            else:
                subRegion = re.split(r'(?=[A-Z])', subRegion)[1]
            #Append
            if not subRegion in region_content:
                region_content[subRegion] = [row]
            else:
                region_content[subRegion].append(row)



    # regions_levels_copy = regions_levels.copy()
    # for region_index,region_content in enumerate(regions_levels_copy): # Pour pas itérer sur ce qu'on modifie
    #     for k,v in region_content.items():
    #         if k == lastRegionName:
    #             # 7 = Region in the rows
    #             regionName = row[7]
    #             print(regionName)
    #             regions_levels[region_index][regionName] = row

# print(regions_levels[3]["Dog"])
#Pour chaque item, la condition c'est : Region + (subregion) + (Trash) + Special

# Potter rock
# Intro
# display_name_item_from_subregion(pottersrock["Intro"])

# FOR NOW REGIONS LOGIC IS IGNORED
#get_connection_logic()
update_level("../locations/Potters Rock.json",regions_levels[1])

