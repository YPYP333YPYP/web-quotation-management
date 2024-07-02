from core.response.code.base_code import BaseCode


class ErrorStatus(BaseCode):

    # Common
    BAD_REQUEST = ("1000", "잘못된 요청입니다.", "COMMON")
    UNAUTHORIZED = ("1001", "인증이 필요합니다.", "COMMON")
    FORBIDDEN = ("1002", "접근 권한이 없습니다.", "COMMON")
    NOT_FOUND = ("1003", "리소스를 찾을 수 없습니다.", "COMMON")
    METHOD_NOT_ALLOWED = ("1004", "허용되지 않은 메소드입니다.", "COMMON")
    CONFLICT = ("1005", "리소스 충돌이 발생했습니다.", "COMMON")
    INTERNAL_SERVER_ERROR = ("1006", "내부 서버 오류가 발생했습니다.", "COMMON")
    SERVICE_UNAVAILABLE = ("1007", "서비스를 사용할 수 없습니다.", "COMMON")

    # Authentication & Authorization
    INVALID_TOKEN = ("2000", "유효하지 않은 토큰입니다.", "AUTH")
    TOKEN_EXPIRED = ("2001", "토큰이 만료되었습니다.", "AUTH")
    INVALID_CREDENTIALS = ("2002", "잘못된 인증 정보입니다.", "AUTH")
    ACCOUNT_LOCKED = ("2003", "계정이 잠겼습니다.", "AUTH")
    ACCOUNT_DISABLED = ("2004", "계정이 비활성화되었습니다.", "AUTH")
    PASSWORD_EXPIRED = ("2005", "비밀번호가 만료되었습니다.", "AUTH")
    INSUFFICIENT_PERMISSIONS = ("2006", "권한이 부족합니다.", "AUTH")
    INVALID_PASSWORD = ("2007", "현재 비밀번호와 일치하지 않습니다", "AUTH")
    PASSWORDS_MUST_BE_DIFFERENT = ("2008", "현재 비밀번호와 과거 비밀번호는 달라야 합니다", "AUTH")

    # Database
    DB_CONNECTION_ERROR = ("3000", "데이터베이스 연결 오류가 발생했습니다.", "DATABASE")
    DB_QUERY_ERROR = ("3001", "데이터베이스 쿼리 실행 중 오류가 발생했습니다.", "DATABASE")
    DB_INTEGRITY_ERROR = ("3002", "데이터베이스 무결성 제약 조건 위반이 발생했습니다.", "DATABASE")
    DB_TIMEOUT_ERROR = ("3003", "데이터베이스 작업 시간이 초과되었습니다.", "DATABASE")

    # Validation
    INVALID_INPUT = ("4000", "잘못된 입력 값입니다.", "VALIDATION")
    REQUIRED_FIELD_MISSING = ("4001", "필수 필드가 누락되었습니다.", "VALIDATION")
    INVALID_FORMAT = ("4002", "잘못된 데이터 형식입니다.", "VALIDATION")
    VALUE_TOO_LONG = ("4003", "입력 값이 너무 깁니다.", "VALIDATION")
    VALUE_TOO_SHORT = ("4004", "입력 값이 너무 짧습니다.", "VALIDATION")

    # File Errors
    FILE_NOT_FOUND = ("5000", "파일을 찾을 수 없습니다.", "FILE")
    FILE_TOO_LARGE = ("5001", "파일 크기가 너무 큽니다.", "FILE")
    INVALID_FILE_TYPE = ("5002", "유효하지 않은 파일 형식입니다.", "FILE")
    FILE_UPLOAD_ERROR = ("5003", "파일 업로드 중 오류가 발생했습니다.", "FILE")
    INVALID_VALUE = ("5004", "파일 CELL 값이 올바르지 않습니다", "FILE")

    # External Service
    EXTERNAL_SERVICE_UNAVAILABLE = ("6000", "외부 서비스를 사용할 수 없습니다.", "EXTERNAL")
    EXTERNAL_SERVICE_TIMEOUT = ("6001", "외부 서비스 응답 시간이 초과되었습니다.", "EXTERNAL")
    EXTERNAL_SERVICE_ERROR = ("6002", "외부 서비스에서 오류가 발생했습니다.", "EXTERNAL")

    PRODUCT_NOT_FOUND = ("4001", "요청한 상품을 찾을 수 없습니다.", "PRODUCT")
    INVALID_PRODUCT_DATA = ("4002", "유효하지 않은 상품 데이터입니다.", "PRODUCT")
    PRODUCT_ALREADY_EXISTS = ("4003", "이미 존재하는 상품입니다.", "PRODUCT")
    PRODUCT_NOT_UPDATED = ("4004", "Product가 업데이트 되지 않았습니다.", "PRODUCT")
    PRODUCT_NOT_CREATED = ("4005", "Product가 생성 되지 않았습니다..", "PRODUCT")

    # User related error statuses (10000-10999)
    USER_NOT_FOUND = ("4001", "요청한 사용자를 찾을 수 없습니다.", "USER")
    INVALID_USER_DATA = ("4002", "유효하지 않은 사용자 데이터입니다.", "USER")
    USER_ALREADY_EXISTS = ("4003", "이미 존재하는 사용자입니다.", "USER")

    # 필요한 다른 에러 상태 코드들을 여기에 추가할 수 있습니다.