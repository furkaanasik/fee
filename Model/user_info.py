class UserInfo:
    ip = None
    brand = None
    request_url = None
    response = None

    def __init__(self, ip, brand, request_url, response):
        self.ip = ip
        self.brand = brand
        self.request_url = request_url
        self.response = response

    def __str__(self):
        return f'UserInfo(ip = {self.ip}, brand = {self.brand}, request_url = {self.request_url}, response = {self.response})'
