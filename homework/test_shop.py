"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(10) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(10)
        assert product.quantity == 990

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match="Not enough quantity available"):
            product.buy(1001)

    def test_product_check_zero_quantity(self, product):
        assert product.check_quantity(0) is True

    def test_product_buy_zero_quantity(self, product):
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            product.buy(0)

    def test_product_check_negative_quantity(self, product):
        assert product.check_quantity(-1) is False

    def test_product_buy_negative_quantity(self, product):
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            product.buy(-1)


class TestCart:
    """
    Тесты для класса Cart
    """

    def test_cart_add_product(self, cart, product):
        cart.add_product(product, 5)
        assert cart.products[product] == 5

    def test_cart_add_existing_product(self, cart, product):
        cart.add_product(product, 5)
        cart.add_product(product, 3)
        assert cart.products[product] == 8

    def test_cart_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 3)
        assert cart.products[product] == 2
        cart.remove_product(product, 2)
        assert product not in cart.products

    def test_cart_remove_product_entirely(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products

    def test_cart_clear(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert len(cart.products) == 0

    def test_cart_get_total_price(self, cart, product):
        cart.add_product(product, 5)
        assert cart.get_total_price() == 500

    def test_cart_buy_success(self, cart, product):
        cart.add_product(product, 5)
        cart.buy()
        assert product.quantity == 995
        assert len(cart.products) == 0

    def test_cart_buy_insufficient_stock(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError, match="Not enough quantity for product: book"):
            cart.buy()

    def test_cart_add_zero_quantity(self, cart, product):
        cart.add_product(product, 0)
        assert product not in cart.products

    def test_cart_remove_more_than_available(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 10)
        assert product not in cart.products

    def test_cart_remove_negative_quantity(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, -1)
        assert cart.products[product] == 5

    def test_cart_add_multiple_products(self, cart):
        product1 = Product("book", 100, "Book 1", 1000)
        product2 = Product("notebook", 50, "Notebook", 500)
        cart.add_product(product1, 3)
        cart.add_product(product2, 2)
        assert cart.products[product1] == 3
        assert cart.products[product2] == 2

    def test_cart_get_total_price_multiple_products(self, cart):
        product1 = Product("book", 100, "Book 1", 1000)
        product2 = Product("notebook", 50, "Notebook", 500)
        cart.add_product(product1, 3)
        cart.add_product(product2, 2)
        assert cart.get_total_price() == 400

    def test_cart_buy_empty(self, cart):
        with pytest.raises(ValueError, match="Cart is empty"):
            cart.buy()
