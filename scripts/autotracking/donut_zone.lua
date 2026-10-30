DONUT_ZONE_KEY = nil
DONUT_LATEST_ZONE = nil

DONUT_CANDIDATES = {}

function RegisterDonutZoneKeys(notify_keys)
    local player = Archipelago.PlayerNumber or -1
    if player < 0 then return end
    local team = Archipelago.TeamNumber or 0

    local bases = { "current_level", "level", "CurrentLevel", "Level" }  -- à adapter
    for _, b in ipairs(bases) do
        local variants = {
            b,
            b .. "_" .. player,
            b .. "_" .. team .. "_" .. player,
            "DonutCounty_" .. b .. "_" .. player,
            "Donut County_" .. b .. "_" .. player,
        }
        for _, k in ipairs(variants) do
            DONUT_CANDIDATES[k] = true
            table.insert(notify_keys, k)
        end
    end
end

function onDonutZone(key, value, old_value)
    if not DONUT_CANDIDATES[key] then return end
    if value ~= nil then
        print("[Donut] TROUVÉ key=" .. key .. " value=" .. tostring(value))
    end
end

Archipelago:AddSetReplyHandler("donut zone handler", onDonutZone)
Archipelago:AddRetrievedHandler("donut zone launch handler", onDonutZone)