import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.127 Safari/537.36'}


def scrap_comments(url: str, max_comment_count: int):
    all_review = {
        "comments": []
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_id = soup.find("a", attrs={"id": "getWishList"}).get("data-productid")

    n11_review_url = f"https://www.n11.com/component/render/productReviews?page=1&productId={product_id}"

    response = requests.get(url=n11_review_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        page_count = int(soup.find("a", attrs={"class": "pageLink last"}).get_text())
    except (Exception,):
        page_count = 1

    for i in range(page_count):
        n11_review_url = f"https://www.n11.com/component/render/productReviews?page={i + 1}&productId={product_id}"

        response = requests.get(url=n11_review_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        in_page_comments = soup.find_all("li", attrs={"class": "comment"})

        for comment in in_page_comments:
            id = comment.get("data-reviewid")
            owner = comment.find("span", attrs={"class": "userName"}).get_text().strip()
            owner_comment = comment.find("p").get_text().strip()
            comment_date = comment.find("span", attrs={"class": "commentDate"}).get_text().strip()

            add_dict = {
                "id": id,
                "owner": owner,
                "comment": owner_comment,
                "date": comment_date
            }

            if max_comment_count != len(all_review['comments']) or max_comment_count == 0:
                all_review['comments'].append(add_dict)
            else:
                all_review['commentCount'] = len(all_review['comments'])
                return all_review

    all_review['commentCount'] = len(all_review['comments'])
    return all_review
