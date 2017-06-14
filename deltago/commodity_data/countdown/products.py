from lxml import html
import requests
import re
import json

def replace(string):
    return re.sub('\s+\$', '', string)

def product_elements(url, stamp):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree.xpath(stamp)

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

def product_list(url, fields, category_field, stamp):
    products = []
    elements = product_elements(url, stamp)
    for element in elements:
        item = product(element, fields, category_field)
        products.append(item)
    return products

def sub(category_name, category_data, fields, stamp):
    sub = []
    for sub_category_name in category_data:
        category_field = {
            "category": category_name,
            "sub_category": sub_category_name
        }
        url = category_data[sub_category_name]
        products = product_list(url, fields, category_field, stamp)
        sub.extend(products)
    return sub

def fetch(file):
    with open(file, 'r') as data_file:
        commodity = json.load(data_file)
    babycare = commodity["countdown"]["B"]
    fields = commodity["fields"]
    stamp = commodity["stamp"]
    babycare_product_list = sub("B", babycare, fields, stamp)
    return babycare_product_list

def save(input_file, output_file):
    data = fetch(input_file)
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

# save('deltago/commodity_data/countdown/countdown.json', 'deltago/commodity_data/countdown/babycare.json')