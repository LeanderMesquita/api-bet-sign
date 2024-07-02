import re
from playwright.sync_api import Page, expect
from time import sleep
from api.src.utils.logger.index import log

def click_and_fill(page: Page, selector:str, value:str, press:str = None, before_delay:float = 0.35, after_delay:float = 0.35):
    try:
        if before_delay > 0:
            sleep(before_delay)

        log.debug(f'Filling selector: {selector} with value: {value}')
        page.get_by_label(selector).click()
        page.get_by_label(selector).fill(value)

        if press != None:
            page.get_by_label(selector).press(press)

        if after_delay > 0:
            sleep(after_delay)    
    except ValueError as e:
        log.error(f'Error when trying fill selector: {selector} with value: {value}. ERROR: {e} ')