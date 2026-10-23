
## FIRST WE PARSE THE LOGIC FILE
import re

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

with open("Rows.txt", "a") as f:
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
                region_content[subRegion] = row
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

print(regions_levels[0]["scn_mom_house_merged"])