from flask import Flask, request, json, render_template
from Enums.brand_enum import BrandEnum
from Model.user_info import UserInfo
from util import related_brand
from util import sql_util

import logging
import json

# Flask App
app = Flask(__name__)

# Db connection
con = sql_util.get_db_connection()

# Logger
logging.basicConfig(filename="logger.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w')
logger = logging.getLogger()


@app.route('/scrap', methods=['GET', 'POST'])
def scrap():
    if request.method == 'POST':
        json_body = json.loads(request.data)
        parse_url = str(json_body['url'])
        max_comment = int(json_body['comment_count'])
        brand = parse_url.split(".")[1].upper()

        try:
            brand_enum = BrandEnum[brand]
        except (Exception,):
            return "Not supported url", 400

        comments = related_brand.call_related_brand_method(
            brand_name=brand_enum,
            url=parse_url,
            max_comment_count=max_comment
        )
        comment_json = json.dumps(comments, indent=4)
        user = UserInfo(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                        BrandEnum[brand].name, parse_url, comment_json)

        con.execute("INSERT INTO user_info (ip, brand, request_url, response) VALUES(?, ?, ?, ?)",
                    (str(user.ip), str(user.brand), str(user.request_url), str(user.response)))

        con.commit()
        logging.info(user.__str__())

        return comments

    elif request.method == 'GET':
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        query_dict = con.execute("SELECT * FROM user_info WHERE ip = ?", (str(ip),)).fetchall()

        response = []
        for x in query_dict:
            res = {
                "ip": x["ip"],
                "brand": x["brand"],
                "request_url": x["request_url"],
                "response": json.loads(x["response"])
            }

            response.append(res)

        return response, 200


if __name__ == '__main__':
    app.run()
