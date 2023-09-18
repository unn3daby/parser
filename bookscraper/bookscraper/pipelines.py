# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if value is not None:
                if isinstance(value, str) and not value.strip():
                    adapter[field_name] = None
                else:
                    adapter[field_name] = value.strip()

        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value is not None:
                adapter[lowercase_key] = value.lower()

        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None:
                value = value.replace('£', '').strip()
                if value:
                    adapter[price_key] = float(value)
                else:
                    # Если строка была пустой после удаления символа '£', установите значение на None
                    adapter[price_key] = None

        availability_string = adapter.get('availability')
        if availability_string is not None:
            split_string_array = availability_string.split('(')
            if len(split_string_array) >= 2:
                availability_array = split_string_array[1].split()
                if len(availability_array) > 0:
                    adapter['availability'] = int(availability_array[0])
                else:
                    adapter['availability'] = 0
            else:
                adapter['availability'] = 0

        num_reviews_string = adapter.get('num_reviews')
        if num_reviews_string is not None:
            adapter['num_reviews'] = int(num_reviews_string)

        stars_string = adapter.get('stars')
        if stars_string is not None:
            split_stars_array = stars_string.split(' ')
            if len(split_stars_array) >= 2:
                stars_text_value = split_stars_array[1].lower()
                if stars_text_value == "zero":
                    adapter['stars'] = 0
                elif stars_text_value == "one":
                    adapter['stars'] = 1
                elif stars_text_value == "two":
                    adapter['stars'] = 2
                elif stars_text_value == "three":
                    adapter['stars'] = 3
                elif stars_text_value == "four":
                    adapter['stars'] = 4
                elif stars_text_value == "five":
                    adapter['stars'] = 5

        return item
