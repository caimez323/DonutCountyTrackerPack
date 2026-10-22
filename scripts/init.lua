local variant = Tracker.ActiveVariantUID

-- Items
require("scripts.items_import")

-- Logic
require("scripts.logic.logic_helper")
require("scripts.logic.base_logic")
require("scripts.logic.graph_logic.logic_main")

-- Maps
Tracker:AddMaps("maps/maps.json")

-- Layout
require("scripts.layouts_import")

-- Locations
require("scripts.locations_import")

-- AutoTracking for PopTracker
if PopVersion and PopVersion >= "0.26.0" then
    require("scripts.autotracking")
else
    -- Charger le layout tabs par défaut
    Tracker:AddLayouts("layouts/tabs_default.json")
end

function OnFrameHandler()
    ScriptHost:RemoveOnFrameHandler("load handler")
    -- stuff
    ScriptHost:AddWatchForCode("StateChanged", "*", StateChanged)
    ScriptHost:AddOnLocationSectionChangedHandler("location_section_change_handler", LocationHandler)
    CreateLuaManualStorageItem("manual_location_storage")
    ForceUpdate()
end
require("scripts.luaitems")
require("scripts.watches")
ScriptHost:AddOnFrameHandler("load handler", OnFrameHandler)


-- TODO 
-- Ajouter salt 1/2 pepper 1/2/3
-- Mettre le buy catapult pareil
-- Implémenter le "glitch" en hors logique



-- Current bugs
-- Salt & Pepper logic is bugged
-- Achivements does not display on the overworld
-- Salt & Pepper don't increment on the tracker