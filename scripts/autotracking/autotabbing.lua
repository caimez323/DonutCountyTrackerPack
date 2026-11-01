TABBING_KEY = nil
DONUT_LATEST_MODE = nil
DONUT_LATEST_LEVEL = nil

LEVEL_CODE = {
    [0]  = "Miras House",
    [1]  = "Potters Rock",
    [2]  = "Ranger Station",
    [3]  = "Riverbed",
    [4]  = "Campground",
    [5]  = "Hopper Springs",
    [6]  = "Joshua Tree",
    [7]  = "Beach Lot C",
    [8]  = "Gecko Park",
    [9]  = "Chicken Barn",
    [10] = "Honey Nut Forest",
    [11] = "Cat Soup",
    [12] = "Donut Shop",
    [13] = "Abandoned House",
    [14] = "Raccoon Lagoon",
    [15] = "The 405",
    [16] = "Raccoon HQ",
    [17] = "Biology Lab",
    [18] = "Anthropology Lab",
    [19] = "Trash Kings Office",
    [20] = "Boss Fight",
}

function RegisterDonutZoneKeys(notify_keys)
    local player = Archipelago.PlayerNumber or -1
    if player < 0 then return end
    TABBING_KEY = "Slot:" .. player .. ":level"
    table.insert(notify_keys, TABBING_KEY)
    -- Following this
end

function ParseDonutLevel(value)
    if type(value) ~= "string" then return nil, nil end
    local mode, idx = value:match("^(%a+):(%-?%d+)$")
    if not mode then return nil, nil end
    return mode, tonumber(idx)
end

function applyDonutTab(mode, idx)
    
    if mode == "select" or mode == "title" then
        Tracker:UiHint("ActivateTab", "Overworld")
        return
    end

    if mode == "game" then
        local title = LEVEL_CODE[idx]
        if not title then
            -- print("[Donut] niveau inconnu : " .. tostring(idx))
            return
        end
        Tracker:UiHint("ActivateTab", "Map details")
        Tracker:UiHint("ActivateTab", title)
    end
end

-- On key changing
function onChangeZone(key, value, old_value)
    -- Not our key
    if key ~= TABBING_KEY then return end

    local mode, idx = ParseDonutLevel(value)
    if not mode then
        -- print("[Donut] valeur inattendue : " .. tostring(value))
        return
    end
    -- Not changed
    if mode == DONUT_LATEST_MODE and idx == DONUT_LATEST_LEVEL then return end
    DONUT_LATEST_MODE = mode
    DONUT_LATEST_LEVEL = idx
    -- for debug
    -- print(string.format("[Donut] mode=%s level=%d", mode, idx))

    applyDonutTab(mode, idx)
end

Archipelago:AddSetReplyHandler("donut zone handler", onChangeZone)
Archipelago:AddRetrievedHandler("donut zone launch handler", onChangeZone)