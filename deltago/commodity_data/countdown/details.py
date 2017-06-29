

ORIGIN_FIELD = ".//div[@id=\"product-details-rating\"]/p/text()[1]"

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
