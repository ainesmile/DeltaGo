

ORIGIN_FIELD = ".//div[@id=\"product-details-rating\"]/p/text()[1]"
INGREDIENT_TEXT_FIELD = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
INGREDIENT_NOTE_FIELD = ".//div[@class=\"navigation-toggle-children\"]/div/text()"

def combine_text(field):
    str = ''
    for f in field:
        str += f
    return str

def get_ingredient_text(element):
    field = element.xpath(INGREDIENT_FIELD)
    text = combine_text(field)
    return text

def get_ingredient_note(element):
    note = element.xpath(INGREDIENT_NOTE_FIELD)
    return note

def get_urls(base_url, products):
    urls = {}
    for p in products:
        name = p["name"]
        href = base_url + p["href"]
        urls.update({name:href})
    return urls

def get_origin(tree):
    origins = tree.xpath(ORIGIN_FIELD)
    if len(origins) > 0 :
        origin = origins[0]
    else:
        origin = "null"
    return origin
