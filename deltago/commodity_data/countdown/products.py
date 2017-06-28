from lxml import html
import requests
import re
import json
import math
import time

def replace(string):
    result = re.search(r'\d+\.\d+', string)
    return result.group()

def get_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def get_page_number(tree, element, per_page):
    per = int(per_page)
    item_text = tree.xpath(element)[0]
    result = re.search(r'\d+', item_text)
    item_number = result.group()
    if item_number:
        page = int(math.ceil(float(item_number)/per))
    else:
        page = 1
    return page

def field(product_element, field_name, field_details):
    ele = field_details["ele"]
    need_process = field_details["need_process"]
    field = product_element.xpath(ele)
    if not len(field):
        value = "null"
    else:
        value = field[0]
        if need_process:
            value = replace(value)
    return {field_name: value}

def product(product_element, fields, category_field):
    product_item = category_field.copy()
    for field_name in fields:
        field_details = fields[field_name]
        field_item = field(product_element, field_name, field_details)
        product_item.update(field_item)
    return product_item

def page_product(tree, fields, category_field, stamp):
    products = []
    elements = tree.xpath(stamp)
    for element in elements:
        item = product(element, fields, category_field)
        products.append(item)
    return products

def sub_product(base_url, items_number_element, per_page, fields, category_field, stamp):
    products = []
    base_tree = get_tree(base_url)
    base_produces = page_product(base_tree, fields, category_field, stamp)
    products.extend(base_produces)

    page_number = get_page_number(base_tree, items_number_element, per_page)
    if page_number > 1:
        for number in range(page_number-1):
            next_url = base_url + '?page=' + str(number+2)
            next_tree = get_tree(next_url)
            next_produces = page_product(next_tree, fields, category_field, stamp)
            products.extend(next_produces)
    return products

def sub(category_name, category_data, fields, stamp, items_number_element, per_page):
    subs = []
    for sub_category_name in category_data:
        category_field = {
            "category": category_name,
            "sub_category": sub_category_name
        }
        base_url = category_data[sub_category_name]
        products = sub_product(base_url, items_number_element, per_page, fields, category_field, stamp)
       
        subs.extend(products)
    return subs

def fetch(file):
    with open(file, 'r') as data_file:
        commodity = json.load(data_file)
    babycare = commodity["countdown"]["B"]
    fields = commodity["fields"]
    stamp = commodity["stamp"]
    items_number_element = commodity["items_number_element"]
    per_page = commodity["per_page"]
    babycare_product_list = sub("B", babycare, fields, stamp, items_number_element, per_page)
    return babycare_product_list

def save(input_file, output_file):
    data = fetch(input_file)
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

# save('deltago/commodity_data/countdown/countdown.json', 'deltago/commodity_data/countdown/babycare.json')