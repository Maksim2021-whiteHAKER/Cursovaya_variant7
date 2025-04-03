""" Тестовый файл для проверки хеширования SHA-256. """
import hashlib

# Функция для хеширования строки в SHA-256
def sha256_hash(text: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))  # Преобразуем строку в байты
    return sha256.hexdigest()  # Возвращаем хеш в виде шестнадцатеричной строки

# Функция для попытки восстановления оригинальной строки из хеша (невероятно сложно!)
def hash_to_text(hash_value: str) -> str:
    # Важно понимать, что восстановить строку из хеша невозможно без использования словарей или атак на основе брутфорса
    return "Невозможно восстановить исходный текст из SHA-256"

# Пример использования:
original_text = input("Введите текст/числа: ")
hashed_text = sha256_hash(original_text)

print("Оригинальный текст:", original_text)
print("SHA-256 хеш:", hashed_text)

# Попытка восстановить строку из хеша
recovered_text = hash_to_text(hashed_text)
print("Восстановленный текст:", recovered_text)
