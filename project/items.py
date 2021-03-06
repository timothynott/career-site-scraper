# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags, replace_entities
from .procs import date_proc, description_proc, job_type_proc, job_level_proc, wage_proc, shifts_proc

# TODO: remove unused items/loaders


class Job(Item):
    company = Field()
    jobSourceUrl = Field()
    address = Field()
    city = Field()
    state = Field()
    postalCode = Field()
    title = Field()
    date = Field(output_processor=date_proc)
    description = Field(output_processor=description_proc)
    jobType = Field(output_processor=job_type_proc)
    jobLevel = Field(output_processor=job_level_proc)
    shiftInfo = Field(input_processor=Identity())
    wageInfo = Field(input_processor=Identity())


class WageInfo(Item):
    base = Field(output_processor=wage_proc)
    max = Field(output_processor=wage_proc)


class ShiftInfo(Item):
    shifts = Field(output_processor=shifts_proc)  # [FIRST, SECOND, THIRD]
    startTime = Field()
    endTime = Field()
    days = Field(output_processor=Identity())  # [M, TU, W, TH, F, SA, SU]


class JobLoader(ItemLoader):
    default_item_class = Job
    default_input_processor = MapCompose(remove_tags, replace_entities, str.strip)
    default_output_processor = TakeFirst()


class WageInfoLoader(ItemLoader):
    default_item_class = WageInfo
    default_input_processor = MapCompose(remove_tags, replace_entities, str.strip)
    default_output_processor = TakeFirst()


class ShiftInfoLoader(ItemLoader):
    default_item_class = ShiftInfo
    default_input_processor = MapCompose(remove_tags, replace_entities, str.strip)
    default_output_processor = TakeFirst()
