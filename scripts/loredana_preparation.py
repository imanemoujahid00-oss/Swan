"""Preparation helpers copied from Loredana's catalogue V2 notebook for local expansion.
No notebook cells with file writes or team decisions are executed.
"""

import html

import re

NB_ROUTINE_PRODUCT = 3

ROUTINE_STEPS = ['cleanser', 'moisturizer', 'sunscreen']

MIN_INGREDIENTS = 5

BLEMISH_REFERRAL_LEVEL = 4

LIGHT_SKIN_TYPES = ['oily', 'combination', 'normal', 'not_sure']

FRAGRANCE_ALLERGENS = ['linalool', 'limonene', 'citronellol', 'geraniol', 'citral', 'coumarin', 'eugenol', 'benzyl alcohol', 'benzyl benzoate', 'benzyl salicylate', 'hexyl cinnamal', 'farnesol', 'alpha-isomethyl ionone', 'hydroxycitronellal', 'cinnamal', 'amyl cinnamal', 'isoeugenol']

ESSENTIAL_OILS = ['lavandula', 'citrus', 'mentha', 'eucalyptus', 'rosmarinus', 'melaleuca', 'pelargonium', 'cymbopogon', 'cananga', 'santalum', 'pogostemon', 'juniperus', 'cinnamomum', 'jasminum']

ACNE_ACTIVES = ['salicylic acid', 'niacinamide', 'zinc pca', 'zinc gluconate', 'azelaic acid']

HEAVY_INGREDIENTS = ['petrolatum', 'paraffinum liquidum', 'paraffin', 'mineral oil', 'butter', 'cera', 'wax', 'lanolin', 'seed oil', 'kernel oil', 'fruit oil', 'nut oil']

GEL_INGREDIENTS = ['carbomer', 'sodium polyacrylate', 'acrylates/c10-30 alkyl acrylate crosspolymer', 'ammonium acryloyldimethyltaurate', 'xanthan gum', 'hydroxyethylcellulose']

WATER_LIKE = ['aqua', 'water', 'eau', 'aloe barbadensis leaf juice', 'hydrosol']

RICH_NAME_WORDS = ['riche', 'rich', 'baume', 'balm', 'cold cream', 'nourri', 'beurre', 'butter', 'nutri', 'intense']

LIGHT_NAME_WORDS = ['gel', 'fluide', 'fluid', 'light', 'légère', 'legere', 'matifiant', 'mattifying', 'sorbet', 'émulsion', 'emulsion', 'oil-free', 'water cream']

RICH_CLEANSER_WORDS = ['lait', 'milk', 'milch', 'crème', 'cream', 'creme', 'huile', 'oil', 'öl', 'baume', 'balm']

LIGHT_CLEANSER_WORDS = ['gel', 'jel', 'гель', 'foam', 'mousse', 'schaum', 'espuma', 'purif']

SKIN_BY_TEXTURE = {'rich': 'dry', 'medium': 'normal, combination, dry', 'light': 'oily, combination, normal'}

ALIASES = {'glycérine': 'glycerin', 'propylène glycol': 'propylene glycol', 'xantham gum': 'xanthan gum', 'purified water': 'aqua', 'acohol denat': 'alcohol denat.', 'water': 'aqua', 'eau': 'aqua', 'aqua (water)': 'aqua', 'aqua/water/eau': 'aqua', 'aqua / water': 'aqua', 'aqua / water / eau': 'aqua', 'glycerine': 'glycerin', 'fragrance': 'parfum', 'perfume': 'parfum', 'aroma': 'parfum', 'parfum (fragrance)': 'parfum', 'parfum/fragrance': 'parfum', 'shea butter': 'butyrospermum parkii butter', 'butyrospermum parkii': 'butyrospermum parkii butter', 'alcohol denat': 'alcohol denat.', 'flagrance': 'parfum'}

def has_word(text, words):
    """True if one of the words is in the text."""
    for word in words:
        if word in text:
            return True
    return False

def policy_rule(row):
    """The rule of the policy for one product. The first rule that matches wins."""
    name = str(row['product_name']).lower()
    inci = str(row['ingredients_text']).lower()
    first_ingredient = inci.split(',')[0].strip()
    if has_word(name, NOT_COSMETIC) or 'wc' in name.split() or first_ingredient == 'acetone' or has_word(inci, NAIL_INGREDIENTS):
        return 'C08'
    if ' ou ' in name:
        return 'to check by hand'
    if has_word(name, SCRUB):
        return 'C05'
    if has_word(name, NOT_DAILY):
        return 'C06'
    if ('tonique' in name or 'tonic' in name) and 'lait' not in name:
        return 'C09'
    if has_word(name, EYE_WORDS) and (not has_word(name, FACE_WORDS)):
        return 'C03'
    if has_word(name, WIPES):
        return 'C04'
    if has_word(name, SOAP) or 'bar' in name.split():
        return 'C07'
    if has_word(name, CLEANSER_WORDS):
        return 'C01'
    return 'to check by hand'

UV_FILTERS = ['octocrylene', 'butyl methoxydibenzoylmethane', 'avobenzone', 'titanium dioxide', 'zinc oxide', 'ethylhexyl methoxycinnamate', 'octyl methoxycinnamate', 'homosalate', 'ethylhexyl salicylate', 'octyl salicylate', 'bis-ethylhexyloxyphenol', 'bemotrizinol', 'ethylhexyl triazone', 'diethylamino hydroxybenzoyl', 'methylene bis-benzotriazolyl', 'drometrizole trisiloxane', 'terephthalylidene', 'phenylbenzimidazole', 'benzophenone-3', 'tris-biphenyl triazine', 'diethylhexyl butamido triazone', 'polysilicone-15', 'isoamyl p-methoxycinnamate', 'methoxypropylamino cyclohexenylidene', 'methylbenzylidene camphor']

SUN_WORDS = ['spf', 'fps', 'sun', 'solaire', 'solare', 'solcreme', 'güneş', 'uv', 'protect']

OTHER_AREA = ['lip', 'lèvre', 'levre', 'stick', 'bb cream', 'cc cream', 'cc krem', 'after sun', 'après-soleil', 'autobronz', 'self tan']

LOW_SPF = ['spf 6', 'spf 10', 'spf 15', 'spf 20', 'spf 25', 'spf6', 'spf10', 'spf15', 'spf20', 'spf25', 'fps 10', 'fps 15', 'fps 20', 'fps 25']

FACE_AND_BODY = ['body', 'corps', 'famille']

SEPARATORS = ['•', '·', '⚫', '|', ';', ' (and) ', '. ']

def split_ingredients(text):
    """Turn the ingredient text into a list of names."""
    text = html.unescape(str(text)).lower()
    text = text.replace('ingredients:', '').replace('ingrédients:', '')
    text = text.replace('1,2-hexanediol', '1-2-hexanediol')
    for separator in SEPARATORS:
        text = text.replace(separator, ',')
    if ',' not in text:
        text = text.replace(' - ', ',')
    names = []
    for piece in text.split(','):
        name = piece.strip().strip('."').strip()
        if name != '':
            names.append(name.replace('1-2-hexanediol', '1,2-hexanediol'))
    return names

def to_inci(name):
    """Clean one ingredient name and return its INCI name when we know it."""
    name = name.lower().replace('*', '').strip().strip('.').strip()
    if '[' in name and ']' in name:
        name = name.split('[')[0] + name.split(']')[-1]
        name = name.strip().strip('.').strip()
    if '(' in name and ')' in name:
        name = name.split('(')[0] + name.split(')')[-1]
    elif '(' in name:
        name = name.split('(')[0]
    name = name.replace(')', '')
    if name.endswith('%'):
        name = ' '.join(name.split()[:-1])
    name = ' '.join(name.split())
    name = ALIASES.get(name, name)
    if name not in inci_names and '/' in name:
        first = ALIASES.get(name.split('/')[0].strip(), name.split('/')[0].strip())
        if first in inci_names:
            name = first
    return name

def count_heavy(ingredients):
    """How many ingredients of the list are heavy (oil, butter, wax, petrolatum)?"""
    count = 0
    for ingredient in ingredients:
        if has_word(ingredient, HEAVY_INGREDIENTS):
            count = count + 1
    return count

def ingredient_points(inci_text):
    """Points from the first ingredients: + for a rich texture, - for a light one."""
    ingredients = str(inci_text).split(' | ')
    heavy_top5 = count_heavy(ingredients[:5])
    points = heavy_top5
    if count_heavy(ingredients[:2]) >= 1:
        points = points + 1
    if not has_word(ingredients[0], WATER_LIKE):
        points = points + 1
    if heavy_top5 == 0 and has_word(' '.join(ingredients[:8]), GEL_INGREDIENTS):
        points = points - 1
    if 'alcohol denat' in ' '.join(ingredients[:5]):
        points = points - 1
    return points

def find_texture(inci_text, name, role):
    """rich, medium or light: the product name first, then the first ingredients."""
    name = str(name).lower()
    if role == 'cleanser':
        if has_word(name, RICH_CLEANSER_WORDS):
            return 'rich'
        if has_word(name, LIGHT_CLEANSER_WORDS):
            return 'light'
        return 'medium'
    if has_word(name, RICH_NAME_WORDS):
        return 'rich'
    if has_word(name, LIGHT_NAME_WORDS) and 'gelée' not in name:
        return 'light'
    points = ingredient_points(inci_text)
    if points >= 2:
        return 'rich'
    if points <= -1:
        return 'light'
    return 'medium'

ANIMAL_INGREDIENTS = ['cera alba', 'beeswax', 'propolis', 'royal jelly', 'lanolin', 'collagen', 'elastin', 'keratin', 'silk', 'sericin', 'snail', 'lactis', 'casein', 'goat milk', 'donkey milk', 'carmine', 'ci 75470', 'guanine', 'ci 75170', 'shellac', 'tallow', 'chitosan', 'caviar', 'mink oil']

NOT_ANIMAL = ['vegan', 'vegetable', 'plant', 'phyto']

UNCERTAIN = ['squalane', 'squalene', 'cholesterol', 'stearic acid']

def has_animal(inci_text):
    ingredients = inci_text.split(' | ')
    for ingredient in ingredients:
        plant_version = False
        for word in NOT_ANIMAL:
            if word in ingredient:
                plant_version = True
        if plant_version:
            continue
        if ingredient == 'mel' or 'honey' in ingredient or 'mel extract' in ingredient:
            return True
        for animal in ANIMAL_INGREDIENTS:
            if animal in ingredient:
                return True
    return False

def is_uncertain(inci_text):
    ingredients = inci_text.split(' | ')
    for ingredient in ingredients:
        for word in UNCERTAIN:
            if word in ingredient:
                return True
    return False

STEP_TEXT = {'cleanser': 'Cleanser', 'moisturizer': 'Moisturizer', 'sunscreen': 'Sunscreen'}

TEXTURE_TEXT = {'rich': 'rich texture, best suited to dry skin', 'medium': 'medium texture, suits most skin types', 'light': 'light texture, best suited to combination to oily skin'}

ACTIVE_NAMES = {'salicylic acid': 'salicylic acid', 'niacinamide': 'niacinamide', 'azelaic acid': 'azelaic acid', 'zinc pca': 'zinc PCA', 'zinc gluconate': 'zinc gluconate', 'ceramide': 'ceramides', 'panthenol': 'panthenol'}

KEY_ACTIVE_LIMIT = 2 / 3

def actives_found(inci_text):
    """Our key actives in the first two thirds of the list (after that, probably a trace: preservative or pH)."""
    ingredients = str(inci_text).split(' | ')
    limit = max(1, round(len(ingredients) * KEY_ACTIVE_LIMIT))
    found = []
    for inci, name in ACTIVE_NAMES.items():
        for ingredient in ingredients[:limit]:
            if inci in ingredient and name not in found:
                found.append(name)
    return found

def join_words(words):
    """['a'] -> 'a', ['a', 'b'] -> 'a and b', ['a', 'b', 'c'] -> 'a, b and c'."""
    if len(words) == 1:
        return words[0]
    return ', '.join(words[:-1]) + ' and ' + words[-1]

def describe(row):
    """Two short sentences, in English, from the catalogue columns."""
    title = STEP_TEXT[row['role']]
    if row['role'] == 'cleanser':
        if row['rinse_mode'] == 'rinse-off':
            title = 'Rinse-off ' + title.lower()
        else:
            title = 'No-rinse ' + title.lower()
    text = title + ', ' + TEXTURE_TEXT[row['texture']] + '.'
    actives = actives_found(row['inci_text'])
    if len(actives) > 0:
        text = text + ' Contains ' + join_words(actives) + '.'
    return text

def badges(row):
    """At most 3 short labels, from the ingredient list only. Order: fragrance, key active, animal."""
    labels = []
    if row['has_parfum'] == False:
        labels.append('Fragrance-free')
    actives = actives_found(row['inci_text'])
    if len(actives) > 0:
        labels.append(actives[0].capitalize())
    if row['is_vegan']:
        labels.append('No animal-derived ingredients')
    return ' · '.join(labels[:3])
