import json
import os
from datetime import datetime
from typing import List, Optional

# Модель данных Expense
class Expense:
    def __init__(self, amount: float, category: str, date: datetime):
        self.amount = amount
        self.category = category
        self.date = date
    
    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} | {self.category:<15} | {self.amount:>10.2f} ₽"
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d")
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Expense(
            amount=data["amount"],
            category=data["category"],
            date=datetime.strptime(data["date"], "%Y-%m-%d")
        )

# Основной класс приложения
class ExpenseTracker:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.file_path = "expenses.json"
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.expenses = [Expense.from_dict(item) for item in data]
                print(f"Загружено {len(self.expenses)} записей.")
            else:
                self.expenses = []
                print("Создан новый файл расходов.")
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.expenses = []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            data = [expense.to_dict() for expense in self.expenses]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Данные сохранены.")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def validate_amount(self, amount: float) -> bool:
        """Проверка корректности суммы"""
        if amount < 0:
            print("Ошибка: Сумма не может быть отрицательной!")
            return False
        return True
    
    def validate_date(self, date_str: str) -> Optional[datetime]:
        """Проверка корректности даты"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Ошибка: Неверный формат даты! Используйте ГГГГ-ММ-ДД (например, 2024-03-15)")
            return None
    
    def add_expense(self):
        """Добавление расхода"""
        print("\n--- Добавление расхода ---")
        
        # Ввод суммы
        try:
            amount = float(input("Введите сумму: "))
            if not self.validate_amount(amount):
                return
        except ValueError:
            print("Ошибка: Введите корректное число!")
            return
        
        # Ввод категории
        category = input("Введите категорию: ").strip()
        if not category:
            print("Ошибка: Категория не может быть пустой!")
            return
        
        # Ввод даты
        date_input = input("Введите дату (ГГГГ-ММ-ДД) или Enter для сегодняшней: ").strip()
        if not date_input:
            date = datetime.today()
        else:
            date = self.validate_date(date_input)
            if date is None:
                return
        
        self.expenses.append(Expense(amount, category, date))
        self.save_data()
        print("Расход успешно добавлен!")
    
    def view_all_expenses(self):
        """Просмотр всех расходов"""
        print("\n--- Все расходы ---")
        
        if not self.expenses:
            print("Нет записей о расходах.")
            return
        
        # Сортируем по дате
        sorted_expenses = sorted(self.expenses, key=lambda x: x.date)
        
        print(f"{'Дата':<12} | {'Категория':<15} | {'Сумма':>10}")
        print("-" * 40)
        
        for i, expense in enumerate(sorted_expenses, 1):
            print(f"{i}. {expense}")
        
        print("-" * 40)
        total = sum(e.amount for e in self.expenses)
        print(f"Общая сумма: {total:>10.2f} ₽")
    
    def delete_expense(self):
        """Удаление расхода"""
        print("\n--- Удаление расхода ---")
        
        if not self.expenses:
            print("Нет записей для удаления.")
            return
        
        self.view_all_expenses()
        
        try:
            index = int(input(f"\nВведите номер записи для удаления (1-{len(self.expenses)}): "))
            if index < 1 or index > len(self.expenses):
                print("Ошибка: Неверный номер записи!")
                return
            
            # Получаем отсортированный список для соответствия нумерации
            sorted_expenses = sorted(self.expenses, key=lambda x: x.date)
            removed = sorted_expenses[index - 1]
            self.expenses.remove(removed)
            self.save_data()
            print(f"Удалена запись: {removed}")
        except ValueError:
            print("Ошибка: Введите корректный номер!")
    
    def filter_expenses(self):
        """Фильтрация по категории или дате"""
        print("\n--- Фильтрация расходов ---")
        print("1. По категории")
        print("2. По дате")
        choice = input("Выберите опцию: ").strip()
        
        filtered = None
        
        if choice == "1":
            category = input("Введите категорию: ").strip()
            filtered = [e for e in self.expenses if e.category.lower() == category.lower()]
            print(f"\nРасходы по категории '{category}':")
        
        elif choice == "2":
            date_input = input("Введите дату (ГГГГ-ММ-ДД): ").strip()
            date = self.validate_date(date_input)
            if date is None:
                return
            filtered = [e for e in self.expenses if e.date.date() == date.date()]
            print(f"\nРасходы за {date.strftime('%Y-%m-%d')}:")
        
        else:
            print("Неверный выбор!")
            return
        
        if not filtered:
            print("Записи не найдены.")
            return
        
        print(f"{'Дата':<12} | {'Категория':<15} | {'Сумма':>10}")
        print("-" * 40)
        
        for expense in filtered:
            print(expense)
        
        print("-" * 40)
        total = sum(e.amount for e in filtered)
        print(f"Итого: {total:>10.2f} ₽")
    
    def calculate_sum_by_period(self):
        """Подсчёт суммы расходов за период"""
        print("\n--- Подсчёт расходов за период ---")
        
        start_input = input("Введите начальную дату (ГГГГ-ММ-ДД): ").strip()
        start_date = self.validate_date(start_input)
        if start_date is None:
            return
        
        end_input = input("Введите конечную дату (ГГГГ-ММ-ДД): ").strip()
        end_date = self.validate_date(end_input)
        if end_date is None:
            return
        
        if start_date > end_date:
            print("Ошибка: Начальная дата не может быть позже конечной!")
            return
        
        period_expenses = [
            e for e in self.expenses 
            if start_date.date() <= e.date.date() <= end_date.date()
        ]
        total = sum(e.amount for e in period_expenses)
        
        print(f"\nРасходы за период с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}:")
        print(f"Всего записей: {len(period_expenses)}")
        print(f"Общая сумма: {total:.2f} ₽")
        
        if period_expenses:
            print("\nДетализация по категориям:")
            from collections import defaultdict
            by_category = defaultdict(float)
            for expense in period_expenses:
                by_category[expense.category] += expense.amount
            
            for category, amount in by_category.items():
                print(f"  {category}: {amount:.2f} ₽")
    
    def run(self):
        """Главное меню"""
        while True:
            print("\n=== Учёт расходов ===")
            print("1. Добавить расход")
            print("2. Просмотреть все расходы")
            print("3. Удалить расход")
            print("4. Фильтрация расходов")
            print("5. Подсчёт суммы за период")
            print("6. Выход")
            
            choice = input("Выберите опцию: ").strip()
            
            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_all_expenses()
            elif choice == "3":
                self.delete_expense()
            elif choice == "4":
                self.filter_expenses()
            elif choice == "5":
                self.calculate_sum_by_period()
            elif choice == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

# Запуск приложения
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
