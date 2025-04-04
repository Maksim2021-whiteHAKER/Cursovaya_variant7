from enum import Enum

class ERROR(Enum):
    """Перечисление возможных ошибок API."""
    OK = 0
    UNAUTHORIZED = 1
    DATABASE_ERROR = 2
    BAD_REQUEST = 3
    INTERNAL_ERROR = 4
    OBJ_NOT_FOUND = 5
    UNKNOWN_DEVICE = 6
    UNABLE_CHANGE = 7
    FAIL_CHANGE = 8


class APIError:
    """Класс для работы с текстовыми описаниями ошибок API."""
    errors = {
        0: 'Ok',
        1: 'Не авторизован',
        2: 'Ошибка базы данных',
        3: 'Неверный запрос',
        4: 'Внутренняя ошибка',
        5: 'Объект, указанный в запросе, не найден',
        6: 'Неверный идентификатор устройства',
        7: 'Невозможно изменить состояние данного устройства',
        8: 'Не удалось изменить состояние устройства',
    }

    @staticmethod
    def err(error: ERROR) -> str:
        """
        Возвращает текстовое описание ошибки по её Enum значению.
        Аналог from_enum, но с более коротким именем для удобства.
        """
        return APIError.errors.get(error.value, "Неизвестная ошибка")

        

    @staticmethod
    def get_message(error_code: int) -> str:
        """
        Возвращает текстовое описание ошибки по её коду.

        :param error_code: Код ошибки (целое число).
        :return: Текстовое описание ошибки или "Неизвестная ошибка".
        """
        return APIError.errors.get(error_code, "Неизвестная ошибка")

    @staticmethod
    def from_enum(error: ERROR) -> str:
        """
        Возвращает текстовое описание ошибки по её Enum значению.

        :param error: Экземпляр перечисления ERROR.
        :return: Текстовое описание ошибки.
        """
        if not isinstance(error, ERROR):
            raise ValueError("Параметр должен быть экземпляром ERROR")
        return APIError.errors[error.value]