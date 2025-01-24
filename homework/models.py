class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        Возвращает True, если количество продукта больше или равно запрашиваемому,
        и False в обратном случае
        """
        if quantity < 0:
            return False
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        Метод покупки.
        Проверяет количество продукта с помощью метода check_quantity.
        Если продуктов не хватает, выбрасывает исключение ValueError.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if not self.check_quantity(quantity):
            raise ValueError("Not enough quantity available")
        self.quantity -= quantity

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество.
        """
        if buy_count <= 0:
            return  # Игнорируем добавление нулевого или отрицательного количества
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция.
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция.
        Игнорирует попытку удаления отрицательного количества.
        """
        if product not in self.products:
            return
        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        elif remove_count > 0:
            self.products[product] -= remove_count

    def clear(self):
        """
        Очищает корзину.
        """
        self.products.clear()

    def get_total_price(self) -> float:
        """
        Возвращает общую стоимость всех продуктов в корзине.
        """
        return sum(product.price * quantity for product, quantity in self.products.items())

    def buy(self):
        """
        Метод покупки.
        Проверяет наличие всех товаров на складе.
        Если товаров недостаточно, выбрасывает ValueError.
        После успешной покупки очищает корзину.
        """
        if not self.products:
            raise ValueError("Cart is empty")
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(f"Not enough quantity for product: {product.name}")
        for product, quantity in self.products.items():
            product.buy(quantity)
        self.clear()
