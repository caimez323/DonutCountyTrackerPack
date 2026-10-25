# Donut County Poptracker Pack

## Features

Track Donut County (crazy right ?)

This pack auto adjust to your configuration if you connect to the autotracking via archipelago servers.
It will add/remove tabs and simplify the layout if it detects things not relevant via the configuration.
**This does mean that** if the screen is pitch black, it may be an issue with your archipelago connection. (Although it should be default case implemented)

See **Issues** below if you have any trouble, or check the archipelago Donut County channel if you find any logic issues.

# Usage
Download the latest release of the pack : [Pack release](https://github.com/caimez323/DonutCountyTrackerPack/releases).

If you don't have Poptracker yet : [Poptracker](https://github.com/black-sliver/PopTracker/releases/).

You can also find the Donut County .apworld [here](https://github.com/1e1001/DonutCountyAP/releases/).

# Issues & Todo

## Todo

- Add auto tabbing
- Add "glitch" OoL
- Make the same detection as settings for splitting catapults/holeeffects
- Add definitive .png for items/levels/settings
- Compress .png and reduce overall repo size
- Remove Achievement tab if not needed
- Add texting glitch logic e.g. miras house
- On a un cas on/off avec le trashsouls Et un cas on/off avec le trash sanity, il faudrait mélanger les deux, donc faire 2 paires de json, c'est bof, y a peut être un autre moyen

## Know Issues

As of last release :
- Salt & Pepper don't increment correctly on the tracker
- Quadcopter pieces don't increment (nor unlock the boss fight location) in the tracker
- I have some doubt with bio lab frog logic
- Ending a zone ignores the trashsouls logic
- Trash Category doesn't check/(Logic is more complicated and maybe need to rewrite the trashsouls/trashsanity logic due to "hole size" or item that might not be reachable)




