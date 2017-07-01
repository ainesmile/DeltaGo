import re
from deltago.commodity_data.countdown import products

ELEMENT = ".//div[@class=\"product-details-description\"]"

ORIGIN_FIELD = ".//div[@id=\"product-details-rating\"]/p/text()[1]"
FIELD = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
INGREDIENT_TEXT_FIELD = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
INGREDIENT_NOTE_FIELD = ".//div[@class=\"navigation-toggle-children\"]/div/text()"
NUTRITIONAL_TABLE_TR = ".//div[@class=\"nutritionInfo-table\"]/table/tbody/tr/td/text()"
PIC_URL = ".//img[@class=\"product-image\"]/@src"


def get_origin(tree):
    return get_node_value(tree, ORIGIN_FIELD)

def get_node_value(tree, node_name):
    try:
        return tree.xpath(node_name)[0]
    except IndexError:
        return None

def get_ingredient(element):
    text = ''.join(element.xpath(INGREDIENT_TEXT_FIELD))
    note = get_node_value(element, INGREDIENT_NOTE_FIELD)
    return {
        "text": text,
        "note": note
    }

def get_nutritions(element):
    nutritions = []
    table = element.xpath(NUTRITIONAL_TABLE_TR)
    for t in table:
        if re.search(r'\d', t):
            nutritions.append(t)
    return nutritions

def get_descriptions(tree):
    descriptions = {}
    elements = tree.xpath(ELEMENT)
    descriptions["ingredient"] = get_ingredient(elements[0])
    descriptions["nutritions"] = get_nutritions(elements[1])
    descriptions["claims"] = get_node_value(elements[2], FIELD)
    descriptions["endorsements"] = get_node_value(elements[3], FIELD)
    return descriptions

def get_pic_url(base_url, tree):
    return base_url + get_node_value(tree, PIC_URL)

def get_details(base_url, product):
    url = base_url + product["href"]
    tree = products.get_tree(url)
    name = product["name"]
    origin = get_origin(tree)
    descriptions = get_descriptions(tree)
    pic_url = get_pic_url(base_url, tree)
    return {
        "name": name,
        "origin": origin,
        "descriptions": descriptions,
        "pic_url": pic_url
    }



def fetch(base_url, products):
    details = []
    for product in products:
        details.extend(get_details(base_url, product))
    return details