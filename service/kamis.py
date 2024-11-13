
class AgriculturalService:
    BASE_URL = "http://www.kamis.or.kr/service/price/xml.do?action"

    def __init__(self, cert_key:str, cert_id: str):
        self.cert_key = cert_key
        self.cert_id = cert_id

