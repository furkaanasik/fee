import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.127 Safari/537.36'}


def scrap_comments(url: str, max_comment_count: int):
    all_review = {
        "comments": []
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_id = soup.find("div", attrs={"class": "product-list__product-code pull-left product-id"}).get(
        "data-productid")
    product_review_url = f"https://www.vatanbilgisayar.com/ProductDetail/Comments/?productId={product_id}"

    response = requests.get(url=product_review_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    all_comments = soup.find_all("div", attrs={"class": "col-md-12 ds-table comment-items"})

    for elements in all_comments:
        id = elements.find("div", attrs={"class": "comment-likebtn"}).find("a").get("data-commentid")
        owner = elements.find("div", attrs={"class": "comment-name"}).find("span").get_text()
        comment = elements.find("div", attrs={"class": "comment"}).get_text(strip=True)
        date = elements.find("span", attrs={"class": "replaced-date"}).get_text()

        add_dict = {
            "id": id,
            "owner": owner,
            "comment": comment,
            "date": date
        }

        if max_comment_count != len(all_review['comments']) or max_comment_count == 0:
            all_review['comments'].append(add_dict)
        else:
            all_review['commentCount'] = len(all_review['comments'])
            return all_review

    all_review['commentCount'] = len(all_review['comments'])
    return all_review
