"""Build school-menu.md: Woodcrest breakfast + lunch, one week per view, items
tagged healthy (green) or junk (red).

Run from the repo root:  python _code/school_menu.py
Data: the Nutrislice weeks API behind midlandps.nutrislice.com. It sends no CORS
header, so the page can't fetch it live; this script bakes the weeks in and the
GitHub Action in .github/workflows/school-menu.yml reruns it daily.
"""
import json
import re
import time
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

API = "https://midlandps.api.nutrislice.com/menu/api/weeks/school/{school}/menu-type/{menu}/{d:%Y/%m/%d}/"
SCHOOL = "woodcrest"
MENUS = {"breakfast": "breakfast", "lunch": "lunch-2"}  # meal -> menu-type slug
WEEKS_BACK, WEEKS_AHEAD = 1, 8

# Matched against the lower-cased item name; JUNK wins over HEALTHY.
JUNK = [r"pizza", r"corn dog", r"nugget", r"chicken patty", r"popcorn chicken", r"breadstick", r"pull apart",
        r"cornbread", r"nachos", r"\bcrisp\b", r"frudel", r"cobbler", r"cinnamon cream cheese",
        r"(?<!english )muffin", r"tenders?\b", r"\bfries\b",
        r"smile potatoes", r"\btots?\b", r"tater", r"hash brown", r"chips", r"tostitos", r"doritos",
        r"cheetos", r"cookie", r"brownie", r"donut", r"doughnut", r"pop.?tart", r"cinnamon roll",
        r"cinnamon and sugar", r"pancake", r"waffle", r"french toast", r"syrup", r"sidekicks", r"slush",
        r"gelatin", r"jell-?o", r"whipped", r"chocolate", r"lucky charms", r"froot loops", r"cocoa",
        r"frosted", r"trix", r"goldfish", r"graham", r"cereal bar", r"bosco", r"crispy", r"breaded",
        r"\bjuice\b", r"cake", r"honey bun", r"uncrustable", r"hot dog", r"cheese crunch", r"cruncher"]
HEALTHY = [r"\bfresh\b", r"salad", r"broccoli", r"carrot", r"celery", r"cucumber", r"zucchini",
           r"bell pepper", r"tomato", r"radish", r"green beans", r"peas\b", r"spinach", r"cauliflower",
           r"lettuce", r"vegetable", r"\bbeans\b", r"apple", r"banana", r"orange", r"grape", r"kiwi",
           r"peach", r"pear", r"melon", r"berr", r"pineapple", r"mandarin", r"raisin", r"whole fruit",
           r"chilled fruit", r"mixed fruit", r"low fat milk", r"string cheese", r"egg salad", r"yogurt",
           r"parfait", r"hummus", r"grilled chicken", r"cottage cheese"]
# Never green even when the category is fruit/vegetable or a HEALTHY word appears.
PLAIN = [r"potato", r"bagel", r"\bsub\b", r"sandwich", r"scrambler", r"pocket", r"pretzel", r"cereal",
         r"smoothie", r"cheese sauce", r"biscuit", r"cheddar/mozzarella"]
# Entree-category items that are parts of the dish listed around them (taco bar, pasta + sauce).
COMPONENT = (r"diced tomato|shredded|lettuce|tortilla chips|taco meat|pasta$|penne|noodles|^cream cheese"
             r"|spread$|syrup$|sauce$|croutons|bun$")
TOPPING = r"diced|shredded|lettuce|chips|tortilla"


def get_json(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 school-menu page"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)


def classify(name, cat, nut):
    """'junk', 'healthy', or '' (plain). Added sugar >= 12 g is junk whatever the name."""
    n = name.lower()
    if any(re.search(p, n) for p in JUNK) or (nut.get("g_added_sugar") or 0) >= 12:
        return "junk"
    if any(re.search(p, n) for p in PLAIN):
        return ""
    if cat in ("fruit", "vegetable") or any(re.search(p, n) for p in HEALTHY):
        return "healthy"
    return ""


def item(f):
    nut = f.get("rounded_nutrition_info") or {}
    cat = f.get("food_category") or ""
    desc = re.sub(r"\s+", " ", f.get("description") or "").strip()
    size = f.get("serving_size_info") or {}
    icons = (f.get("icons") or {}).get("food_icons") or []
    return dict(n=re.sub(r"\s+", " ", f["name"]).strip(), k=classify(f["name"], cat, nut),
                img=f.get("image_url") or "", d=desc if desc.lower() != f["name"].strip().lower() else "",
                nu={k: v for k, v in nut.items() if v is not None},
                sv=" ".join(str(size.get(k) or "") for k in ("serving_size_amount", "serving_size_unit")).strip(),
                al=[i.get("synced_name") or (i.get("sprite") or {}).get("name") for i in icons if i.get("enabled", True)],
                ing=(f.get("ingredients") or "").strip())


def week_items(meal, monday):
    """date -> {'main': [...], 'sides': [...], 'note': str} for the days of that week.

    Nutrislice lists each main dish followed by the grain/vegetable that comes with it,
    then the shared fruit and vegetable choices, then drinks and condiments. So
    everything before the first fruit is the main block: each grain or vegetable there
    joins the dish before it as its 'with' list, and anything else opens a new dish. Drinks (always white or
    chocolate milk) and condiments are dropped.
    """
    data = get_json(API.format(school=SCHOOL, menu=MENUS[meal], d=monday))
    out = {}
    for day in data.get("days", []):
        main, sides, notes, in_main = [], [], [], True
        for m in day.get("menu_items", []):
            f = m.get("food")
            if not f:
                if m.get("text") and not m.get("is_section_title"):
                    notes.append(m["text"].strip())
                continue
            cat = f.get("food_category") or ""
            if cat in ("beverage", "condiment"):
                continue
            if cat == "fruit":
                in_main = False
            it = item(f)
            if not in_main:
                sides.append(it)
            elif not main or (cat not in ("grain", "vegetable") and not re.search(COMPONENT, it["n"].lower())):
                main.append(dict(it, w=[]))
            elif re.search(TOPPING, main[-1]["n"].lower()) and re.search(r"meat|sauce", it["n"].lower()):
                # Taco day lists the tomatoes first; the meat names the dish.
                head = main[-1]
                main[-1] = dict(it, w=[{k: v for k, v in head.items() if k != "w"}] + head["w"])
            else:
                main[-1]["w"].append(it)
        if main or sides or notes:
            out[day["date"]] = dict(main=main, sides=sides, note=" · ".join(notes))
    return out


def main():
    root = Path(__file__).resolve().parent.parent
    today = date.today()
    start = today - timedelta(days=today.weekday()) - timedelta(weeks=WEEKS_BACK)
    weeks, empty_run = [], 0
    for w in range(WEEKS_BACK + WEEKS_AHEAD + 1):
        monday = start + timedelta(weeks=w)
        meals = {meal: week_items(meal, monday) for meal in MENUS}
        days = []
        for i in range(5):
            d = (monday + timedelta(days=i)).isoformat()
            days.append(dict(date=d, **{meal: meals[meal].get(d) for meal in MENUS}))
        has_any = any(day[m] for day in days for m in MENUS)
        print(f"{monday}  " + "  ".join(f"{m}:{sum(bool(day[m]) for day in days)}d" for m in MENUS))
        if has_any:
            weeks.append(dict(monday=monday.isoformat(), days=days))
            empty_run = 0
        elif monday > today:
            empty_run += 1
            if empty_run == 2:
                break
        time.sleep(0.3)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    page = (Path(__file__).with_name("school_menu_template.html").read_text(encoding="utf-8")
            .replace("__DATA__", json.dumps(weeks, separators=(",", ":")))
            .replace("__STAMP__", stamp))
    (root / "school-menu.md").write_text(
        # Hidden page: not in the nav or sitemap, reachable only at /meals/.
        '---\nlayout: page\ntitle: "School Menu"\npermalink: /meals/\nsitemap: false\n---\n\n{% raw %}\n' + page + "\n{% endraw %}\n",
        encoding="utf-8")


if __name__ == "__main__":
    main()
