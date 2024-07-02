from core.response.code.base_code import BaseCode


class SuccessStatus(BaseCode):
    OK = ("200", "요청에 성공하였습니다.", "COMMON")
    CREATED = ("201", "리소스가 생성되었습니다.", "COMMON")

    # Product related success statuses
    PRODUCT_CREATED = ("201", "상품이 성공적으로 생성되었습니다.", "PRODUCT")
    PRODUCT_UPDATED = ("200", "상품이 성공적으로 업데이트되었습니다.", "PRODUCT")
    PRODUCT_DELETED = ("200", "상품이 성공적으로 삭제되었습니다.", "PRODUCT")

    # User related success statuses
    USER_CREATED = ("201", "사용자가 성공적으로 생성되었습니다.", "USER")
    USER_UPDATED = ("200", "사용자 정보가 성공적으로 업데이트되었습니다.", "USER")

