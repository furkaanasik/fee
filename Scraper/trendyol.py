import requests


def scrap_comments(url: str, max_comment_count: int):
    all_review = {
        "comments": []
    }

    # Get product id and merchant id from url
    merchantId = int(url.split("&")[1].replace("merchantId=", ""))
    product_id = int(url.split("?")[0].split("-")[-1])

    product_review_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}" \
                         f"?merchantId={merchantId}&storefrontId=1&culture=tr-TR&order=5&searchValue=" \
                         f"&onlySellerReviews=false&page=0 "

    # Get Trendyol data.
    response = requests.get(url=product_review_url)
    json_response = (response.json())

    # Get productReviews json.
    # productReviews = json_response.get("result").get("productReviews")
    productReviews = json_response["result"]["productReviews"]

    # Get total page count.
    # total_page = int(productReviews.get("totalPages")) + 1
    total_page = int(productReviews["totalPages"]) + 1

    for i in range(0, total_page):
        try:
            product_review_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}" \
                                 f"?merchantId={merchantId}&storefrontId=1&culture=tr-TR&order=5&searchValue=" \
                                 f"&onlySellerReviews=false&page={i}"

            # Get Trendyol data.
            response = requests.get(url=product_review_url)
            json_response = (response.json())

            # Get productReviews json.
            productReviews = json_response["result"]["productReviews"]

            # Get content array in json.
            content = productReviews["content"]

            # Get id, owner, comment, rate, date, isElite, isInfluencer information from json file.
            # Add these information data all_review json file.
            for review in content:
                if max_comment_count != len(all_review['comments']) or max_comment_count == 0:
                    all_review['comments'].append(review)
                else:
                    all_review['commentCount'] = len(all_review['comments'])
                    return all_review
        except (Exception,):
            pass

    all_review['commentCount'] = len(all_review['comments'])
    return all_review
