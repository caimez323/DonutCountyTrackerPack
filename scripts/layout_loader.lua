DEFAULT_LAYOUT_OPTS = {
    holeeffects = 2,
    catapults = 2,
    achievement = true,
    trash_category = true,
    trashopedia = true,
}

local function b(v) return v and 1 or 0 end


LAYOUTS_LOADED = false
function LoadLayouts(opts)
    if LAYOUTS_LOADED then
        print("LoadLayouts: PLEASE RELOAD PACK/RELAUNCH POP TRACKER")
        return
    end
    
    LAYOUTS_LOADED = true
    opts = opts or DEFAULT_LAYOUT_OPTS
    Tracker:AddLayouts(string.format("layouts/items/holeeffects_%d.json", opts.holeeffects))
    Tracker:AddLayouts(string.format("layouts/items/catapults_%d.json", opts.catapults))
    Tracker:AddLayouts(string.format("layouts/tabs/tabs_a%d_t%d_s%d.json",
        b(opts.achievement), b(opts.trash_category), b(opts.trashopedia)))
end
