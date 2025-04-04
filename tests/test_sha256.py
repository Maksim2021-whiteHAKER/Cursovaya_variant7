""" Тестовый файл для проверки хеширования SHA-256. """
import hashlib

# Функция для хеширования строки в SHA-256
def sha256_hash(text: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))  # Преобразуем строку в байты
    return sha256.hexdigest()  # Возвращаем хеш в виде шестнадцатеричной строки

# Пример использования:
original_text = input("Введите текст/числа: ")
hashed_text = sha256_hash(original_text)

print("Оригинальный текст:", original_text)
print("SHA-256 хеш:", hashed_text)
