import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.127 Safari/537.36'}

base_request_url = 'https://user-content-gw-hermes.hepsiburada.com/queryapi/v2'


def scrap_comments(url: str, max_comment_count: int):
    all_review = {
        "comments": [],
    }

    sku = url.split("-")[-1]

    base_review_url = f'{base_request_url}/ApprovedUserContents?sku={sku}&from=0&size=100'

    response = requests.get(url=base_review_url, headers=headers)
    json_response = (response.json())

    while True:
        comments = json_response['data']['approvedUserContent']['approvedUserContentList']

        for comment in comments:
            customer = {
                "name": f"{comment['customer']['name']}  {comment['customer']['surname']}",
                "isInfluencer": comment['customer']['isInfluencer'],
                "gender": comment['customer']['gender'],
                "birthDate": comment['customer']['birthDate']
            }

            created_at = comment['createdAt']
            review = comment['review']['content']
            if review is None:
                continue

            add_dict = {
                'customer': customer,
                'created_at': created_at,
                'review': review
            }

            if max_comment_count != len(all_review['comments']) or max_comment_count == 0:
                all_review['comments'].append(add_dict)
            else:
                all_review['commentCount'] = len(all_review['comments'])
                return all_review

        next_url = json_response['links']['next']
        if next_url is not None:
            request_url = base_request_url + str(next_url).replace('Sku', 'sku')
            response = requests.get(url=request_url, headers=headers)
            json_response = (response.json())
        else:
            all_review['commentCount'] = len(all_review['comments'])
            return all_review
