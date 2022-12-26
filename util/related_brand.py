from Enums.brand_enum import BrandEnum
from Scraper import trendyol, vatan, n11, hepsiburada


def call_related_brand_method(brand_name, url, max_comment_count):
    if BrandEnum.TRENDYOL == brand_name:
        return trendyol.scrap_comments(url, max_comment_count)
    elif BrandEnum.VATANBILGISAYAR == brand_name:
        return vatan.scrap_comments(url, max_comment_count)
    elif BrandEnum.N11 == brand_name:
        return n11.scrap_comments(url, max_comment_count)
    elif BrandEnum.HEPSIBURADA == brand_name:
        return hepsiburada.scrap_comments(url, max_comment_count)
    else:
        return None
