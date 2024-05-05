import os
import datetime

# Функция для чтения данных из файла
def read_data(filename):
    data = []
    if not os.path.exists(filename):
        # Если файл не существует, создаем его
        with open(filename, 'w') as file:
            pass

    with open(filename, 'r') as file:
        lines = file.readlines()
        record = {}
        for line in lines:
            line = line.strip()
            if line:
                key, value = line.split(': ')
                record[key] = value
            else:
                data.append(record)
                record = {}
        if record:
            data.append(record)
    return data

# Функция для записи данных в файл
def write_data(filename, data):
    with open(filename, 'w') as file:
        for record in data:
            for key, value in record.items():
                file.write(f"{key}: {value}\n")
            file.write('\n')

# Функция для вывода баланса
def show_balance(data):
    total_income = 0
    total_expense = 0
    for record in data:
        if 'Категория' in record:  # Проверяем наличие ключа 'Категория'
            if record['Категория'] == 'Доход':
                total_income += int(record.get('Сумма', 0))
            elif record['Категория'] == 'Расход':
                total_expense += int(record.get('Сумма', 0))
    balance = total_income - total_expense
    print(f"Текущий баланс: {balance}")
    print(f"Доходы: {total_income}")
    print(f"Расходы: {total_expense}")

# Функция для добавления записи
def add_record(data):
    while True:
        date_str = input("\nВведите дату в формате (гггг-мм-дд) через дефис: ")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("\nНекорректный формат даты. Пожалуйста, введите дату в формате 'гггг-мм-дд'.")
    while True:
        category = input(
            "\nВведите категорию (Доход/Расход): ").capitalize()
        if category in ['Доход', 'Расход']:
            break
        else:
            print("\nНекорректная категория. Пожалуйста, введите 'Доход' или 'Расход'.")
    while True:
        amount = input("\nВведите сумму: ")
        if amount.isdigit() and int(amount) > 0:
            break
        else:
            print("\nНекорректная сумма. Введите положительное число в формате '1234567890' ")
    description = input("\nВведите описание: ").capitalize()
    record = {
        'Дата': date,
        'Категория': category,
        'Сумма': amount,
        'Описание': description
    }
    data.append(record)  # Добавляем новую запись в данные
    filename = "finances.txt"
    write_data(filename, data)  # Перезаписываем файл с обновленными данными
    print("\nЗапись добавлена успешно.")

# Функция для редактирования записи
def edit_record(data):
    search_criteria = input("\nВведите критерий для поиска записи (например: дату (гггг-мм-дд), категорию (Доход/Расход), сумму или описание расходов): ")

    found_records = []
    for record in data:
        for key, value in record.items():
            if isinstance(value, str) and value.lower() == search_criteria.lower():
                found_records.append(record)
                break
            elif isinstance(value, datetime.date) and value.strftime("%Y-%m-%d") == search_criteria:
                found_records.append(record)
                break

    if not found_records:
        print("\nЗапись не найдена.")
        return

    print("\nНайденные записи:")
    for i, record in enumerate(found_records, 1):
        print(f"№{i}. {record['Дата']} - {record['Категория']} - {record['Сумма']} - {record['Описание']}")

    try:
        choice = int(input("\nВведите номер записи для редактирования или удаления: "))
        if 0 < choice <= len(found_records):
            record = found_records[choice - 1]
            print("\nВыбранная запись:")
            print_record(record)
            action = input("\nВыберите действие (Редактирование/Удаление): ").capitalize()
            if action == "Редактирование":
                field = input("\nВведите поле для редактирования (Дата/Категория/Сумма/Описание): ").capitalize()
                if field == 'Дата':
                    while True:
                        new_value = input("\nВведите новую дату в формате (гггг-мм-дд): ")
                        try:
                            datetime.datetime.strptime(new_value, "%Y-%m-%d")
                            record[field] = new_value
                            print("\nЗапись успешно отредактирована.")
                            break
                        except ValueError:
                            print("\nНекорректный формат даты. Пожалуйста, введите дату в формате 'гггг-мм-дд'.")
                elif field == 'Категория':
                    while True:
                        new_value = input("\nВведите новую категорию (Доход/Расход): ").capitalize()
                        if new_value in ['Доход', 'Расход']:
                            record[field] = new_value
                            print("\nЗапись успешно отредактирована.")
                            break
                        else:
                            print("\nНекорректная категория. Пожалуйста, введите 'Доход' или 'Расход'.")
                elif field == 'Сумма':
                    while True:
                        new_value = input("\nВведите новую сумму: ")
                        if new_value.isdigit() and int(new_value) >= 0:
                            record[field] = new_value
                            print("\nЗапись успешно отредактирована.")
                            break
                        else:
                            print("\nНекорректная сумма. Введите положительное число.")
                elif field == 'Описание':
                    new_value = input(f"\nВведите новое значение для поля '{field}': ")
                    record[field] = new_value
                    print("\nЗапись успешно отредактирована.")
                else:
                    print("\nНекорректное поле.")
            elif action == "Удаление":
                confirm = input("\nВы уверены, что хотите удалить эту запись? (Да/Нет): ").capitalize()
                if confirm == "Да":
                    data.remove(record)
                    print("\nЗапись успешно удалена.")
                else:
                    print("\nУдаление отменено.")
            else:
                print("\nНекорректное действие.")
        else:
            print("\nНекорректный номер записи.")
    except ValueError:
        print("\nНекорректный ввод.")

# Функция для поиска записей по категории
def search_by_category(data):
    category = input("\nВведите категорию для поиска (Доход/Расход): ").capitalize()
    found_records = []
    for record in data:
        if 'Категория' in record and record['Категория'] == category:
            found_records.append(record)
    if found_records:
        print("\nНайденные записи по категории", category, ":")
        for record in found_records:
            print_record(record)
    else:
        print("\nЗаписи по указанной категории не найдены.")

# Функция для поиска записей по дате
def search_by_date(data):
    date_str = input("\nВведите дату в формате (гггг-мм-дд) через дефис: ")
    try:
        search_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        found_records = []
        for record in data:
            if 'Дата' in record and record['Дата'] == search_date:
                found_records.append(record)
        if found_records:
            print("\nНайденные записи по дате", search_date, ":")
            for record in found_records:
                print_record(record)
        else:
            print("\nЗаписи по указанной дате не найдены.")
    except ValueError:
        print("\nНекорректный формат даты. Пожалуйста, введите дату в формате 'дд-мм-гггг'.")

# Функция для поиска записей по сумме
def search_by_amount(data):
    amount_str = input("\nВведите сумму для поиска: ")
    try:
        amount = int(amount_str)
        found_records = []
        for record in data:
            if 'Сумма' in record and int(record['Сумма']) == amount:
                found_records.append(record)
        if found_records:
            print("\nНайденные записи по сумме", amount, ":")
            for record in found_records:
                print_record(record)
        else:
            print("\nЗаписи с указанной суммой не найдены.")
    except ValueError:
        print("\nНекорректная сумма. Введите целое число.")

# Основная функция для выбора типа поиска
def search_records(data):
    while True:
        print("\nВыберите тип поиска:")
        print("1. По категории")
        print("2. По дате")
        print("3. По сумме")
        print("4. Назад")
        choice = input("Введите номер типа поиска: ")
        if choice == '1':
            search_by_category(data)
        elif choice == '2':
            search_by_date(data)
        elif choice == '3':
            search_by_amount(data)
        elif choice == '4':
            break  # Возврат к предыдущему меню
        else:
            print("\nНекорректный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

# Функция для вывода записи на экран
def print_record(record):
    for key, value in record.items():
        print(f"{key}: {value}")
    print()

# Основная функция
def main():
    filename = "finances.txt"
    data = read_data(filename)

    while True:
        print("\n1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")
        print("5. Выход")

        choice = input("\nВыберите действие: ")

        if choice == '1':
            show_balance(data)
        elif choice == '2':
            add_record(data)
        elif choice == '3':
            edit_record(data)
        elif choice == '4':
            search_records(data)
        elif choice == '5':
            write_data(filename, data)
            print("\nДанные сохранены. До свидания!")
            break
        else:
            print("\nНекорректный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
