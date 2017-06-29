

ORIGIN_FIELD = ".//div[@id=\"product-details-rating\"]/p/text()[1]"
FIELD = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
INGREDIENT_TEXT_FIELD = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
INGREDIENT_NOTE_FIELD = ".//div[@class=\"navigation-toggle-children\"]/div/text()"

def first(list):
    try:
        return list[0]
    except IndexError:
        return None

def get_ingredient_text(element):
    field = element.xpath(INGREDIENT_TEXT_FIELD)
    return ''.join(field)

def get_ingredient_note(element):
    return first(element.xpath(INGREDIENT_NOTE_FIELD))

def get_field(element):
    return first(element.xpath(FIELD))

def get_urls(base_url, products):
    urls = {}
    for p in products:
        name = p["name"]
        href = base_url + p["href"]
        urls.update({name:href})
    return urls

def get_origin(tree):
    return first(tree.xpath(ORIGIN_FIELD))
