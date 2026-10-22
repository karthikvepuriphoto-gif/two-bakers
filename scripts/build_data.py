#!/usr/bin/env python3
"""Build pantry and recipe JSON from published recipes and USDA SR Legacy amounts.

Gram weights come from USDA FoodData Central household portions (SR Legacy, April 2018)
unless the recipe author printed a gram weight. Those author weights win.
Nutrient values are per 100 g from the same release. This script does not invent them.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "data"

# USDA household portions (SR Legacy food_portion.csv), grams.
CUP_OATS = 81.0  # FDC 173904, 1 cup
TBSP_OATS = CUP_OATS / 16.0
CUP_PB = 258.0  # FDC 174266 / 172470, 1 cup
TBSP_PB = 16.0  # 2 tbsp = 32 g
CUP_MASHED_BANANA = 225.0  # FDC 173944
MEDIUM_BANANA = 118.0
SMALL_BANANA = 101.0
LARGE_BANANA = 136.0
LARGE_EGG = 50.0
EGG_WHITE = 33.0
CUP_AP = 125.0  # FDC 168894
CUP_WW = 120.0  # FDC 168893
# Greek yogurt has no cup portion in SR Legacy. Ambitious Kitchen prints 1/2 cup (113 g).
CUP_GREEK = 226.0
CUP_COTTAGE_4 = 225.0  # FDC 172179, 1 cup small curd, not packed
CUP_COTTAGE_2 = 226.0  # FDC 172182
CUP_BROWN = 220.0  # FDC 168833, packed
TBSP_HONEY = 21.0
CUP_HONEY = 339.0
TBSP_MAPLE = 20.0
CUP_MAPLE = 315.0
TSP_VANILLA = 4.2
TSP_CINN = 2.6
TSP_BP = 4.6
TSP_BS = 4.6
TSP_SALT = 6.0
CUP_CHIPS = 168.0  # FDC 167976, 1 cup chips
CUP_MINI = 173.0
TBSP_COCOA = 5.4
CUP_COCOA = 86.0
CUP_ALMOND_FLOUR = 95.0  # FDC 170567, 1 cup ground almonds
CUP_PROTEIN = 96.0  # FDC 173180, 0.33 cup = 32 g, treated as 1/3 cup
CUP_ALMOND_BUTTER = 250.0
TBSP_COCONUT_OIL = 13.6
TBSP_OLIVE = 13.5
CUP_YOGURT = 245.0  # FDC 170888, 1 cup
CUP_BERRIES = 148.0
CUP_STRAW_SLICED = 166.0
CUP_GRANOLA = 122.0
CUP_COCONUT = 93.0  # FDC 168586 shredded cup; nutrients stay on unsweetened FDC 170170
CUP_WALNUT = 117.0  # chopped
CUP_RAISIN = 145.0  # not packed
CUP_MOZZ = 112.0  # FDC 170845 shredded
BACON_SLICE = 8.1  # FDC 167914, 1 slice cooked
TSP_GARLIC = 3.1
TSP_ONION = 2.4
TSP_OREGANO = 1.0
CUP_MILK_SKIM = 245.0
CUP_MILK_2 = 244.0
CUP_ALMOND_MILK = 262.0
TBSP_GROUND_ALMOND = CUP_ALMOND_FLOUR / 16.0

DATASET = "USDA FoodData Central, SR Legacy, April 2018"


def food(fid, pantry, name, fdc, fdc_name, kcal, protein, fiber, sugar, allergens=None, gluten_risk=False, note=""):
    return {
        "id": fid,
        "pantryId": pantry,
        "name": name,
        "fdcId": fdc,
        "fdcName": fdc_name,
        "dataset": DATASET,
        "fdcUrl": f"https://fdc.nal.usda.gov/food-details/{fdc}/nutrients" if fdc else None,
        "per100g": {"kcal": kcal, "protein": protein, "fiber": fiber, "sugar": sugar},
        "allergens": allergens or [],
        "glutenRisk": gluten_risk,
        "note": note,
    }


FOODS = [
    food("pb-salted", "peanut-butter", "Peanut butter", 174266, "Peanut butter, smooth style, with salt", 598, 22.21, 5, 10.49, ["peanut"]),
    food("pb-unsalted", "peanut-butter", "Natural peanut butter", 172470, "Peanut butter, smooth style, without salt", 598, 22.21, 5, 10.49, ["peanut"]),
    food("pb-flour", "powdered-peanut", "Powdered peanut butter", 174267, "Peanut flour, defatted", 327, 52.2, 15.8, 8.22, ["peanut"], note="Powdered peanut butter is counted as defatted peanut flour. Sugar is USDA nutrient 2000 (total sugars), because 1063 was not published for this food."),
    food("sunflower-butter", "sunflower-butter", "Sunflower seed butter", 170155, "Seeds, sunflower seed butter, without salt", 617, 17.28, 5.7, 10.54),
    food("almond-butter", "almond-butter", "Almond butter", 168588, "Nuts, almond butter, plain, without salt added", 614, 20.96, 10.3, 4.43),
    food("banana", "banana", "Banana", 173944, "Bananas, raw", 89, 1.09, 2.6, 12.23),
    food("oats", "oats", "Rolled oats", 173904, "Cereals, oats, regular and quick, not fortified, dry", 379, 13.15, 10.1, 0.99, gluten_risk=True, note="Oats are flagged as a gluten risk because they are often packed near wheat. Certified gluten-free oats are a grown-up decision."),
    food("egg", "egg", "Egg", 171287, "Egg, whole, raw, fresh", 143, 12.56, 0, 0.37, ["egg"]),
    food("egg-white", "egg", "Egg white", 172183, "Egg, white, raw, fresh", 52, 10.9, 0, 0.71, ["egg"]),
    food("greek-nonfat", "greek-yogurt", "Nonfat Greek yogurt", 170894, "Yogurt, Greek, plain, nonfat", 59, 10.19, 0, 3.24, ["dairy"]),
    food("greek-lowfat", "greek-yogurt", "Low-fat Greek yogurt", 170903, "Yogurt, Greek, plain, lowfat", 73, 9.95, 0, 3.56, ["dairy"], note="Used when a recipe says plain Greek yogurt and allows 2%."),
    food("greek-whole", "greek-yogurt", "Whole-milk Greek yogurt", 171304, "Yogurt, Greek, plain, whole milk", 97, 9, 0, 4, ["dairy"]),
    food("greek-vanilla-low", "greek-yogurt", "Low-fat vanilla Greek yogurt", 170907, "Yogurt, Greek, vanilla, lowfat", 95, 8.64, 0, 9.54, ["dairy"]),
    food("yogurt-vanilla", "yogurt", "Low-fat vanilla yogurt", 170888, "Yogurt, vanilla, low fat", 85, 4.93, 0, 13.8, ["dairy"], note="SR Legacy has no whole-milk vanilla yogurt. This low-fat record is the closest published vanilla yogurt."),
    food("cottage-4", "cottage-cheese", "Cottage cheese (4%)", 172179, "Cheese, cottage, creamed, large or small curd", 98, 11.12, 0, 2.67, ["dairy"], note="Cup weight is the small-curd, not-packed cup (225 g), the usual grocery tub."),
    food("cottage-2", "cottage-cheese", "Low-fat cottage cheese (2%)", 172182, "Cheese, cottage, lowfat, 2% milkfat", 81, 10.45, 0, 4, ["dairy"], note="Used when the author says low-fat. A 1% record also exists (FDC 173417)."),
    food("cocoa", "cocoa", "Cocoa powder", 169593, "Cocoa, dry powder, unsweetened", 228, 19.6, 37, 1.75),
    food("honey", "honey", "Honey", 169640, "Honey", 304, 0.3, 0.2, 82.12),
    food("maple", "maple", "Maple syrup", 169661, "Syrups, maple", 260, 0.04, 0, 60.46),
    food("chips", "chocolate", "Semisweet chocolate chips", 167976, "Candies, semisweet chocolate", 480, 4.2, 5.9, 54.5, ["dairy"], note="Flagged as dairy because baking chips are usually made with milk."),
    food("dark-70", "chocolate", "Dark chocolate", 170273, "Chocolate, dark, 70-85% cacao solids", 598, 7.79, 10.9, 23.99, ["dairy"], note="Flagged as dairy so a milk-containing bar is not shown as safe. Some 70% bars are dairy-free; a grown-up should read the package."),
    food("baking-powder", "baking-powder", "Baking powder", 172803, "Leavening agents, baking powder, double-acting, sodium aluminum sulfate", 53, 0, 0.2, 0),
    food("baking-soda", "baking-soda", "Baking soda", 175040, "Leavening agents, baking soda", 0, 0, 0, 0),
    food("vanilla", "vanilla", "Vanilla extract", 173471, "Vanilla extract", 288, 0.06, 0, 12.65),
    food("cinnamon", "cinnamon", "Cinnamon", 171320, "Spices, cinnamon, ground", 247, 3.99, 53.1, 2.17),
    food("salt", "salt", "Salt", 173468, "Salt, table", 0, 0, 0, 0),
    food("whey", "protein-powder", "Whey protein powder", 173180, "Beverages, Protein powder whey based", 352, 78.13, 3.1, 0, ["dairy"], note="Flavored powders are often lower in protein than this unflavored whey-based record. The recipe still gets this USDA row, and the screen says so."),
    food("whey-isolate", "protein-powder", "Whey protein isolate", 173177, "Beverages, Whey protein powder isolate", 359, 58.14, 0, 1.16, ["dairy"]),
    food("soy-protein", "protein-powder", "Soy protein powder", 173181, "Beverages, Protein powder soy based", 388, 55.56, 6.7, 22.22, note="Stand-in for an unspecified plant protein powder. The cup weight is borrowed from whey protein powder, which is the protein powder with a published cup fraction (1/3 cup = 32 g)."),
    food("flour", "flour", "All-purpose flour", 168894, "Wheat flour, white, all-purpose, enriched, bleached", 364, 10.33, 2.7, 0.27, ["gluten"]),
    food("whole-wheat", "whole-wheat", "Whole-wheat flour", 168893, "Wheat flour, whole-grain", 340, 13.21, 10.7, 0.41, ["gluten"]),
    food("soft-wheat", "whole-wheat", "Soft whole-wheat flour", 168944, "Wheat flour, whole-grain, soft wheat", 332, 9.61, 13.1, 1.02, ["gluten"], note="Stand-in for whole-wheat pastry flour, which is not its own SR Legacy food. The author's gram weight is used."),
    food("almond-flour", "almond-flour", "Almond flour", 170568, "Nuts, almonds, blanched", 590, 21.4, 9.9, 4.63, note="Almond flour is not a separate SR Legacy food. Nutrients are blanched almonds (FDC 170568). One cup uses the ground-almond portion on FDC 170567 (95 g)."),
    food("brown-sugar", "brown-sugar", "Brown sugar", 168833, "Sugars, brown", 380, 0.12, 0, 97.02),
    food("walnuts", "walnuts", "Walnuts", 170187, "Nuts, walnuts, english", 654, 15.23, 6.7, 2.61),
    food("raisins", "raisins", "Raisins", 168165, "Raisins, dark, seedless", 299, 3.3, 4.5, 65.18),
    food("coconut", "coconut", "Unsweetened coconut", 170170, "Nuts, coconut meat, dried (desiccated), not sweetened", 660, 6.88, 16.3, 7.35, note="Unsweetened coconut only publishes a 1 oz weight. Cup measures use the shredded-cup weight from sweetened shredded coconut (FDC 168586, 93 g) with these unsweetened nutrients."),
    food("strawberries", "strawberries", "Strawberries", 167762, "Strawberries, raw", 32, 0.67, 2, 4.89),
    food("blueberries", "blueberries", "Blueberries", 171711, "Blueberries, raw", 57, 0.74, 2.4, 9.96),
    food("milk-2", "milk", "Milk (2%)", 171267, "Milk, reduced fat, fluid, 2% milkfat, with added vitamin A and vitamin D", 50, 3.3, 0, 5.06, ["dairy"]),
    food("milk-skim", "milk", "Skim milk", 171269, "Milk, nonfat, fluid, with added vitamin A and vitamin D", 34, 3.37, 0, 5.09, ["dairy"]),
    food("almond-milk", "almond-milk", "Unsweetened almond milk", 174832, "Beverages, almond milk, unsweetened, shelf stable", 15, 0.4, 0.2, 0.81),
    food("mozzarella", "mozzarella", "Mozzarella", 170845, "Cheese, mozzarella, whole milk", 299, 22.17, 0, 0, ["dairy"], note="Shredded cup weight (112 g) is published on this whole-milk record."),
    food("bacon", "bacon", "Cooked bacon", 167914, "Pork, cured, bacon, cooked, baked", 548, 35.73, 0, 0, note="One strip uses USDA '1 slice cooked' (8.1 g), which can be thinner than a grocery strip."),
    food("butter", "butter", "Butter", 173430, "Butter, without salt", 717, 0.85, 0, 0.06, ["dairy"]),
    food("coconut-oil", "coconut-oil", "Coconut oil", 171412, "Oil, coconut", 892, 0, 0, 0),
    food("olive-oil", "olive-oil", "Olive oil", 171413, "Oil, olive, salad or cooking", 884, 0, 0, 0),
    food("onion-powder", "onion-powder", "Onion powder", 171327, "Spices, onion powder", 341, 10.41, 15.2, 6.63),
    food("garlic-powder", "garlic-powder", "Garlic powder", 171325, "Spices, garlic powder", 331, 16.55, 9, 2.43),
    food("oregano", "oregano", "Dried oregano", 171328, "Spices, oregano, dried", 265, 9, 42.5, 4.09),
    food("granola", "granola", "Homemade granola", 171646, "Cereals ready-to-eat, granola, homemade", 489, 13.67, 8.9, 19.8, gluten_risk=True, note="The author did not name a granola brand. Homemade granola is the USDA record used, and it counts as a gluten risk because of the oats."),
    {
        "id": "rice-paper",
        "pantryId": "rice-paper",
        "name": "Rice paper sheets",
        "fdcId": None,
        "fdcName": None,
        "dataset": None,
        "fdcUrl": None,
        "per100g": None,
        "allergens": [],
        "glutenRisk": False,
        "note": "SR Legacy (April 2018) and Foundation Foods (April 2026) have no rice-paper wrapper. Wonton wrappers were not used as a stand-in: USDA says they include egg-roll wrappers, which contain wheat.",
    },
]

PANTRY = [
    {"id": "banana", "name": "Bananas", "group": "Fruit", "hint": "The spottier, the sweeter"},
    {"id": "strawberries", "name": "Strawberries", "group": "Fruit", "hint": "Fresh berries"},
    {"id": "blueberries", "name": "Blueberries", "group": "Fruit", "hint": "Fresh berries"},
    {"id": "peanut-butter", "name": "Peanut butter", "group": "Jars", "hint": "Creamy or crunchy"},
    {"id": "powdered-peanut", "name": "Powdered peanut butter", "group": "Jars", "hint": "Like PB2"},
    {"id": "almond-butter", "name": "Almond butter", "group": "Jars", "hint": "A nut butter"},
    {"id": "sunflower-butter", "name": "Sunflower butter", "group": "Jars", "hint": "A peanut-free spread"},
    {"id": "honey", "name": "Honey", "group": "Jars", "hint": "Not for babies under 1"},
    {"id": "maple", "name": "Maple syrup", "group": "Jars", "hint": "The real syrup"},
    {"id": "greek-yogurt", "name": "Greek yogurt", "group": "Cold", "hint": "Plain or vanilla"},
    {"id": "yogurt", "name": "Yogurt", "group": "Cold", "hint": "A yogurt cup"},
    {"id": "cottage-cheese", "name": "Cottage cheese", "group": "Cold", "hint": "Curds in a tub"},
    {"id": "milk", "name": "Milk", "group": "Cold", "hint": "From the fridge"},
    {"id": "almond-milk", "name": "Almond milk", "group": "Cold", "hint": "A carton"},
    {"id": "egg", "name": "Eggs", "group": "Cold", "hint": "In the carton"},
    {"id": "mozzarella", "name": "Mozzarella", "group": "Cold", "hint": "Shredded cheese"},
    {"id": "butter", "name": "Butter", "group": "Cold", "hint": "A stick of butter"},
    {"id": "oats", "name": "Oats", "group": "Baking", "hint": "Rolled or quick"},
    {"id": "flour", "name": "Flour", "group": "Baking", "hint": "All-purpose"},
    {"id": "whole-wheat", "name": "Whole-wheat flour", "group": "Baking", "hint": "Brown flour"},
    {"id": "almond-flour", "name": "Almond flour", "group": "Baking", "hint": "Ground almonds"},
    {"id": "baking-powder", "name": "Baking powder", "group": "Baking", "hint": "The can that makes things rise"},
    {"id": "baking-soda", "name": "Baking soda", "group": "Baking", "hint": "The orange box"},
    {"id": "vanilla", "name": "Vanilla", "group": "Baking", "hint": "The little brown bottle"},
    {"id": "cinnamon", "name": "Cinnamon", "group": "Baking", "hint": "Warm spice"},
    {"id": "salt", "name": "Salt", "group": "Baking", "hint": "A pinch"},
    {"id": "cocoa", "name": "Cocoa powder", "group": "Baking", "hint": "Unsweetened cocoa"},
    {"id": "brown-sugar", "name": "Brown sugar", "group": "Baking", "hint": "Soft brown sugar"},
    {"id": "protein-powder", "name": "Protein powder", "group": "Baking", "hint": "A scoop jar"},
    {"id": "chocolate", "name": "Chocolate chips", "group": "Sweet", "hint": "Chips or a bar"},
    {"id": "raisins", "name": "Raisins", "group": "Sweet", "hint": "Dried grapes"},
    {"id": "coconut", "name": "Coconut", "group": "Sweet", "hint": "Flakes or shredded"},
    {"id": "granola", "name": "Granola", "group": "Sweet", "hint": "Crunchy clusters"},
    {"id": "walnuts", "name": "Walnuts", "group": "Crunch", "hint": "Chopped nuts"},
    {"id": "coconut-oil", "name": "Coconut oil", "group": "Crunch", "hint": "In a jar"},
    {"id": "olive-oil", "name": "Olive oil", "group": "Crunch", "hint": "Cooking oil"},
    {"id": "bacon", "name": "Bacon", "group": "Savory", "hint": "Cooked strips"},
    {"id": "rice-paper", "name": "Rice paper", "group": "Savory", "hint": "Round spring-roll sheets"},
    {"id": "oregano", "name": "Oregano", "group": "Savory", "hint": "Dried leaves"},
    {"id": "onion-powder", "name": "Onion powder", "group": "Savory", "hint": "A spice jar"},
    {"id": "garlic-powder", "name": "Garlic powder", "group": "Savory", "hint": "A spice jar"},
]

FOOD_BY_ID = {f["id"]: f for f in FOODS}


def line(food_id, amount, grams, note, count=1, optional=False):
    food_row = FOOD_BY_ID[food_id]
    return {
        "foodId": food_id,
        "pantryId": food_row["pantryId"],
        "amount": amount,
        "grams": round(grams, 2) if grams is not None else None,
        "count": count,
        "optional": optional,
        "gramNote": note,
    }


def swap(sid, removes, label, source, *, adds=None, same_grams=False, author=False):
    return {
        "id": sid,
        "removesPantry": removes,
        "label": label,
        "source": source,
        "author": author,
        "sameGrams": same_grams,
        "adds": adds or [],
    }


EGG_YOGURT = swap(
    "egg-yogurt",
    "egg",
    "No egg? Use 1/4 cup plain Greek yogurt for each egg.",
    "A common baking swap. The recipe writer did not test this version. Counted as low-fat plain Greek yogurt, 56.5 g per egg, from a published 1/2 cup = 113 g.",
    adds=[{"foodId": "greek-lowfat", "gramsEach": round(CUP_GREEK / 4, 2)}],
)


def R(rid, title, category, blurb, servings, serving_label, minutes, source_name, source_url, author, lines, steps, swaps=None, unquantified=None, heat="oven"):
    return {
        "id": rid,
        "title": title,
        "category": category,
        "blurb": blurb,
        "servings": servings,
        "servingLabel": serving_label,
        "minutes": minutes,
        "heat": heat,
        "sourceName": source_name,
        "sourceUrl": source_url,
        "author": author,
        "lines": lines,
        "swaps": swaps or [],
        "unquantified": unquantified or [],
        "steps": steps,
    }


# Short kid steps. Temperatures and times match the published method.
recipes = []

recipes.append(R(
    "quaker-pb-banana-bites",
    "Peanut butter banana bites",
    "Bites",
    "Five ingredients, no oven, and a banana does the sweetening.",
    24, "1 bite", 40,
    "Quaker Oats",
    "https://www.quakeroats.com/cooking-and-recipes/peanut-butter-and-banana-energy-bites",
    "Quaker Oats",
    [
        line("oats", "2 1/2 cups oats", 2.5 * CUP_OATS, "USDA 1 cup dry oats = 81 g."),
        line("cinnamon", "1 tsp cinnamon", TSP_CINN, "USDA 1 tsp ground cinnamon = 2.6 g."),
        line("banana", "1 cup mashed banana", CUP_MASHED_BANANA, "USDA 1 cup mashed banana = 225 g. Quaker says that is about 2 large bananas."),
        line("pb-salted", "1/4 cup peanut butter", CUP_PB / 4, "USDA 1 cup peanut butter = 258 g."),
        line("honey", "2 tbsp honey", 2 * TBSP_HONEY, "USDA 1 tbsp honey = 21 g."),
    ],
    [
        {"text": "Wash your hands. Put the oats and cinnamon in a big bowl. Stir.", "grownup": []},
        {"text": "Ask a grown-up to help mash the banana. Add the banana, peanut butter, and honey. Stir until every oat looks sticky.", "grownup": []},
        {"text": "Roll the mix into 24 little balls, about the size of a big marble.", "grownup": []},
        {"text": "Cover the bowl and let the bites get cold in the fridge.", "timerSec": 1800, "timerLabel": "30 minutes", "grownup": []},
    ],
    heat="none",
))

recipes.append(R(
    "yummy-toddler-energy-balls",
    "Peanut butter oatmeal balls",
    "Bites",
    "Cookie-dough bites from Yummy Toddler Food. Honey is the glue.",
    16, "1 ball", 20,
    "Yummy Toddler Food",
    "https://www.yummytoddlerfood.com/oatmeal-raisin-peanut-butter-energy-balls/",
    "Amy Palanjian",
    [
        line("pb-unsalted", "1/2 cup peanut butter", CUP_PB / 2, "USDA 1 cup natural peanut butter = 258 g. Amy uses unsweetened creamy peanut butter."),
        line("honey", "1/4 cup honey", CUP_HONEY / 4, "USDA 1 cup honey = 339 g."),
        line("oats", "1 cup rolled oats", CUP_OATS, "USDA 1 cup rolled oats = 81 g. Amy grinds them a little, which does not change the weight."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla extract = 4.2 g."),
        line("raisins", "1/4 cup raisins", CUP_RAISIN / 4, "USDA 1 cup raisins, not packed = 145 g. Amy says they are optional but recommended. They are in her ingredient list, so they are counted."),
    ],
    [
        {"text": "Ask a grown-up to warm the peanut butter and honey for a few seconds so they stir easily.", "grownup": ["microwave"]},
        {"text": "Pour that into a bowl. Add the oats, vanilla, and raisins. Stir, then squish with clean hands if the spoon gets stuck.", "grownup": []},
        {"text": "Scoop tablespoon-size mounds and roll 16 balls.", "grownup": []},
        {"text": "Eat, or keep them in a covered box in the fridge.", "grownup": []},
    ],
    unquantified=["1 tsp chia seeds. SR Legacy only publishes chia by the ounce (28.35 g), not by the teaspoon, so chia is left out of the numbers. Amy says you can skip it."],
    heat="microwave",
))

recipes.append(R(
    "best-ideas-pb-balls",
    "No-bake snack bites",
    "Bites",
    "Oats, peanut butter, honey, and a pocket of chocolate, coconut, and raisins.",
    20, "1 bite", 40,
    "The Best Ideas for Kids",
    "https://www.thebestideasforkids.com/no-bake-peanut-butter-snack-bites/",
    "The Best Ideas for Kids",
    [
        line("oats", "1 cup rolled oats", CUP_OATS, "USDA 1 cup rolled oats = 81 g."),
        line("pb-salted", "1/2 cup peanut butter", CUP_PB / 2, "USDA 1 cup peanut butter = 258 g."),
        line("honey", "1/4 cup honey", CUP_HONEY / 4, "USDA 1 cup honey = 339 g. The page says honey is only for kids over 1."),
        line("chips", "1/4 cup mini chocolate chips", CUP_MINI / 4, "USDA 1 cup mini chocolate chips = 173 g."),
        line("raisins", "1/4 cup raisins", CUP_RAISIN / 4, "USDA 1 cup raisins, not packed = 145 g."),
        line("coconut", "1/4 cup coconut flakes", CUP_COCONUT / 4, "Cup weight 93 g is from sweetened shredded coconut. Nutrients are unsweetened dried coconut."),
    ],
    [
        {"text": "Put the peanut butter and honey in a bowl. Stir them together.", "grownup": []},
        {"text": "Add the oats, chocolate chips, raisins, and coconut. Mix until you do not see dry oats.", "grownup": []},
        {"text": "Roll 20 balls. The page uses about 2 tablespoons of mix for each one.", "grownup": []},
        {"text": "Chill them until they feel firm.", "timerSec": 1800, "timerLabel": "30 minutes", "grownup": []},
    ],
    heat="none",
))

recipes.append(R(
    "marisa-pb-banana-cookies",
    "Peanut butter banana breakfast cookies",
    "Cookies",
    "Three ingredients. Mash, mix, bake.",
    6, "1 serving", 15,
    "Marisa Moore Nutrition",
    "https://marisamoore.com/peanut-butter-banana-breakfast-cookies/",
    "Marisa Moore, RDN",
    [
        line("banana", "2 small bananas", 2 * SMALL_BANANA, "USDA 1 small banana = 101 g. Marisa's card says 6 servings, and also says you can roll 10 to 12 small cookies or 5 to 6 large ones."),
        line("oats", "1 cup old-fashioned oats", CUP_OATS, "USDA 1 cup oats = 81 g."),
        line("pb-unsalted", "1/4 cup natural peanut butter", CUP_PB / 4, "USDA 1 cup peanut butter = 258 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Lightly oil a baking sheet.", "grownup": ["oven"]},
        {"text": "Mash the bananas in a bowl. Add the oats and peanut butter. Mix.", "grownup": []},
        {"text": "Roll and flatten the cookies. Marisa makes 5 or 6 large ones for the 6 servings on her card.", "grownup": []},
        {"text": "Bake until the cookies look golden.", "timerSec": 12 * 60, "timerLabel": "12 minutes", "grownup": ["oven"]},
        {"text": "Let a grown-up take the pan out. Cool a little before you grab one.", "grownup": ["oven"]},
    ],
))

recipes.append(R(
    "plant-kitchen-pb-cookies",
    "3-ingredient banana oat cookies",
    "Cookies",
    "No egg, no milk, and no extra sugar. The banana is the sweet part.",
    8, "1 cookie", 22,
    "The Conscious Plant Kitchen",
    "https://www.theconsciousplantkitchen.com/peanut-butter-banana-oatmeal-cookies/",
    "Carine Claudepierre",
    [
        line("banana", "1/2 cup mashed banana", CUP_MASHED_BANANA / 2, "Carine says 1 medium banana equals 1/2 cup mashed. USDA 1 cup mashed = 225 g, so half is 112.5 g. A USDA medium banana is 118 g."),
        line("pb-unsalted", "1/4 cup unsalted peanut butter", CUP_PB / 4, "USDA 1 cup peanut butter = 258 g."),
        line("oats", "1 1/4 cups rolled oats", 1.25 * CUP_OATS, "USDA 1 cup oats = 81 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a cookie sheet with parchment paper.", "grownup": ["oven"]},
        {"text": "Mash the banana. Check that you have about 1/2 cup. Stir in the peanut butter and oats.", "grownup": []},
        {"text": "Make 8 balls. Flatten them with a slightly oily hand. They will not spread in the oven.", "grownup": []},
        {"text": "Bake until the edges look golden.", "timerSec": 15 * 60, "timerLabel": "15 minutes", "grownup": ["oven"]},
        {"text": "Cool on a rack. Carine waits about 20 minutes. They taste sweeter once they cool.", "timerSec": 20 * 60, "timerLabel": "20 minutes", "grownup": ["oven"]},
    ],
))

recipes.append(R(
    "skinnytaste-banana-cookies",
    "Banana oatmeal walnut cookies",
    "Cookies",
    "Gina's three-ingredient cookies. Two of them make one serving.",
    8, "2 cookies", 25,
    "Skinnytaste",
    "https://www.skinnytaste.com/healthy-cookies/",
    "Gina Homolka",
    [
        line("banana", "2 medium bananas", 2 * MEDIUM_BANANA, "USDA 1 medium banana = 118 g."),
        line("oats", "1 cup quick oats", CUP_OATS, "USDA 1 cup dry oats = 81 g. Gina says rolled oats can stand in for quick oats."),
        line("walnuts", "1/4 cup crushed walnuts", CUP_WALNUT / 4, "USDA 1 cup chopped walnuts = 117 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Set out a cookie sheet.", "grownup": ["oven"]},
        {"text": "Mash the bananas. Stir in the oats. Fold in the walnuts.", "grownup": []},
        {"text": "Drop tablespoon mounds on the sheet. Gina's batch makes 16 cookies.", "grownup": []},
        {"text": "Bake.", "timerSec": 15 * 60, "timerLabel": "15 minutes", "grownup": ["oven"]},
        {"text": "Cool before you eat. A serving is 2 cookies.", "grownup": ["oven"]},
    ],
))

recipes.append(R(
    "power-hungry-protein-cookies",
    "Banana oat protein cookies",
    "Cookies",
    "Four ingredients and a scoop of protein powder. Camilla's batch makes 20 cookies.",
    20, "1 cookie", 20,
    "Power Hungry",
    "https://www.powerhungry.com/2015/01/15/banana-oat-protein-cookies/",
    "Camilla",
    [
        line("oats", "1 1/2 cups rolled oats", 1.5 * CUP_OATS, "USDA 1 cup oats = 81 g."),
        line("banana", "1 cup mashed banana", CUP_MASHED_BANANA, "USDA 1 cup mashed banana = 225 g. Camilla says that is about 2 to 3 large bananas."),
        line("almond-butter", "1/4 cup almond butter", CUP_ALMOND_BUTTER / 4, "USDA 1 cup almond butter = 250 g."),
        line("soy-protein", "1/4 cup plant protein powder", CUP_PROTEIN / 4, "Camilla does not give grams. 1/4 cup is 24 g because USDA whey protein powder lists 1/3 cup = 32 g (1 cup = 96 g). Nutrients are soy protein powder, the plant-protein record."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a baking sheet.", "grownup": ["oven"]},
        {"text": "Ask a grown-up to grind half of the oats (3/4 cup) into a coarse meal.", "grownup": []},
        {"text": "Stir the mashed banana and almond butter. Add all the oats and the protein powder. Mix.", "grownup": []},
        {"text": "Roll 1-inch balls and flatten them a little. They do not spread.", "grownup": []},
        {"text": "Bake until the edges are golden. Camilla says 11 to 15 minutes.", "timerSec": 13 * 60, "timerLabel": "13 minutes", "grownup": ["oven"]},
        {"text": "Move the cookies to a rack and let them cool.", "grownup": ["oven"]},
    ],
    swaps=[
        swap("almond-to-pb", "almond-butter", "Camilla says peanut butter can replace the almond butter, same amount.", "Power Hungry recipe notes.", same_grams=True, author=True, adds=[{"foodId": "pb-unsalted", "gramsEach": None}]),
        swap("almond-to-sun", "almond-butter", "Camilla says sunflower seed butter can replace the almond butter, same amount.", "Power Hungry recipe notes.", same_grams=True, author=True, adds=[{"foodId": "sunflower-butter", "gramsEach": None}]),
    ],
))

recipes.append(R(
    "taste-cottage-cookie-dough",
    "Cottage cheese cookie dough",
    "Bites",
    "The viral edible dough. No raw flour. It stays in the fridge.",
    4, "1 serving", 10,
    "Taste of Home",
    "https://www.tasteofhome.com/recipes/cottage-cheese-cookie-dough/",
    "Taste of Home Test Kitchen",
    [
        line("cottage-4", "1 cup 4% cottage cheese", CUP_COTTAGE_4, "USDA 1 cup small-curd creamed cottage cheese, not packed = 225 g."),
        line("maple", "3 tbsp maple syrup", 3 * TBSP_MAPLE, "USDA 1 tbsp maple syrup = 20 g."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("almond-flour", "1 1/2 cups almond flour", 1.5 * CUP_ALMOND_FLOUR, "1 cup ground almonds = 95 g on FDC 170567. Nutrients are blanched almonds, FDC 170568."),
        line("whey", "1/4 cup vanilla whey protein powder", CUP_PROTEIN / 4, "1/4 cup = 24 g from the whey powder cup fraction. Nutrients are unflavored whey-based powder, not a sweetened vanilla tub."),
        line("chips", "1/2 cup mini semisweet chocolate chips", CUP_MINI / 2, "USDA 1 cup mini chips = 173 g."),
    ],
    [
        {"text": "Ask a grown-up to blend the cottage cheese, maple syrup, and vanilla until smooth.", "grownup": []},
        {"text": "Scrape it into a bowl. Stir in the almond flour and protein powder.", "grownup": []},
        {"text": "Fold in the chocolate chips. Taste. Add a tiny pinch of salt only if a grown-up says it needs it.", "grownup": []},
        {"text": "Keep it in a covered container in the fridge. Scoop and eat.", "grownup": []},
    ],
    heat="none",
))

recipes.append(R(
    "bird-flatbread",
    "Cottage cheese flatbread",
    "Flatbread",
    "The viral two-main-ingredient flatbread. One wrap, a lot of protein.",
    1, "1 flatbread", 30,
    "Eating Bird Food",
    "https://www.eatingbirdfood.com/cottage-cheese-flatbread/",
    "Brittany Mullins",
    [
        line("cottage-4", "1 cup full-fat cottage cheese", CUP_COTTAGE_4, "USDA 1 cup small-curd creamed cottage cheese = 225 g. Brittany uses Good Culture full-fat."),
        line("egg", "2 eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("oregano", "1 tsp dried oregano", TSP_OREGANO, "USDA 1 tsp dried oregano leaves = 1 g."),
        line("onion-powder", "1/4 tsp onion powder", TSP_ONION / 4, "USDA 1 tsp onion powder = 2.4 g."),
        line("garlic-powder", "1/4 tsp garlic powder", TSP_GARLIC / 4, "USDA 1 tsp garlic powder = 3.1 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F.", "grownup": ["oven"]},
        {"text": "Blend the cottage cheese, eggs, oregano, onion powder, and garlic powder until smooth.", "grownup": []},
        {"text": "Line a small sheet pan with parchment. A grown-up sprays it. Pour the mix on and spread it thin.", "grownup": []},
        {"text": "Bake until it is cooked through and golden in spots.", "timerSec": 25 * 60, "timerLabel": "25 minutes", "grownup": ["oven"]},
        {"text": "Cool a few minutes. Peel it off the paper. Fill it, roll it, and cut it in half.", "grownup": ["knife"]},
    ],
))

recipes.append(R(
    "urban-farmie-bark",
    "Cottage cheese berry bark",
    "Bark",
    "A frozen bark with cottage cheese, yogurt, berries, and coconut.",
    6, "1 serving", 15,
    "Urban Farmie",
    "https://urbanfarmie.com/cottage-cheese-bark/",
    "Shruthi Baskaran-Makanju",
    [
        line("cottage-4", "2 cups whole-milk cottage cheese", 2 * CUP_COTTAGE_4, "USDA 1 cup small-curd creamed cottage cheese = 225 g."),
        line("greek-vanilla-low", "1 cup vanilla Greek yogurt", CUP_GREEK, "No USDA cup for Greek yogurt. 1 cup = 226 g from Ambitious Kitchen's printed 1/2 cup = 113 g. Shruthi does not name a fat level, so low-fat vanilla Greek yogurt is used."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("honey", "2 tbsp honey", 2 * TBSP_HONEY, "USDA 1 tbsp honey = 21 g."),
        line("strawberries", "1 cup sliced strawberries", CUP_STRAW_SLICED, "USDA 1 cup sliced strawberries = 166 g."),
        line("blueberries", "1 cup blueberries", CUP_BERRIES, "USDA 1 cup blueberries = 148 g."),
        line("coconut", "1/2 cup unsweetened shredded coconut", CUP_COCONUT / 2, "Cup weight from sweetened shredded coconut. Nutrients are unsweetened."),
    ],
    [
        {"text": "Line a tray with parchment paper. Make sure it fits in the freezer.", "grownup": []},
        {"text": "Blend the cottage cheese, yogurt, vanilla, and honey until completely smooth.", "grownup": []},
        {"text": "Pat the berries dry. Fold them in with a spoon so you see streaks of color.", "grownup": []},
        {"text": "Spread the mix about as thick as a pencil. Sprinkle the coconut on top.", "grownup": []},
        {"text": "Freeze until solid.", "timerSec": 4 * 60 * 60, "timerLabel": "4 hours", "grownup": []},
        {"text": "Break the bark into pieces. Eat it frozen.", "grownup": []},
    ],
    heat="none",
))

recipes.append(R(
    "daisybeet-muffins",
    "Greek yogurt banana oat muffins",
    "Muffins",
    "Fluffy muffins with a whole cup of Greek yogurt. A dietitian's recipe.",
    12, "1 muffin", 25,
    "Daisybeet",
    "https://www.daisybeet.com/healthy-banana-oat-muffins-with-greek-yogurt/",
    "Alex Aldeborgh, RD",
    [
        line("banana", "2 very ripe bananas", 2 * MEDIUM_BANANA, "Alex says very ripe bananas and does not give a size. USDA medium banana = 118 g is used for each."),
        line("greek-lowfat", "1 cup plain Greek yogurt", CUP_GREEK, "Alex allows 2% or 5%. Low-fat (2%) Greek yogurt is counted. 1 cup = 226 g from a published 1/2 cup = 113 g, because SR Legacy has no Greek yogurt cup."),
        line("egg", "1 large egg", LARGE_EGG, "USDA 1 large egg = 50 g.", count=1),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("brown-sugar", "1/2 cup light brown sugar", CUP_BROWN / 2, "USDA 1 packed cup brown sugar = 220 g. Alex does not say packed. Packed is used."),
        line("flour", "1 1/2 cups all-purpose flour", 1.5 * CUP_AP, "USDA 1 cup all-purpose flour = 125 g."),
        line("oats", "1/3 cup rolled oats", CUP_OATS / 3, "USDA lists 1/3 cup oats = 27 g."),
        line("cinnamon", "1 tsp cinnamon", TSP_CINN, "USDA 1 tsp cinnamon = 2.6 g."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("baking-soda", "1 tsp baking soda", TSP_BS, "USDA 1 tsp baking soda = 4.6 g."),
        line("salt", "1/2 tsp salt", TSP_SALT / 2, "USDA 1 tsp table salt = 6 g. Salt adds no calories, protein, fiber, or sugar in this record."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 425°F. Line a muffin tin.", "grownup": ["oven"]},
        {"text": "Mash the bananas. Stir in the yogurt, egg, vanilla, and brown sugar.", "grownup": []},
        {"text": "In another bowl, whisk the flour, oats, cinnamon, baking powder, baking soda, and salt.", "grownup": []},
        {"text": "Pour the wet mix into the dry mix. Stir just until you do not see dry flour. The batter is thick.", "grownup": []},
        {"text": "Fill the cups almost to the top.", "grownup": []},
        {"text": "Bake 5 minutes at 425°F. Then a grown-up turns the oven down to 350°F.", "timerSec": 5 * 60, "timerLabel": "5 minutes", "grownup": ["oven"]},
        {"text": "Bake until a toothpick comes out clean. Alex says another 8 to 12 minutes.", "timerSec": 10 * 60, "timerLabel": "10 minutes", "grownup": ["oven"]},
        {"text": "Cool a few minutes before you pick one up.", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
))

recipes.append(R(
    "bethenny-bagels",
    "Cottage cheese bagels",
    "Bagels",
    "Four bagels from cottage cheese, flour, and baking powder.",
    4, "1 bagel", 35,
    "Bethenny",
    "https://bethenny.com/blogs/recipes/bethenny-cottage-cheese-bagel-recipe",
    "Bethenny Frankel",
    [
        line("cottage-4", "1 1/4 cups blended cottage cheese", 1.25 * CUP_COTTAGE_4, "Bethenny says regular cottage cheese, blended. USDA small-curd creamed cup = 225 g."),
        line("flour", "1 cup all-purpose flour", CUP_AP, "USDA 1 cup all-purpose flour = 125 g."),
        line("baking-powder", "1 1/2 tsp baking powder", 1.5 * TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("egg", "1 egg, for the wash", LARGE_EGG, "USDA 1 large egg = 50 g. The wash is brushed on and baked, so the egg is counted.", count=1),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 375°F with the baking sheet inside.", "grownup": ["oven"]},
        {"text": "Stir the blended cottage cheese, flour, and baking powder into a sticky dough.", "grownup": []},
        {"text": "Flour the counter. A grown-up divides the dough into 4 pieces. Shape balls, then poke a thumb through the middle to make bagel holes.", "grownup": ["knife"]},
        {"text": "Brush the tops with beaten egg.", "grownup": []},
        {"text": "A grown-up moves the parchment onto the hot sheet. Bake until golden.", "timerSec": 25 * 60, "timerLabel": "25 minutes", "grownup": ["oven"]},
        {"text": "Cool a little, then eat.", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
    unquantified=["Everything bagel seasoning and flaky salt. Bethenny does not give amounts, so they are not in the numbers."],
))

recipes.append(R(
    "nic-cookie-dough-bark",
    "Cottage cheese cookie dough bark",
    "Bark",
    "Cookie dough you freeze, then break. Nic's batch is 16 pieces.",
    16, "1 piece", 20,
    "Nourished by Nic",
    "https://nourishedbynic.com/cottage-cheese-cookie-dough-bark/",
    "Nic",
    [
        line("cottage-2", "1 cup 2% cottage cheese", CUP_COTTAGE_2, "USDA 1 cup 2% cottage cheese, not packed = 226 g."),
        line("pb-unsalted", "2 tbsp natural peanut butter", 2 * TBSP_PB, "USDA 1 tbsp peanut butter = 16 g."),
        line("maple", "1 tbsp maple syrup", TBSP_MAPLE, "USDA 1 tbsp maple syrup = 20 g."),
        line("vanilla", "2 tsp vanilla", 2 * TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("oats", "1 cup oat flour", CUP_OATS + 2 * TBSP_OATS, "Nic says 1 cup oat flour is 1 cup plus 2 tablespoons of whole oats blended. USDA cup = 81 g and 2 tbsp = 10.13 g."),
        line("whey", "1/4 cup vanilla protein powder", CUP_PROTEIN / 4, "1/4 cup = 24 g from the whey cup fraction. Nutrients are unflavored whey-based powder."),
        line("chips", "1/3 cup chocolate chips", CUP_CHIPS / 3, "USDA 1 cup chocolate chips = 168 g."),
        line("chips", "1 cup chocolate chips for the topping", CUP_CHIPS, "USDA 1 cup chocolate chips = 168 g."),
        line("coconut-oil", "2 tsp coconut oil", 2 * (TBSP_COCONUT_OIL / 3), "USDA 1 tsp coconut oil = 4.5 g."),
    ],
    [
        {"text": "Blend the cottage cheese, peanut butter, maple syrup, and vanilla until smooth.", "grownup": []},
        {"text": "Stir in the oat flour and protein powder. Then stir in 1/3 cup of chocolate chips.", "grownup": []},
        {"text": "Spread the dough on parchment. Wet the spatula if it sticks.", "grownup": []},
        {"text": "Ask a grown-up to melt 1 cup of chocolate chips with the coconut oil, 30 seconds at a time.", "grownup": ["microwave"]},
        {"text": "Spread the chocolate over the dough.", "grownup": []},
        {"text": "Freeze until hard. Nic says at least 2 hours.", "timerSec": 2 * 60 * 60, "timerLabel": "2 hours", "grownup": []},
        {"text": "Break into about 16 pieces. Keep them in the freezer.", "grownup": []},
    ],
    heat="microwave",
))

recipes.append(R(
    "saucy-cc-muffins",
    "Banana cottage cheese muffins",
    "Muffins",
    "Blended cottage cheese muffins. The author printed several gram weights.",
    12, "1 muffin", 30,
    "The Saucy Chickpea",
    "https://thesaucychickpea.com/recipes/banana-cottage-cheese-muffins",
    "The Saucy Chickpea",
    [
        line("cottage-4", "1 cup (240 g) cottage cheese", 240, "The author printed 240 g. Fat level is not named, so creamed cottage cheese (4%) is used."),
        line("banana", "2 ripe bananas", 2 * MEDIUM_BANANA, "Size is not named. USDA medium banana = 118 g is used for each."),
        line("egg", "2 eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("maple", "1/4 cup (60 ml) maple syrup", CUP_MAPLE / 4, "USDA 1 cup maple syrup = 315 g. The author also wrote 60 ml. The cup fraction is used."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("oats", "1 1/2 cups (150 g) oat flour", 150, "The author printed 150 g. Nutrients are dry rolled oats, because oat flour is milled oats."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("baking-soda", "1/2 tsp baking soda", TSP_BS / 2, "USDA 1/2 tsp baking soda = 2.3 g."),
        line("cinnamon", "1 tsp cinnamon", TSP_CINN, "USDA 1 tsp cinnamon = 2.6 g."),
        line("salt", "1/4 tsp salt", TSP_SALT / 4, "USDA 1 tsp salt = 6 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a muffin tin.", "grownup": ["oven"]},
        {"text": "Blend the cottage cheese, bananas, eggs, maple syrup, and vanilla until smooth.", "grownup": []},
        {"text": "Stir in the oat flour, baking powder, baking soda, cinnamon, and salt. Stop when the flour disappears.", "grownup": []},
        {"text": "Fill the cups about 3/4 full.", "grownup": []},
        {"text": "Bake until the tops spring back. The page says 18 to 22 minutes.", "timerSec": 20 * 60, "timerLabel": "20 minutes", "grownup": ["oven"]},
        {"text": "Cool 10 minutes in the tin.", "timerSec": 10 * 60, "timerLabel": "10 minutes", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
    unquantified=["Optional 1/2 cup chocolate chips or walnuts. Left out of the count."],
))

recipes.append(R(
    "savory-banana-mug",
    "Banana yogurt oat mug cake",
    "Mug cakes",
    "One mug. About a minute in the microwave.",
    1, "1 mug cake", 5,
    "Savory Mom Kitchen",
    "https://savorymomskitchen.com/1-minute-banana-yogurt-oat-mug-cake/",
    "Sophia",
    [
        line("banana", "1 ripe banana", MEDIUM_BANANA, "Size is not named. USDA medium banana = 118 g."),
        line("greek-lowfat", "1/4 cup plain Greek yogurt", CUP_GREEK / 4, "1/4 cup = 56.5 g from the published 1/2 cup = 113 g. Fat level is not named, so low-fat plain Greek yogurt is used."),
        line("oats", "1/2 cup rolled oats", CUP_OATS / 2, "USDA 1 cup oats = 81 g. Sophia blends them into flour first. The weight stays the same."),
        line("baking-powder", "1/2 tsp baking powder", TSP_BP / 2, "USDA 1/2 tsp baking powder = 2.3 g."),
        line("vanilla", "1/2 tsp vanilla", TSP_VANILLA / 2, "USDA 1 tsp vanilla = 4.2 g."),
    ],
    [
        {"text": "Blend the oats into a soft flour. A grown-up can help with the blender.", "grownup": []},
        {"text": "Mash the banana in a microwave-safe mug. Stir in the yogurt and vanilla.", "grownup": []},
        {"text": "Stir in the oat flour and baking powder. Leave room at the top so it can rise.", "grownup": []},
        {"text": "Ask a grown-up to microwave it for about 60 seconds. Add 10 seconds only if the center still looks wet.", "timerSec": 60, "timerLabel": "1 minute", "grownup": ["microwave"]},
        {"text": "Rest 1 minute. The mug is hot. Eat from the mug.", "timerSec": 60, "timerLabel": "1 minute", "grownup": ["microwave"]},
    ],
    unquantified=["Optional cinnamon, and an optional drizzle of honey or maple syrup. Left out of the count."],
    heat="microwave",
))

recipes.append(R(
    "rita-cottage-mug",
    "Cottage cheese banana mug cake",
    "Mug cakes",
    "A tiny banana-bread cake with cottage cheese, ready in about a minute.",
    1, "1 mug cake", 5,
    "Rita Mug Cakes",
    "https://ritamugcakes.com/cottage-cheese-banana-bread-mug-cake/",
    "Rita Mug Cakes",
    [
        line("banana", "1/2 ripe banana", MEDIUM_BANANA / 2, "Size is not named. Half of a USDA medium banana (118 g) is used."),
        line("cottage-4", "2 tbsp cottage cheese", 2 * CUP_COTTAGE_4 / 16, "Scaled from the USDA small-curd cup, 225 g. Fat level is not named, so creamed cottage cheese is used."),
        line("egg", "1 egg", LARGE_EGG, "USDA 1 large egg = 50 g.", count=1),
        line("oats", "1 tbsp oat flour", TBSP_OATS, "No USDA tablespoon for oat flour. 1 tbsp dry oats = 5.06 g is used, and the screen says oat flour can weigh a little more."),
        line("baking-powder", "1/2 tsp baking powder", TSP_BP / 2, "USDA 1/2 tsp baking powder = 2.3 g."),
        line("vanilla", "1/2 tsp vanilla", TSP_VANILLA / 2, "USDA 1 tsp vanilla = 4.2 g."),
    ],
    [
        {"text": "Mash the banana in a microwave-safe mug.", "grownup": []},
        {"text": "Add the cottage cheese, egg, and vanilla. Mix well.", "grownup": []},
        {"text": "Stir in the oat flour and baking powder.", "grownup": []},
        {"text": "Ask a grown-up to microwave it until the top is set. The page says 60 to 90 seconds.", "timerSec": 75, "timerLabel": "75 seconds", "grownup": ["microwave"]},
        {"text": "Cool 1 to 2 minutes. The mug is hot.", "timerSec": 90, "timerLabel": "90 seconds", "grownup": ["microwave"]},
    ],
    swaps=[EGG_YOGURT, swap("oat-to-almond-flour", "oats", "Rita says almond flour can replace the oat flour, same tablespoon.", "Rita Mug Cakes recipe notes.", author=True, adds=[{"foodId": "almond-flour", "grams": round(TBSP_GROUND_ALMOND, 2)}])],
    unquantified=["Optional cinnamon, 1 tbsp chocolate chips, and a drizzle of maple syrup. Left out of the count."],
    heat="microwave",
))

recipes.append(R(
    "pur-cc-brownies",
    "Cottage cheese banana brownies",
    "Brownies",
    "A small pan of brownies sweetened with banana and maple syrup.",
    4, "1 brownie", 35,
    "Pur and Simple Recipes",
    "https://purandsimplerecipes.com/cottage-cheese-banana-brownies/",
    "Mary McQueen",
    [
        line("banana", "1 ripe banana", MEDIUM_BANANA, "Size is not named. USDA medium banana = 118 g."),
        line("cottage-4", "1/2 cup cottage cheese", CUP_COTTAGE_4 / 2, "Half of the USDA small-curd cup (225 g). Fat level is not named, so creamed cottage cheese is used."),
        line("cocoa", "1/4 cup cocoa powder", CUP_COCOA / 4, "USDA 1 cup unsweetened cocoa = 86 g."),
        line("maple", "1/4 cup maple syrup", CUP_MAPLE / 4, "USDA 1 cup maple syrup = 315 g."),
        line("oats", "1/2 cup oat flour", CUP_OATS / 2, "No oat-flour cup in SR Legacy. Half of the rolled-oat cup (81 g) is used. Oat flour can weigh more, so fiber may be a little low."),
        line("baking-powder", "1/2 tsp baking powder", TSP_BP / 2, "USDA 1/2 tsp baking powder = 2.3 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a small baking dish.", "grownup": ["oven"]},
        {"text": "Blend or stir the banana, cottage cheese, cocoa, and maple syrup until smooth.", "grownup": []},
        {"text": "Stir in the oat flour and baking powder.", "grownup": []},
        {"text": "Spread the batter in the dish.", "grownup": []},
        {"text": "Bake until a toothpick comes out clean. The page says 20 to 25 minutes.", "timerSec": 22 * 60, "timerLabel": "22 minutes", "grownup": ["oven"]},
        {"text": "Cool, then a grown-up cuts 4 brownies.", "grownup": ["knife", "oven"]},
    ],
))

recipes.append(R(
    "rachna-protein-brownies",
    "Yogurt cottage cheese protein brownies",
    "Brownies",
    "Egg-free brownies with yogurt, cottage cheese, and protein powder. Twelve bars.",
    12, "1 bar", 40,
    "Rachna's Kitchen",
    "https://rachnas-kitchen.com/eggless-chocolate-protein-brownies/",
    "Rachna's Kitchen",
    [
        line("flour", "1/4 cup wheat flour", CUP_AP / 4, "Rachna says wheat flour. All-purpose enriched flour is used. USDA 1 cup = 125 g."),
        line("oats", "1/4 cup rolled oats", CUP_OATS / 4, "USDA 1 cup oats = 81 g."),
        line("brown-sugar", "3/4 cup brown sugar", 0.75 * CUP_BROWN, "USDA 1 packed cup brown sugar = 220 g. Packed is assumed."),
        line("cocoa", "1/4 cup unsweetened cocoa", CUP_COCOA / 4, "USDA 1 cup cocoa = 86 g."),
        line("whey", "1/2 cup chocolate protein powder", CUP_PROTEIN / 2, "1/2 cup = 48 g from the whey cup fraction. Rachna used vanilla once and recommends chocolate. Nutrients are unflavored whey-based powder."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("greek-lowfat", "1/2 cup plus 1 tbsp Greek yogurt", CUP_GREEK / 2 + CUP_GREEK / 16, "Fat level is not named, so low-fat plain Greek yogurt is used. Cup weight 226 g comes from a published 1/2 cup = 113 g."),
        line("banana", "1/2 cup mashed banana", CUP_MASHED_BANANA / 2, "USDA 1 cup mashed banana = 225 g."),
        line("cottage-4", "1/4 cup cottage cheese", CUP_COTTAGE_4 / 4, "Quarter of the USDA small-curd cup. Fat level is not named, so creamed cottage cheese is used."),
        line("milk-skim", "1/4 cup skim milk", CUP_MILK_SKIM / 4, "USDA 1 cup skim milk = 245 g."),
        line("dark-70", "3 tbsp dark chocolate", 3 * CUP_CHIPS / 16, "No tablespoon for dark chocolate. 3 tbsp is scaled from the semisweet chip cup (168 g). Nutrients are dark chocolate, 70-85% cacao."),
        line("milk-skim", "2 tsp milk for the frosting", 2 * CUP_MILK_SKIM / 48, "2 tsp scaled from the USDA cup of skim milk (245 g)."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F and grease a baking pan.", "grownup": ["oven"]},
        {"text": "Stir the flour, protein powder, oats, baking powder, and cocoa in a bowl.", "grownup": []},
        {"text": "Mash the banana. Stir in the yogurt, cottage cheese, brown sugar, vanilla, and a tiny pinch of baking soda.", "grownup": []},
        {"text": "Ask a grown-up to heat the 1/4 cup of milk and melt chocolate into it, then stir that into the batter.", "grownup": ["stove"]},
        {"text": "Pour the batter into the pan. Bake until the top is set. Rachna says 18 to 22 minutes.", "timerSec": 20 * 60, "timerLabel": "20 minutes", "grownup": ["oven"]},
        {"text": "Cool. A grown-up melts 3 tablespoons of chocolate with 2 teaspoons of milk and pours it on top, then cuts 12 bars.", "grownup": ["microwave", "knife"]},
    ],
    unquantified=["A small pinch of baking soda. No gram weight was published, and baking soda would not change protein or fiber, so it is left out."],
))

recipes.append(R(
    "ambitious-oatmeal-cups",
    "Peanut butter banana oatmeal cups",
    "Muffins",
    "Baked oatmeal you can hold. Monique wrote gram weights for the big ingredients.",
    12, "1 cup", 35,
    "Ambitious Kitchen",
    "https://www.ambitiouskitchen.com/peanut-butter-banana-baked-oatmeal-cups/",
    "Monique Volz",
    [
        line("banana", "1 heaping cup mashed banana", CUP_MASHED_BANANA, "USDA 1 cup mashed banana = 225 g. Monique says heaping and does not give a heavier weight, so one level cup is counted."),
        line("pb-unsalted", "1/2 cup (128 g) peanut butter", 128, "Monique printed 128 g. Natural peanut butter, just peanuts and salt, uses the no-salt USDA record."),
        line("egg", "2 eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("maple", "2 tbsp maple syrup", 2 * TBSP_MAPLE, "USDA 1 tbsp maple syrup = 20 g."),
        line("almond-milk", "2/3 cup (160 g) unsweetened almond milk", 160, "Monique printed 160 g."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("oats", "2 cups (190 g) rolled oats", 190, "Monique printed 190 g."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("cinnamon", "1 tsp cinnamon", TSP_CINN, "USDA 1 tsp cinnamon = 2.6 g."),
        line("salt", "1/4 tsp salt", TSP_SALT / 4, "USDA 1 tsp salt = 6 g."),
        line("chips", "1/3 cup (60 g) chocolate chips", 60, "Monique printed 60 g."),
        line("chips", "2 tbsp chocolate chips on top", 22.5, "Scaled from Monique's 60 g per 1/3 cup, so 2 tbsp = 22.5 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line 12 muffin cups and spray the liners.", "grownup": ["oven"]},
        {"text": "Stir the banana, peanut butter, eggs, maple syrup, almond milk, and vanilla until smooth.", "grownup": []},
        {"text": "Stir in the oats, baking powder, cinnamon, and salt. Fold in 1/3 cup of chocolate chips.", "grownup": []},
        {"text": "Share the batter between the cups. Sprinkle the extra chips on top.", "grownup": []},
        {"text": "Bake until set. Monique says 20 to 25 minutes.", "timerSec": 22 * 60, "timerLabel": "22 minutes", "grownup": ["oven"]},
    ],
    swaps=[
        EGG_YOGURT,
        swap("maple-to-honey", "maple", "Monique says honey can replace the maple syrup.", "Ambitious Kitchen ingredient line: maple syrup or honey.", author=True, adds=[{"foodId": "honey", "grams": round(2 * TBSP_HONEY, 2)}]),
        swap("almond-milk-to-milk", "almond-milk", "Monique says any milk works. This swap uses 160 g of 2% milk, her printed weight.", "Ambitious Kitchen ingredient note.", author=True, adds=[{"foodId": "milk-2", "grams": 160}]),
    ],
    unquantified=["Optional 1/3 cup chopped walnuts. Left out of the count."],
))

recipes.append(R(
    "epicurean-yogurt-cookies",
    "Peanut butter yogurt chocolate cookies",
    "Cookies",
    "Greek yogurt cookies with chocolate. Julie's card makes 15.",
    15, "1 cookie", 20,
    "The Healthy Epicurean",
    "https://thehealthyepicurean.com/peanut-butter-yogurt-cookies-with-dark-chocolate/",
    "Julie Andrews",
    [
        line("pb-salted", "1 1/2 cups creamy peanut butter", 1.5 * CUP_PB, "USDA 1 cup peanut butter = 258 g. Julie says not to use the oil-on-top kind, so the salted smooth record is used."),
        line("greek-vanilla-low", "1/2 cup vanilla Greek yogurt", CUP_GREEK / 2, "1/2 cup = 113 g from a published Greek yogurt weight. Low-fat vanilla Greek yogurt is used. Julie says plain yogurt plus 1 tsp vanilla is the other choice, so extra vanilla is not added on top of the vanilla yogurt."),
        line("brown-sugar", "1/2 cup lightly packed brown sugar", CUP_BROWN / 2, "Julie allows 1/2 to 3/4 cup. The lower amount is counted. USDA packed cup = 220 g. She says lightly packed."),
        line("oats", "6 tbsp rolled oats", 6 * TBSP_OATS, "Scaled from USDA 1 cup oats = 81 g."),
        line("egg", "2 large eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("baking-soda", "1 tsp baking soda", TSP_BS, "USDA 1 tsp baking soda = 4.6 g."),
        line("salt", "1 tsp coarse salt", TSP_SALT, "USDA 1 tsp table salt = 6 g. Coarse salt weighs less. This record adds no protein, fiber, calories, or sugar either way."),
        line("dark-70", "1/2 cup dark chocolate chips", CUP_CHIPS / 2, "Dark chocolate has no chip-cup weight. Half of the semisweet chip cup (168 g) is used for the weight. Nutrients are dark chocolate, 70-85% cacao."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a baking sheet.", "grownup": ["oven"]},
        {"text": "Stir the peanut butter, yogurt, brown sugar, oats, eggs, baking soda, and salt until combined.", "grownup": []},
        {"text": "Fold in the chocolate. If the batter looks runny, Julie says to add a few more tablespoons of oats.", "grownup": []},
        {"text": "Scoop mounds onto the sheet, a little bit apart.", "grownup": []},
        {"text": "Bake until the tops just start to crack. Julie says 10 to 15 minutes.", "timerSec": 12 * 60, "timerLabel": "12 minutes", "grownup": ["oven"]},
        {"text": "Let them cool before you move them. They are tender when hot.", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
    unquantified=["Optional flaky sea salt on top. Left out of the count."],
))

recipes.append(R(
    "liv-pb-oat-bars",
    "No-bake peanut butter oat bars",
    "Bars",
    "A pan of oat bars with a chocolate top. Olivia printed the gram weights.",
    24, "1 bar", 20,
    "Liv's Little Muffins",
    "https://livslittlemuffins.com/no-bake-peanut-butter-oat-bars/",
    "Olivia Daly",
    [
        line("pb-salted", "3 cups (660 g) peanut butter", 660, "Olivia printed 660 g for 3 cups. Her weight is used, not the USDA cup."),
        line("honey", "1 cup (320 g) honey", 320, "Olivia printed 320 g."),
        line("salt", "1/2 tsp salt", TSP_SALT / 2, "USDA 1 tsp salt = 6 g."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("oats", "4 cups (480 g) quick oats", 480, "Olivia printed 480 g."),
        line("chips", "2 cups (320 g) semisweet chocolate chips", 320, "Olivia printed 320 g."),
        line("butter", "2 1/2 tbsp (35 g) butter", 35, "Olivia printed 35 g."),
    ],
    [
        {"text": "Line a 9 by 13 inch pan with parchment.", "grownup": []},
        {"text": "Ask a grown-up to warm the peanut butter, honey, and salt in a saucepan over medium-low heat until melted, then 2 minutes more.", "timerSec": 120, "timerLabel": "2 minutes", "grownup": ["stove"]},
        {"text": "Take the pan off the heat. Stir in the vanilla, then the oats. Spread the mix in the pan. Do not press hard.", "grownup": ["stove"]},
        {"text": "Ask a grown-up to melt the chocolate chips and butter, 30 seconds at a time.", "grownup": ["microwave"]},
        {"text": "Spread the chocolate over the oats.", "grownup": []},
        {"text": "Chill until the chocolate is set.", "timerSec": 2 * 60 * 60, "timerLabel": "2 hours", "grownup": []},
        {"text": "A grown-up cuts 24 bars.", "grownup": ["knife"]},
    ],
    heat="stove",
))

recipes.append(R(
    "wellplated-pb-bars",
    "Peanut butter oatmeal bars",
    "Bars",
    "One bowl, one pan, sixteen bars. Flour and butter stay in the cupboard.",
    16, "1 bar", 30,
    "Well Plated",
    "https://www.wellplated.com/peanut-butter-oatmeal-bars/",
    "Erin Clarke",
    [
        line("pb-salted", "1 cup creamy peanut butter", CUP_PB, "USDA 1 cup peanut butter = 258 g."),
        line("brown-sugar", "3/4 cup light brown sugar", 0.75 * CUP_BROWN, "USDA 1 packed cup brown sugar = 220 g. Packed is assumed."),
        line("baking-soda", "1/2 tsp baking soda", TSP_BS / 2, "USDA 1/2 tsp baking soda = 2.3 g."),
        line("salt", "1/8 tsp salt", TSP_SALT / 8, "USDA 1 tsp salt = 6 g."),
        line("egg", "1 large egg", LARGE_EGG, "USDA 1 large egg = 50 g.", count=1),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("chips", "1/2 cup semisweet chocolate chips", CUP_CHIPS / 2, "USDA 1 cup chips = 168 g."),
        line("oats", "1/3 cup rolled oats", CUP_OATS / 3, "USDA 1/3 cup oats = 27 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line an 8-inch square pan.", "grownup": ["oven"]},
        {"text": "Beat the peanut butter, brown sugar, baking soda, and salt until combined.", "grownup": []},
        {"text": "Mix in the egg and vanilla. Stir in the chocolate chips and oats by hand.", "grownup": []},
        {"text": "Press the dough into the pan.", "grownup": []},
        {"text": "Bake until the top is set and golden.", "timerSec": 22 * 60, "timerLabel": "22 minutes", "grownup": ["oven"]},
        {"text": "Cool completely. A grown-up cuts 16 bars.", "grownup": ["knife", "oven"]},
    ],
    swaps=[EGG_YOGURT],
))

recipes.append(R(
    "ambitious-cc-pancakes",
    "Cottage cheese banana pancakes",
    "Pancakes",
    "Blender pancakes for one hungry kid. Oats, banana, egg, and cottage cheese.",
    1, "the whole batch (3 to 4 pancakes)", 15,
    "Ambitious Kitchen",
    "https://www.ambitiouskitchen.com/cottage-cheese-banana-oatmeal-protein-pancakes/",
    "Monique Volz",
    [
        line("oats", "1/2 cup (48 g) rolled oats", 48, "Monique printed 48 g."),
        line("banana", "1/2 medium banana", MEDIUM_BANANA / 2, "USDA 1 medium banana = 118 g."),
        line("vanilla", "1/2 tsp vanilla", TSP_VANILLA / 2, "USDA 1 tsp vanilla = 4.2 g."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("cinnamon", "1/2 tsp cinnamon", TSP_CINN / 2, "USDA 1 tsp cinnamon = 2.6 g."),
        line("egg", "1 egg", LARGE_EGG, "USDA 1 large egg = 50 g.", count=1),
        line("cottage-2", "1/4 cup (55 g) low-fat cottage cheese", 55, "Monique printed 55 g. Nutrients are 2% cottage cheese. A 1% record also exists."),
    ],
    [
        {"text": "Put the oats, banana, vanilla, baking powder, cinnamon, egg, and cottage cheese in a blender. Blend until smooth, about 30 seconds.", "grownup": []},
        {"text": "Ask a grown-up to heat a nonstick pan on medium-low and add a little spray.", "grownup": ["stove"]},
        {"text": "Pour the batter in 1/4-cup puddles.", "grownup": ["stove"]},
        {"text": "Cook until bubbles show on top. A grown-up flips them and cooks the other side.", "grownup": ["stove"]},
        {"text": "Repeat with the rest of the batter. You should get 3 or 4 pancakes.", "grownup": ["stove"]},
    ],
    swaps=[EGG_YOGURT],
    unquantified=["Optional berries, chocolate chips, or peanut butter on top. Left out of the count."],
    heat="stove",
))

recipes.append(R(
    "ambitious-banana-bread",
    "Greek yogurt banana bread",
    "Bread",
    "One loaf, twelve slices, with yogurt and maple syrup instead of a lot of sugar.",
    12, "1 slice", 70,
    "Ambitious Kitchen",
    "https://www.ambitiouskitchen.com/my-favorite-healthy-banana-bread-recipe/",
    "Monique Volz",
    [
        line("banana", "1 1/3 cups mashed banana", CUP_MASHED_BANANA * 4 / 3, "Monique says 3 large bananas, about 1 1/3 cups mashed. USDA 1 cup mashed = 225 g, so 1 1/3 cups = 300 g. Three USDA large bananas would be heavier. The cup she measured is used."),
        line("egg", "2 eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("maple", "1/3 cup (104 g) maple syrup", 104, "Monique printed 104 g."),
        line("greek-whole", "1/2 cup (113 g) plain Greek yogurt", 113, "Monique printed 113 g and allows whole-milk or 2%. Whole-milk plain Greek yogurt is counted."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("soft-wheat", "1 3/4 cups (198 g) whole wheat pastry flour", 198, "Monique printed 198 g. Nutrients are soft whole-wheat flour, the closest SR Legacy flour to pastry flour."),
        line("baking-soda", "1 tsp baking soda", TSP_BS, "USDA 1 tsp baking soda = 4.6 g."),
        line("cinnamon", "1/2 tsp cinnamon", TSP_CINN / 2, "USDA 1 tsp cinnamon = 2.6 g."),
        line("salt", "1/4 tsp salt", TSP_SALT / 4, "USDA 1 tsp salt = 6 g."),
        line("butter", "6 tbsp (85 g) melted butter", 85, "Monique printed 85 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a loaf pan.", "grownup": ["oven"]},
        {"text": "Stir the mashed banana, eggs, maple syrup, yogurt, and vanilla.", "grownup": []},
        {"text": "Whisk the flour, baking soda, cinnamon, and salt. Stir them into the wet mix just until combined.", "grownup": []},
        {"text": "Stir in the melted butter. It should be cool enough to touch.", "grownup": ["stove"]},
        {"text": "Pour the batter into the pan.", "grownup": []},
        {"text": "Bake about 50 to 60 minutes, until a toothpick comes out clean. If the top gets dark, a grown-up can tent it with foil.", "timerSec": 55 * 60, "timerLabel": "55 minutes", "grownup": ["oven"]},
        {"text": "Cool before a grown-up slices 12 pieces.", "grownup": ["knife", "oven"]},
    ],
    swaps=[
        EGG_YOGURT,
        swap("butter-to-olive", "butter", "Monique says olive oil can replace the butter. Counted as 6 tablespoons (81 g).", "Ambitious Kitchen ingredient note.", author=True, adds=[{"foodId": "olive-oil", "grams": round(6 * TBSP_OLIVE, 2)}]),
        swap("butter-to-coconut-oil", "butter", "Monique says melted coconut oil can replace the butter. Counted as 6 tablespoons (81.6 g).", "Ambitious Kitchen ingredient note.", author=True, adds=[{"foodId": "coconut-oil", "grams": round(6 * TBSP_COCONUT_OIL, 2)}]),
    ],
    unquantified=["Optional 1/2 cup walnuts and optional chocolate chips. Left out of the count. An optional banana on top is also left out."],
))

recipes.append(R(
    "ambitious-pb-cookies",
    "Flourless peanut butter chocolate cookies",
    "Cookies",
    "Six ingredients, no flour. The batch makes about 24 cookies.",
    24, "1 cookie", 15,
    "Ambitious Kitchen",
    "https://www.ambitiouskitchen.com/6-ingredient-flourless-peanut-butter-chocolate-chunk-cookies/",
    "Monique Volz",
    [
        line("pb-unsalted", "1 1/2 cups natural creamy peanut butter", 1.5 * CUP_PB, "USDA 1 cup peanut butter = 258 g. She says all-natural, so the no-salt record is used."),
        line("honey", "1/2 cup honey", CUP_HONEY / 2, "USDA 1 cup honey = 339 g."),
        line("vanilla", "2 tsp vanilla", 2 * TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("egg", "2 eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("baking-soda", "1/2 tsp baking soda", TSP_BS / 2, "USDA 1/2 tsp baking soda = 2.3 g."),
        line("chips", "3.5 oz chocolate bar", 3.5 * 28.35, "3.5 ounces using the USDA ounce of 28.35 g. Counted as semisweet chocolate. Monique says any favorite bar."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F.", "grownup": ["oven"]},
        {"text": "Stir the peanut butter, honey, vanilla, eggs, and baking soda until smooth.", "grownup": []},
        {"text": "A grown-up chops the chocolate. Fold it in.", "grownup": ["knife"]},
        {"text": "Roll 2-inch balls. Set them apart and barely flatten the tops.", "grownup": []},
        {"text": "Bake until the edges just turn golden. Monique says 8 to 10 minutes. They look a little underdone, and that is right.", "timerSec": 9 * 60, "timerLabel": "9 minutes", "grownup": ["oven"]},
        {"text": "Cool on the sheet for 5 minutes, then move them to a rack.", "timerSec": 5 * 60, "timerLabel": "5 minutes", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
))

recipes.append(R(
    "sally-pb-oat-cookies",
    "Flourless peanut butter oatmeal cookies",
    "Cookies",
    "Sally's chewy cookies. She printed gram weights, and the dough needs a chill.",
    14, "1 cookie", 60,
    "Sally's Baking Addiction",
    "https://sallysbakingaddiction.com/flourless-peanut-butter-oatmeal-cookies/",
    "Sally McKenney",
    [
        line("oats", "1 cup (85 g) rolled oats", 85, "Sally printed 85 g."),
        line("baking-soda", "1 tsp baking soda", TSP_BS, "USDA 1 tsp baking soda = 4.6 g."),
        line("cinnamon", "1/4 tsp cinnamon", TSP_CINN / 4, "USDA 1 tsp cinnamon = 2.6 g."),
        line("salt", "1/8 tsp salt", TSP_SALT / 8, "USDA 1 tsp salt = 6 g."),
        line("egg", "2 large eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("pb-unsalted", "1 cup (250 g) natural peanut butter", 250, "Sally printed 250 g. Natural peanut butter uses the no-salt record."),
        line("brown-sugar", "2/3 cup (133 g) packed brown sugar", 133, "Sally printed 133 g."),
        line("vanilla", "2 tsp vanilla", 2 * TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("chips", "2/3 cup (120 g) semisweet chocolate chips", 120, "Sally printed 120 g."),
    ],
    [
        {"text": "Whisk the oats, baking soda, cinnamon, and salt.", "grownup": []},
        {"text": "In another bowl, whisk the eggs. Stir in the peanut butter, brown sugar, and vanilla. Then stir in the dry mix. Fold in the chips.", "grownup": []},
        {"text": "Cover the dough and chill it.", "timerSec": 30 * 60, "timerLabel": "30 minutes", "grownup": []},
        {"text": "Ask a grown-up to heat the oven to 350°F. Line baking sheets.", "grownup": ["oven"]},
        {"text": "Scoop about 1 1/2 tablespoons (30 g) of dough for each cookie. Flatten the tops a little.", "grownup": []},
        {"text": "Bake until the edges are set and the centers still look soft. Sally says 12 to 14 minutes.", "timerSec": 13 * 60, "timerLabel": "13 minutes", "grownup": ["oven"]},
        {"text": "Cool 10 minutes on the sheet, then move to a rack.", "timerSec": 10 * 60, "timerLabel": "10 minutes", "grownup": ["oven"]},
    ],
    swaps=[
        EGG_YOGURT,
        swap("pb-to-almond", "peanut-butter", "Sally says the same amount of almond butter works.", "Sally's Baking Addiction FAQ.", same_grams=True, author=True, adds=[{"foodId": "almond-butter", "gramsEach": None}]),
        swap("pb-to-sun", "peanut-butter", "Sally says the same amount of sunflower seed butter works. The inside may turn green. That is a science trick, and it is safe.", "Sally's Baking Addiction FAQ.", same_grams=True, author=True, adds=[{"foodId": "sunflower-butter", "gramsEach": None}]),
    ],
))

recipes.append(R(
    "mason-protein-bites",
    "No-bake protein bites",
    "Bites",
    "Eight little bites. Mason printed a gram weight for every ingredient.",
    8, "1 bite", 10,
    "Kinda Healthy Recipes",
    "https://masonfit.com/no-bake-oatmeal-peanut-butter-protein-bites/",
    "Mason Woodruff",
    [
        line("oats", "3/4 cup (60 g) rolled oats", 60, "Mason printed 60 g."),
        line("whey", "2 scoops (62 g) vanilla protein powder", 62, "Mason printed 62 g of a whey-and-casein powder. Nutrients are whey-based protein powder, the closest USDA record."),
        line("pb-flour", "1/4 cup (26 g) powdered peanut butter", 26, "Mason printed 26 g. Nutrients are defatted peanut flour."),
        line("banana", "1 medium banana (100 g peeled)", 100, "Mason printed 100 g peeled."),
        line("honey", "1/2 tbsp (11 g) honey", 11, "Mason printed 11 g."),
        line("chips", "2 tbsp (28 g) mini chocolate chips", 28, "Mason printed 28 g."),
    ],
    [
        {"text": "Stir the oats, protein powder, and powdered peanut butter.", "grownup": []},
        {"text": "Mash the banana and add it. Stir, then add the honey and chocolate chips. Mix until it holds together.", "grownup": []},
        {"text": "Divide into 8 pieces and roll them smooth.", "grownup": []},
        {"text": "Chill, then eat.", "grownup": []},
    ],
    swaps=[
        swap("pb2-to-pb", "powdered-peanut", "Mason says regular peanut butter can replace the powdered peanut butter. Counted as 1/4 cup (64.5 g), the same measuring cup, because powdered peanut butter is much lighter.", "Kinda Healthy Recipes variations.", author=True, adds=[{"foodId": "pb-unsalted", "grams": round(CUP_PB / 4, 2)}]),
    ],
    heat="none",
))

recipes.append(R(
    "food-network-pb-muffins",
    "Peanut butter banana protein muffins",
    "Muffins",
    "Twelve muffins with yogurt, protein powder, and a peanut-butter center.",
    12, "1 muffin", 45,
    "Food Network Kitchen",
    "https://www.foodnetwork.com/recipes/food-network-kitchen/peanut-butter-banana-protein-muffins-18796114",
    "Food Network Kitchen",
    [
        line("flour", "1 3/4 cups all-purpose flour", 1.75 * CUP_AP, "USDA 1 cup all-purpose flour = 125 g. Food Network spoons and levels the cup, which matches this portion better than a scooped cup."),
        line("whey", "1/2 cup peanut-butter chocolate whey protein powder", CUP_PROTEIN / 2, "1/2 cup = 48 g from the whey cup fraction. The flavor is not a separate USDA food. Nutrients are unflavored whey-based powder."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("cinnamon", "1 tsp cinnamon", TSP_CINN, "USDA 1 tsp cinnamon = 2.6 g."),
        line("baking-soda", "1/2 tsp baking soda", TSP_BS / 2, "USDA 1/2 tsp baking soda = 2.3 g."),
        line("salt", "1/2 tsp kosher salt", TSP_SALT / 2, "Kosher salt weighs less than table salt. USDA table salt is used. It adds no protein, fiber, calories, or sugar."),
        line("brown-sugar", "1/2 cup packed light brown sugar", CUP_BROWN / 2, "USDA 1 packed cup = 220 g."),
        line("greek-whole", "1/2 cup plain whole-milk Greek yogurt", CUP_GREEK / 2, "1/2 cup = 113 g from Monique Volz's printed Greek yogurt weight, which matches this recipe's whole-milk style."),
        line("coconut-oil", "6 tbsp coconut oil", 6 * TBSP_COCONUT_OIL, "USDA 1 tbsp coconut oil = 13.6 g."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("egg", "2 large eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("banana", "1 3/4 cups mashed banana", 1.75 * CUP_MASHED_BANANA, "USDA 1 cup mashed banana = 225 g. Food Network says that is about 4 large bananas."),
        line("pb-unsalted", "1/2 cup natural peanut butter", CUP_PB / 2, "USDA 1 cup peanut butter = 258 g. This is the center of the muffins: 2 tsp in each of 12 muffins equals 1/2 cup."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a 12-cup muffin pan.", "grownup": ["oven"]},
        {"text": "Whisk the flour, protein powder, baking powder, cinnamon, baking soda, and salt.", "grownup": []},
        {"text": "Whisk the brown sugar, yogurt, coconut oil, vanilla, and eggs. Stir in the mashed banana, then the flour mix, just until combined.", "grownup": []},
        {"text": "Fill each liner halfway. Add 2 teaspoons of peanut butter. Cover with the rest of the batter.", "grownup": []},
        {"text": "Bake until a toothpick comes out clean. The page says 30 to 35 minutes.", "timerSec": 32 * 60, "timerLabel": "32 minutes", "grownup": ["oven"]},
        {"text": "Cool 5 minutes in the pan, then move to a rack.", "timerSec": 5 * 60, "timerLabel": "5 minutes", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
))

recipes.append(R(
    "cookieandkate-muffins",
    "Whole-wheat banana muffins",
    "Muffins",
    "Eleven maple-sweetened muffins. Oats are optional in Kathryne's card, so they are not in the base count.",
    11, "1 muffin", 35,
    "Cookie and Kate",
    "https://cookieandkate.com/healthy-banana-muffins-recipe/",
    "Kathryne Taylor",
    [
        line("coconut-oil", "1/3 cup melted coconut oil", 218 / 3, "USDA 1 cup coconut oil = 218 g. Kathryne also allows olive oil."),
        line("maple", "1/2 cup maple syrup", CUP_MAPLE / 2, "USDA 1 cup maple syrup = 315 g. Honey is her other choice."),
        line("egg", "2 eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("banana", "1 cup mashed banana", CUP_MASHED_BANANA, "USDA 1 cup mashed banana = 225 g. She says that is about 3 bananas."),
        line("almond-milk", "1/4 cup almond milk", CUP_ALMOND_MILK / 4, "She says milk of choice and used almond milk. USDA 1 cup unsweetened almond milk = 262 g."),
        line("baking-soda", "1 tsp baking soda", TSP_BS, "USDA 1 tsp baking soda = 4.6 g."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("salt", "1/2 tsp salt", TSP_SALT / 2, "USDA 1 tsp salt = 6 g."),
        line("cinnamon", "1/2 tsp cinnamon", TSP_CINN / 2, "USDA 1 tsp cinnamon = 2.6 g."),
        line("whole-wheat", "1 3/4 cups whole-wheat flour", 1.75 * CUP_WW, "She allows white whole-wheat or regular whole-wheat. USDA 1 cup whole-grain flour = 120 g."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 325°F. Grease a muffin tin if it is not nonstick.", "grownup": ["oven"]},
        {"text": "Whisk the melted coconut oil and maple syrup. Add the eggs and whisk again. Stir in the banana and milk, then the baking soda, vanilla, salt, and cinnamon.", "grownup": []},
        {"text": "Add the flour. Stir just until combined. Kathryne's oats are optional, so add 1/3 cup only if you want them.", "grownup": []},
        {"text": "Fill 11 cups about 2/3 full. You can sprinkle a little oats and sugar on top.", "grownup": []},
        {"text": "Bake until a toothpick comes out clean. She says 22 to 25 minutes.", "timerSec": 23 * 60, "timerLabel": "23 minutes", "grownup": ["oven"]},
        {"text": "Cool in the pan. A grown-up may need a butter knife to loosen the edges.", "grownup": ["knife", "oven"]},
    ],
    swaps=[
        EGG_YOGURT,
        swap("oil-to-olive", "coconut-oil", "Kathryne says olive oil can replace the coconut oil, same 1/3 cup.", "Cookie and Kate ingredient line.", author=True, adds=[{"foodId": "olive-oil", "grams": round(216 / 3, 2)}]),
        swap("maple-to-honey-kate", "maple", "Kathryne says honey can replace the maple syrup.", "Cookie and Kate ingredient line.", author=True, adds=[{"foodId": "honey", "grams": round(CUP_HONEY / 2, 2)}]),
        swap("almond-milk-to-milk-kate", "almond-milk", "She says any milk works. This swap uses 1/4 cup of 2% milk (61 g).", "Cookie and Kate ingredient note.", author=True, adds=[{"foodId": "milk-2", "grams": round(CUP_MILK_2 / 4, 2)}]),
    ],
    unquantified=["Optional 1/3 cup oats in the batter, about 1 tablespoon oats on top, and about 1 teaspoon sugar on top. Left out of the base count."],
))

recipes.append(R(
    "fgf-yogurt-bark",
    "Frozen yogurt bark",
    "Bark",
    "Yogurt spread thin, topped with berries and granola, then frozen.",
    12, "1 piece", 10,
    "Feel Good Foodie",
    "https://feelgoodfoodie.net/recipe/frozen-yogurt-bark/",
    "Yumna Jawad",
    [
        line("yogurt-vanilla", "2 cups whole-milk vanilla yogurt", 2 * CUP_YOGURT, "SR Legacy has no whole-milk vanilla yogurt. Low-fat vanilla yogurt is used (1 cup = 245 g). Whole-milk yogurt would have more calories and a little less protein per 100 g."),
        line("strawberries", "1/2 cup diced strawberries", CUP_STRAW_SLICED / 2, "Diced is not a USDA portion. Half of the sliced cup (166 g) is used."),
        line("blueberries", "1/4 cup blueberries", CUP_BERRIES / 4, "USDA 1 cup blueberries = 148 g."),
        line("granola", "1/4 cup granola", CUP_GRANOLA / 4, "Brand is not named. USDA homemade granola, 1 cup = 122 g."),
    ],
    [
        {"text": "Line a small rimmed baking sheet with parchment paper.", "grownup": []},
        {"text": "Pour the yogurt on and spread it to the edges.", "grownup": []},
        {"text": "Scatter the strawberries, blueberries, and granola on top.", "grownup": []},
        {"text": "Freeze until the yogurt is firm.", "timerSec": 3 * 60 * 60, "timerLabel": "3 hours", "grownup": []},
        {"text": "A grown-up cuts about 12 pieces. Eat them cold. Keep leftovers in the freezer.", "grownup": ["knife"]},
    ],
    heat="none",
))

recipes.append(R(
    "bird-cc-pancakes",
    "Cottage cheese pancakes",
    "Pancakes",
    "Eight small pancakes, two plates. Cottage cheese goes in the blender.",
    2, "4 pancakes", 20,
    "Eating Bird Food",
    "https://www.eatingbirdfood.com/cottage-cheese-pancakes/",
    "Brittany Mullins",
    [
        line("flour", "1/2 cup all-purpose flour", CUP_AP / 2, "USDA 1 cup all-purpose flour = 125 g."),
        line("baking-powder", "1 tsp baking powder", TSP_BP, "USDA 1 tsp baking powder = 4.6 g."),
        line("cinnamon", "1/4 tsp cinnamon", TSP_CINN / 4, "USDA 1 tsp cinnamon = 2.6 g."),
        line("cottage-4", "1 cup 4% cottage cheese", CUP_COTTAGE_4, "Brittany uses Good Culture 4%. USDA small-curd cup = 225 g."),
        line("egg", "2 large eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
        line("maple", "1 tbsp maple syrup", TBSP_MAPLE, "USDA 1 tbsp maple syrup = 20 g. Extra syrup on top is not counted."),
        line("vanilla", "1 tsp vanilla", TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
    ],
    [
        {"text": "Stir the flour, baking powder, and cinnamon in a bowl.", "grownup": []},
        {"text": "Blend the cottage cheese, eggs, maple syrup, and vanilla until smooth. No blender? Whisk them instead.", "grownup": []},
        {"text": "Stir the wet mix into the dry mix. If it is too thick, add 1 tablespoon of milk.", "grownup": []},
        {"text": "Ask a grown-up to heat a pan on medium-low and spray it.", "grownup": ["stove"]},
        {"text": "Pour 1/4-cup circles. Cook until bubbles form and the edges look set.", "grownup": ["stove"]},
        {"text": "A grown-up flips them and cooks 2 to 3 more minutes. The batch makes 8 pancakes, 4 for each plate.", "timerSec": 150, "timerLabel": "2 to 3 minutes", "grownup": ["stove"]},
    ],
    swaps=[EGG_YOGURT],
    unquantified=["Optional 1 tablespoon almond milk if the batter is too thick. Maple syrup and berries on top are not in the count."],
    heat="stove",
))

recipes.append(R(
    "rice-paper-bagels",
    "Rice paper breakfast bagels",
    "Bagels",
    "The crispy rice-paper bagel. Three bagels, eggs in the middle and in the wash.",
    3, "1 bagel", 30,
    "The Chef Out West",
    "https://thechefoutwest.com/bacon-egg-cheese-rice-paper-bagels/",
    "The Chef Out West",
    [
        line("rice-paper", "3 rice paper sheets", None, "No USDA FoodData Central record for rice paper wrappers, so the sheets are not in the numbers."),
        line("egg", "6 large eggs", 6 * LARGE_EGG, "4 eggs for the filling and 2 for the wash. USDA 1 large egg = 50 g.", count=6),
        line("bacon", "3 strips cooked bacon", 3 * BACON_SLICE, "USDA 1 baked slice = 8.1 g. A grocery strip may be heavier."),
        line("mozzarella", "3/4 cup shredded mozzarella", 0.75 * CUP_MOZZ, "USDA 1 cup shredded whole-milk mozzarella = 112 g."),
    ],
    [
        {"text": "Ask a grown-up to cook 4 eggs on medium-low until they are soft and just set. Chop the cooked bacon.", "grownup": ["stove", "knife"]},
        {"text": "Whisk the other 2 eggs in a wide shallow plate.", "grownup": []},
        {"text": "Dip one rice paper sheet in the egg wash until it is bendy, not soggy. Lay it on a lightly oiled board.", "grownup": []},
        {"text": "Spread on some scrambled egg, chopped bacon, and shredded cheese.", "grownup": []},
        {"text": "Roll it into a tight log. Bend the log into a ring and tuck one end into the other. Repeat for 3 bagels.", "grownup": []},
        {"text": "Brush the tops with leftover egg wash. Ask a grown-up to bake or air-fry at 400°F until golden and crisp.", "timerSec": 13 * 60, "timerLabel": "13 minutes", "grownup": ["oven"]},
    ],
    unquantified=["Everything bagel seasoning and a light brush of oil. Amounts are not given, so they are not in the numbers. The rice paper sheets are listed but not counted. See the kitchen math."],
))

recipes.append(R(
    "lifecurrents-cookie-bark",
    "Peanut butter cookie dough bark",
    "Bark",
    "Cottage cheese dough, almond flour, and a chocolate lid. Freeze, then snap.",
    20, "1 piece", 20,
    "Life Currents",
    "https://lifecurrentsblog.com/cottage-cheese-cookie-dough-bark/",
    "Debi",
    [
        line("cottage-4", "1 cup cottage cheese", CUP_COTTAGE_4, "Fat level is not named. Creamed cottage cheese, USDA small-curd cup = 225 g."),
        line("pb-unsalted", "2 tbsp natural peanut butter", 2 * TBSP_PB, "USDA 1 tbsp peanut butter = 16 g."),
        line("maple", "1 tbsp maple syrup", TBSP_MAPLE, "USDA 1 tbsp maple syrup = 20 g."),
        line("vanilla", "2 tsp vanilla", 2 * TSP_VANILLA, "USDA 1 tsp vanilla = 4.2 g."),
        line("almond-flour", "1 cup almond flour", CUP_ALMOND_FLOUR, "1 cup ground almonds = 95 g (FDC 170567). Nutrients are blanched almonds (FDC 170568)."),
        line("whey", "1/4 cup vanilla protein powder", CUP_PROTEIN / 4, "1/4 cup = 24 g from the whey cup fraction. Nutrients are unflavored whey-based powder."),
        line("chips", "1/3 cup mini chocolate chips", CUP_MINI / 3, "USDA 1 cup mini chips = 173 g."),
        line("chips", "1 cup chocolate chips for the topping", CUP_CHIPS, "USDA 1 cup chips = 168 g."),
        line("coconut-oil", "2 tsp coconut oil", 2 * 4.5, "USDA 1 tsp coconut oil = 4.5 g."),
    ],
    [
        {"text": "Blend the cottage cheese, peanut butter, maple syrup, and vanilla until smooth.", "grownup": []},
        {"text": "Stir in the almond flour and protein powder, then the mini chips.", "grownup": []},
        {"text": "Spread the dough on parchment. Wet the spatula if it sticks.", "grownup": []},
        {"text": "Ask a grown-up to melt the topping chips with the coconut oil, 30 seconds at a time.", "grownup": ["microwave"]},
        {"text": "Spread the chocolate over the dough.", "grownup": []},
        {"text": "Freeze at least 2 hours, until hard.", "timerSec": 2 * 60 * 60, "timerLabel": "2 hours", "grownup": []},
        {"text": "Break into about 20 pieces. Keep them in the freezer.", "grownup": []},
    ],
    heat="microwave",
))


recipes.append(R(
    "bobs-banana-oat-cookies",
    "2-ingredient banana oat cookies",
    "Cookies",
    "One banana and a cup of oats. No peanut butter, no sugar jar.",
    8, "1 cookie", 20,
    "Bob's Red Mill",
    "https://www.bobsredmill.com/recipes/how-to-make/2-ingredient-banana-oat-cookies",
    "Bob's Red Mill",
    [
        line("oats", "1 cup quick-cooking rolled oats", CUP_OATS, "USDA 1 cup dry oats = 81 g. Bob's uses quick-cooking rolled oats. The cup weight is the same rolled-oat cup."),
        line("banana", "1 large overripe banana (about 1/2 cup mashed)", LARGE_BANANA, "Bob's says 1 large banana, about 1/2 cup mashed. USDA 1 large banana = 136 g. A USDA 1/2 cup mashed banana is 112.5 g. The large-banana weight is counted."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a baking sheet.", "grownup": ["oven"]},
        {"text": "Mash the banana until it looks smooth and wet. Stir in the oats.", "grownup": []},
        {"text": "Divide the dough into 8 balls. Flatten each one. They will not spread in the oven.", "grownup": []},
        {"text": "Bake until the bottoms turn light brown and lift off the sheet.", "timerSec": 15 * 60, "timerLabel": "15 minutes", "grownup": ["oven"]},
        {"text": "Cool them all the way before eating. A grown-up takes the pan out.", "grownup": ["oven"]},
    ],
    unquantified=["Optional chocolate chips, nuts, dried fruit, vanilla, salt, or up to 2 tbsp maple syrup. Left out of the count."],
))

recipes.append(R(
    "kirbie-pb-cookies",
    "3-ingredient peanut butter cookies",
    "Cookies",
    "Peanut butter, one egg, and maple syrup. No flour.",
    21, "1 cookie", 20,
    "Kirbie's Cravings",
    "https://kirbiecravings.com/3-ingredient-healthy-peanut-butter-cookies/",
    "Jennifer Lee",
    [
        line("pb-unsalted", "1 cup (256 g) natural peanut butter", 256, "Jennifer printed 256 g. Natural peanut butter, no added oil."),
        line("egg", "1 large egg", LARGE_EGG, "USDA 1 large egg = 50 g."),
        line("maple", "1/4 cup pure maple syrup", CUP_MAPLE / 4, "USDA 1 cup maple syrup = 315 g, so 1/4 cup is 78.75 g. Jennifer also writes 59 ml."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line two cookie sheets.", "grownup": ["oven"]},
        {"text": "Stir the peanut butter, whisked egg, and maple syrup until the dough gets thick.", "grownup": []},
        {"text": "Scoop tablespoon balls. Flatten them a little. A fork can press a criss-cross on top.", "grownup": []},
        {"text": "Bake until the tops look dry and a little cracked.", "timerSec": 10 * 60, "timerLabel": "10 minutes", "grownup": ["oven"]},
        {"text": "Leave the cookies on the sheet until they are fully cool. A grown-up moves the pan.", "grownup": ["oven"]},
    ],
    swaps=[EGG_YOGURT],
))

recipes.append(R(
    "real-meal-deal-brownies",
    "Flourless banana peanut butter brownies",
    "Brownies",
    "Bananas, peanut butter, and cocoa. No flour and no added sugar.",
    9, "1 brownie", 30,
    "The Real Meal Deal",
    "https://www.therealmealdeal.com/peanut-butter-banana-brownie-3-ingredients/",
    "Claire Carter",
    [
        line("banana", "3 ripe bananas (400 g, the low end of Claire's 400–500 g)", 400, "Claire prints 400–500 g for 3 bananas. The low end, 400 g, is counted."),
        line("pb-unsalted", "120 g peanut butter", 120, "Claire printed 120 g and asks for peanut butter made from peanuts."),
        line("cocoa", "50 g cocoa powder", 50, "Claire printed 50 g unsweetened cocoa powder."),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 360°F. Line an 8-inch square pan with parchment.", "grownup": ["oven"]},
        {"text": "Mash the bananas. Stir in the peanut butter and cocoa until the batter is smooth.", "grownup": []},
        {"text": "Spread it in the pan.", "grownup": []},
        {"text": "Bake on the middle shelf until the top is set.", "timerSec": 25 * 60, "timerLabel": "25 minutes", "grownup": ["oven"]},
        {"text": "Cool all the way, then slice into 9 squares. A grown-up uses the knife.", "grownup": ["knife", "oven"]},
    ],
    swaps=[
        swap("pb-to-almond", "peanut-butter", "Claire says almond butter works the same way.", "The Real Meal Deal, substituting other butters.", adds=[{"foodId": "almond-butter"}], same_grams=True, author=True),
        swap("pb-to-sun", "peanut-butter", "Claire says sunflower seed butter works for a nut-free pan.", "The Real Meal Deal, substituting other butters.", adds=[{"foodId": "sunflower-butter"}], same_grams=True, author=True),
    ],
    unquantified=["Optional chocolate chips on top. Left out of the count. Claire's card shows 9 next to the calorie line, and the method says to slice into squares, so this count uses 9 brownies."],
))

recipes.append(R(
    "protein-chef-flatbread",
    "Two-ingredient cottage cheese flatbread",
    "Flatbread",
    "Just cottage cheese and two eggs. Blend, spread, bake.",
    1, "1 flatbread", 35,
    "The Protein Chef",
    "https://theproteinchef.co/cottage-cheese-flatbread-recipe/",
    "The Protein Chef",
    [
        line("cottage-4", "1 cup cottage cheese", CUP_COTTAGE_4, "The Protein Chef says full, reduced, or fat-free all work. USDA small-curd creamed cottage cheese, 1 cup = 225 g."),
        line("egg", "2 large eggs", 2 * LARGE_EGG, "USDA 1 large egg = 50 g.", count=2),
    ],
    [
        {"text": "Ask a grown-up to heat the oven to 350°F. Line a baking sheet with parchment.", "grownup": ["oven"]},
        {"text": "Blend the cottage cheese and eggs until smooth. A grown-up runs the blender.", "grownup": []},
        {"text": "Pour the mix on the sheet and spread it thin.", "grownup": []},
        {"text": "Bake until the edges brown. A thin one is ready sooner than a thick one.", "timerSec": 35 * 60, "timerLabel": "35 minutes", "grownup": ["oven"]},
        {"text": "Cool it all the way so it firms up. Then fold it or cut it.", "grownup": ["knife"]},
    ],
    unquantified=["Optional 3/4 tsp garlic powder and 1 tsp Italian seasoning. Left out of the count."],
))

recipes.append(R(
    "ada-power-oats-mug",
    "Power oats yogurt mug muffin",
    "Mug cakes",
    "A one-mug cake from the American Diabetes Association. Yogurt, an egg, and a little oat flour.",
    1, "1 mug muffin", 7,
    "American Diabetes Association",
    "https://diabetesfoodhub.org/recipes/power-oats-mug-muffin",
    "American Diabetes Association",
    [
        line("greek-nonfat", "3 tbsp plain nonfat Greek yogurt", 3 * CUP_GREEK / 16, "The page says 3 tbsp (44 ml) plain nonfat Greek yogurt. USDA has no Greek tablespoon. 3/16 of the 226 g cup is 42.38 g."),
        line("egg", "1 egg", LARGE_EGG, "USDA 1 large egg = 50 g. The page says 1 whole egg."),
        line("vanilla", "1/2 tsp vanilla", TSP_VANILLA / 2, "USDA 1 tsp vanilla = 4.2 g."),
        line("oats", "2 tbsp oat flour", 2 * CUP_OATS / 16, "The page says blend regular oats if you have no oat flour. USDA rolled-oat tablespoon weight is used, 81 g per cup."),
        line("baking-powder", "1/2 tsp baking powder", TSP_BP / 2, "USDA 1 tsp baking powder = 4.6 g."),
        line("cinnamon", "1/4 tsp cinnamon", TSP_CINN / 4, "USDA 1 tsp cinnamon = 2.6 g."),
        line("blueberries", "2 tbsp blueberries", 2 * CUP_BERRIES / 16, "USDA 1 cup blueberries = 148 g."),
    ],
    [
        {"text": "In a mug, whisk the yogurt, egg, and vanilla.", "grownup": []},
        {"text": "Stir in the oat flour, baking powder, cinnamon, and blueberries until the batter is smooth.", "grownup": []},
        {"text": "Ask a grown-up to microwave it until the muffin is puffed and set.", "timerSec": 90, "timerLabel": "90 seconds", "grownup": ["microwave"]},
        {"text": "The mug is hot. Let it sit a moment, then eat it from the mug.", "grownup": ["microwave"]},
    ],
    swaps=[EGG_YOGURT],
    heat="microwave",
))


def totals(recipe):
    acc = {"kcal": 0.0, "protein": 0.0, "fiber": 0.0, "sugar": 0.0}
    skipped = []
    for item in recipe["lines"]:
        if item["optional"] or item["grams"] is None:
            skipped.append(item["amount"])
            continue
        row = FOOD_BY_ID[item["foodId"]]
        per = row["per100g"]
        if not per:
            skipped.append(item["amount"])
            continue
        factor = item["grams"] / 100.0
        for key in acc:
            acc[key] += per[key] * factor
    servings = recipe["servings"]
    per_srv = {key: acc[key] / servings for key in acc}
    return acc, per_srv, skipped


def main():
    ids = [r["id"] for r in recipes]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate recipe ids")
    pantry_ids = {p["id"] for p in PANTRY}
    for food_row in FOODS:
        if food_row["pantryId"] not in pantry_ids:
            raise SystemExit(f"missing pantry {food_row['pantryId']}")
    for recipe in recipes:
        if recipe["servings"] < 1:
            raise SystemExit(recipe["id"])
        if not recipe["steps"]:
            raise SystemExit("no steps " + recipe["id"])
        for item in recipe["lines"]:
            if item["foodId"] not in FOOD_BY_ID:
                raise SystemExit(item["foodId"])
        for sw in recipe["swaps"]:
            for add in sw["adds"]:
                if add["foodId"] not in FOOD_BY_ID:
                    raise SystemExit(add["foodId"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "foods.json").write_text(json.dumps(FOODS, indent=2) + "\n")
    (OUT / "pantry.json").write_text(json.dumps(PANTRY, indent=2) + "\n")
    (OUT / "recipes.json").write_text(json.dumps(recipes, indent=2) + "\n")
    print(f"{len(recipes)} recipes")
    rows = []
    for recipe in recipes:
        batch, per, skipped = totals(recipe)
        rows.append((per["protein"], per["fiber"], per["kcal"], per["sugar"], recipe["title"], recipe["servings"], recipe["servingLabel"]))
    rows.sort(reverse=True)
    print(f"{'protein':>8} {'fiber':>7} {'kcal':>7} {'sugar':>7}  recipe")
    for protein, fiber, kcal, sugar, title, servings, label in rows:
        print(f"{protein:8.1f} {fiber:7.1f} {kcal:7.0f} {sugar:7.1f}  {title} ({label})")


if __name__ == "__main__":
    main()
