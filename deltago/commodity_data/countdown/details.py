


def get_urls(base_url, products):
    urls = {}
    for p in products:
        name = p["name"]
        href = base_url + p["href"]
        urls.update({name:href})
    return urls