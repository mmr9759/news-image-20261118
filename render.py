#!/usr/bin/env python3
"""Render 'THE WORLD TODAY' front page for Wednesday 18 November 2026.
Programmatic PIL render: every glyph drawn from real text, fully deterministic.
Output: entry.png (1024x1024, <= 1 MiB).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (16, 32, 64)
RED = (178, 24, 24)
GREY = (110, 110, 105)
MAP_BG = (214, 226, 233)
LAND = (74, 96, 110)
RULE = (150, 140, 120)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---- 33 stories: 1 lead + 10 Americas + 11 Europe/Middle East + 11 Asia/Africa/Oceania
LEAD_HEAD = "Trump lands in Manila for Quad talks; Ukraine hits Crimea bridge again"
LEAD_SUM = ("The US president opens an Asia tour in the Philippines as Quad leaders meet, "
            "while Kyiv strikes the bridge to Crimea for a second day and Russia hits crossings in the capital.")

AMERICAS = [
    ("Nvidia doubles revenue to $115.8bn", "Board says it will not reinstate ousted chief Jensen Huang."),
    ("US loses measles elimination status", "Worst outbreak since 1991 ends three decades of elimination."),
    ("Trump deposition deadline extended", "Judge gives more time in the $10bn BBC defamation lawsuit."),
    ("Asif Merchant jailed for 27.5 years", "Sentenced over a plot against US officials."),
    ("US presses UN over Taiwan flights", "Washington challenges flight rules; Beijing hits back."),
    ("Pope Leo XIV in Peru for Amazon", "Pontiff calls for justice for rainforest defenders."),
    ("Costa Rican journalist shot dead", "Killed after reporting on drug trafficking and graft."),
    ("Drones arm Latin America's gangs", "Organised crime's new weapon, governments struggle to respond."),
    ("Caribbean fears citizenship crackdown", "EU threats may end visa-free passport-for-cash schemes."),
    ("Canada and China extend trade deals", "Xi meets Carney ahead of the APEC summit in Shenzhen."),
]

EUROPE_ME = [
    ("Ukraine hits Crimea bridge again", "Second day of strikes as Russia pounds bridges in Kyiv."),
    ("Britain sanctions settlement firms", "Eight companies hit over illegal West Bank settlements."),
    ("Latvia approves Kulbergs cabinet", "Saeima backs the new government in a confidence vote."),
    ("Nations League last eight decided", "Germany, Portugal and Norway complete the quarter-final line-up."),
    ("Haaland's 96th-minute penalty", "Norway fight back from 2-0 down to beat Denmark 3-2."),
    ("Northern Ireland reach top tier", "Devenny strike in Budapest seals promotion at last."),
    ("Ireland beat Kosovo 3-0", "Second place and a promotion play-off secured."),
    ("Deutsche Bank ignored warnings", "Leaked files show risky clients kept despite compliance alarms."),
    ("Iran drones hit US radar in Bahrain", "Gulf states report interceptions; Bahrain gives the all-clear."),
    ("Gaza: one hot meal every two days", "WFP warns of hunger as Board of Peace fears ceasefire collapse."),
    ("Jordan bans Telegram", "Messaging app blocked over national security concerns."),
]

ASIA_AFRICA_OCEANIA = [
    ("Cyclone Akvan grows over Bay of Bengal", "India's east coast on high alert as the storm intensifies."),
    ("Modi offers free e-visas at ASEAN", "India pushes maritime ties at the summit in Manila."),
    ("India re-elected to ITU Council", "New Delhi wins a seat for the 2027-2030 term."),
    ("Thailand fire kills 11 in Phuket", "Blaze in the Patong resort area leaves dozens hurt."),
    ("Dhoni retires from the IPL", "Chennai great becomes Super Kings mentor."),
    ("Grammys 2027: Raye leads the field", "Nominations are out; Harry Styles is snubbed."),
    ("Sudan: 2,230 civilians killed in 2026", "UN says drones killed 1,630 of them in ten months."),
    ("South Africa: 17 die in two shootings", "Police report two separate mass shootings."),
    ("Guinea mining crackdown displaces thousands", "Ban on illegal mining stirs tensions with neighbours."),
    ("Congo: 11,000 Bundibugyo cases", "WHO reports 5,400 deaths in the outbreak."),
    ("New Zealand pays Penrhyn port bill", "Wellington accepts liability for cost overruns."),
]

# Map flash points: (lon, lat, label or None)
DOTS = [
    (121.0, 14.6, "MANILA"), (-122.4, 37.8, None), (10.7, 59.9, None),
    (30.5, 50.4, "KYIV"), (33.5, 44.6, None), (50.6, 26.2, "BAHRAIN"),
    (34.5, 31.5, "GAZA"), (-0.1, 51.5, None), (13.4, 52.5, None),
    (77.2, 28.6, "NEW DELHI"), (90.0, 15.0, None),
    (98.4, 7.9, None), (32.6, 15.6, None),
    (28.0, -26.2, "JOHANNESBURG"), (-77.0, -12.0, "LIMA"),
    (133.8, -23.8, None), (174.8, -41.3, "WELLINGTON"),
]

# ---- Simplified continent outlines (lon, lat), equirectangular ----
NORTH_AMERICA = [(-168,66),(-155,58),(-140,60),(-125,49),(-124,40),(-117,32),(-110,24),
    (-105,20),(-97,16),(-90,14),(-83,9),(-79,9),(-83,15),(-87,21),(-90,21),(-97,26),
    (-93,30),(-84,30),(-81,26),(-80,32),(-76,35),(-74,40),(-70,42),(-68,45),(-65,44),
    (-60,46),(-55,52),(-60,55),(-65,60),(-68,58),(-78,62),(-85,66),(-92,66),(-95,69),
    (-110,68),(-125,70),(-140,70),(-155,71),(-165,66)]
GREENLAND = [(-58,64),(-52,60),(-43,60),(-32,68),(-22,70),(-25,74),(-40,76),(-58,76),
    (-60,74),(-58,70)]
SOUTH_AMERICA = [(-80,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),
    (-70,-30),(-72,-37),(-73,-44),(-74,-50),(-70,-54),(-66,-55),(-68,-50),(-65,-45),
    (-62,-41),(-58,-38),(-52,-33),(-48,-28),(-41,-23),(-38,-15),(-35,-8),(-38,-5),
    (-44,-3),(-50,0),(-53,4),(-58,6),(-62,9),(-68,11),(-72,12),(-76,10)]
AFRICA = [(-17,15),(-16,21),(-10,30),(-6,33),(0,36),(10,37),(11,34),(20,32),(30,31),
    (33,27),(37,22),(39,18),(43,12),(48,11),(51,11),(46,5),(41,-2),(40,-10),(36,-18),
    (33,-26),(28,-33),(20,-35),(17,-32),(15,-27),(12,-18),(13,-12),(9,-1),(9,4),
    (4,6),(-8,5),(-13,8),(-17,12)]
EUROPE = [(-10,36),(-9,38),(-9,43),(-2,44),(-1,46),(-4,48),(-2,50),(1,51),(3,53),
    (5,53),(8,55),(8,57),(10,59),(6,58),(5,60),(10,62),(12,60),(18,56),(21,55),
    (24,58),(24,60),(28,61),(30,64),(30,68),(33,68),(40,67),(45,68),(52,68),(58,69),
    (60,66),(55,60),(50,55),(48,50),(45,46),(40,44),(38,47),(35,45),(30,46),(28,44),
    (27,42),(24,40),(23,37),(26,38),(30,36),(28,37),(23,36),(20,40),(19,42),(15,44),
    (12,44),(10,44),(8,44),(3,43),(0,40),(-2,37),(-6,36)]
ASIA = [(30,36),(33,36),(36,36),(40,38),(43,40),(48,42),(50,44),(52,46),(48,50),
    (50,55),(55,60),(60,66),(68,68),(75,72),(80,73),(90,75),(100,77),(110,76),
    (120,74),(130,72),(140,72),(150,70),(160,70),(170,67),(178,65),(178,62),
    (170,60),(163,60),(159,55),(156,51),(150,50),(142,50),(141,45),(140,40),
    (135,37),(130,35),(127,35),(126,33),(122,31),(120,28),(118,25),(114,22),
    (110,20),(108,18),(108,12),(105,9),(103,8),(100,7),(98,10),(97,15),(94,17),
    (92,21),(89,22),(86,20),(82,17),(80,13),(78,8),(76,10),(73,16),(70,20),
    (66,25),(62,25),(58,26),(56,27),(53,27),(50,29),(48,30),(44,29),(42,28),
    (39,28),(36,31),(34,33),(31,35)]
AUSTRALIA = [(113,-22),(114,-28),(115,-33),(118,-35),(124,-33),(129,-32),(132,-32),
    (135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),
    (150,-22),(146,-19),(142,-11),(137,-12),(135,-15),(132,-12),(130,-13),
    (126,-14),(122,-17),(118,-20)]
SE_ASIA_ISLANDS = [[(95,5),(97,5),(100,0),(102,-2),(104,-3),(106,-6),(110,-7),(114,-8),
    (117,-9),(120,-10),(122,-8),(124,-5),(126,-2),(128,0),(130,-2),(132,-4),(131,-1),
    (128,1),(126,2),(124,1),(122,1),(120,0),(118,2),(116,4),(113,3),(110,1),
    (107,0),(104,1),(101,1),(99,3)],[(122,11),(122,14),(121,17),(121,19),(122,18),
    (124,16),(126,12),(125,9),(123,8),(122,9)]]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE, ASIA,
              AUSTRALIA] + SE_ASIA_ISLANDS

def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG)
    def px(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * w,
                y0 + (75.0 - lat) / 130.0 * h)
    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND)
    for lon, lat, label in DOTS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
        if label:
            f = font(SANS_B, 10)
            tw = d.textlength(label, font=f)
            # Wellington sits at the map's right edge: label to the left
            lx = cx - tw - 8 if label == "WELLINGTON" else cx + 6
            d.text((lx, cy - 6), label, font=f, fill=(30, 30, 30))

def draw_section(d, x, y, w, title, stories):
    f_title = font(SANS_B, 15)
    f_head = font(SANS_B, 13)
    f_sum = font(SANS, 11)
    d.rectangle([x, y, x + w, y + 26], fill=NAVY)
    d.text((x + 8, y + 5), title, font=f_title, fill=(255, 255, 255))
    yy = y + 34
    for head, summ in stories:
        hl = wrap(d, head, f_head, w - 4)[:2]
        for line in hl:
            d.text((x + 2, yy), line, font=f_head, fill=INK)
            yy += 16
        sl = wrap(d, summ, f_sum, w - 4)[:2]
        for line in sl:
            d.text((x + 2, yy), line, font=f_sum, fill=(60, 60, 60))
            yy += 13
        yy += 10
        d.line([(x, yy - 5), (x + w, yy - 5)], fill=(210, 204, 190), width=1)
    return yy

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    f_name = font(SERIF_B, 62)
    name = "THE WORLD TODAY"
    nw = d.textlength(name, font=f_name)
    d.text(((W - nw) / 2, 14), name, font=f_name, fill=INK)
    f_date = font(SANS_B, 15)
    date = "WEDNESDAY 18 NOVEMBER 2026  ·  33 STORIES  ·  6 CONTINENTS"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 84), date, font=f_date, fill=RED)
    d.line([(MARGIN, 110), (W - MARGIN, 110)], fill=INK, width=3)
    d.line([(MARGIN, 114), (W - MARGIN, 114)], fill=INK, width=1)
    # Lead story
    y = 126
    f_kick = font(SANS_B, 13)
    d.text((MARGIN, y), "LEAD  —  MANILA  ·  KYIV  ·  CRIMEA", font=f_kick, fill=RED)
    y += 22
    f_lead = font(SERIF_B, 26)
    for line in wrap(d, LEAD_HEAD, f_lead, W - 2 * MARGIN)[:2]:
        d.text((MARGIN, y), line, font=f_lead, fill=INK)
        y += 31
    f_lsum = font(SANS, 14)
    for line in wrap(d, LEAD_SUM, f_lsum, W - 2 * MARGIN)[:2]:
        d.text((MARGIN, y), line, font=f_lsum, fill=(50, 50, 50))
        y += 18
    y += 6
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    # Map
    y += 8
    map_h = 166
    draw_map(d, MARGIN, y, W - 2 * MARGIN, map_h)
    f_cap = font(SANS_B, 11)
    cap = "THE DAY ON THE MAP — 16 FLASH POINTS, FROM MANILA TO LIMA"
    d.text((MARGIN + 6, y + map_h - 18), cap, font=f_cap, fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(40, 50, 60))
    y += map_h + 14
    # Columns
    col_w = (W - 2 * MARGIN - 2 * 16) // 3
    xs = [MARGIN, MARGIN + col_w + 16, MARGIN + 2 * (col_w + 16)]
    ends = []
    ends.append(draw_section(d, xs[0], y, col_w, "THE AMERICAS", AMERICAS))
    ends.append(draw_section(d, xs[1], y, col_w, "EUROPE & THE MIDDLE EAST", EUROPE_ME))
    ends.append(draw_section(d, xs[2], y, col_w, "ASIA, AFRICA & OCEANIA", ASIA_AFRICA_OCEANIA))
    # Footer
    fy = max(ends) + 6
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=INK, width=2)
    f_foot = font(SANS, 11)
    foot = "All 33 stories happened or were first reported on Wednesday 18 November 2026."
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, fy + 6), foot, font=f_foot, fill=GREY)
    print("columns end at", ends, "footer at", fy)
    img.save("entry.png", optimize=True)
    print("saved entry.png")

if __name__ == "__main__":
    main()
