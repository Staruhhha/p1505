from django.db import models

MAX_LEN=100


class Distributor(models.Model):
    name = models.CharField(max_length=MAX_LEN, verbose_name='Название дистрибьютора')
    agent_firstname = models.CharField(max_length=MAX_LEN, verbose_name='Фамилия поставщика')
    agent_name = models.CharField(max_length=MAX_LEN, verbose_name='Имя поставщика')
    agent_patronymic = models.CharField(max_length=MAX_LEN, blank=True,verbose_name='Отчество поставщика')
    agent_phone = models.CharField(max_length=MAX_LEN, verbose_name='Телефон представителя')
    email = models.CharField(max_length=MAX_LEN, verbose_name='Электронная почта')

    def __str__(self):
        return f"{self.name} {self.agent_firstname} {self.agent_phone}"

    class Meta:
        verbose_name = 'Дистрибьютор'
        verbose_name_plural = 'Дистрибьюторы'


class Purchase(models.Model):
    date_purchase = models.DateTimeField(verbose_name='Дата закупки')

    distributor = models.ForeignKey(Distributor, on_delete=models.PROTECT, verbose_name='Дистрибьютор')
    software = models.ManyToManyField('Software', through='Pos_purchase', verbose_name='Программное обеспечение')

    def __str__(self):
        return f'{self.date_purchase} {self.distributor.name}'

    class Meta:
        verbose_name = 'Закупка'
        verbose_name_plural = 'Закупки'


class Pos_purchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, verbose_name='Закупка')
    software = models.ForeignKey('Software', on_delete=models.PROTECT, verbose_name='Программное обеспечение')

    count = models.PositiveIntegerField(verbose_name='Кол-во цифровых копий')

    def __str__(self):
        return f"{self.software.name}: {self.count} {self.purchase}"

    class Meta:
        verbose_name = 'Позиция закупки'
        verbose_name_plural = 'Позиции закупки'


class Order(models.Model):
    CARD = 'CRD'
    SBP = 'SBP'
    UMONEY = 'UMN'

    PAYMENT = [
        (CARD, "Картой"),
        (SBP, 'Система быстрых платежей'),
        (UMONEY, 'ЮMoney')
    ]

    customer_firstname = models.CharField(max_length=MAX_LEN, verbose_name='Фамилия клиента')
    customer_name = models.CharField(max_length=MAX_LEN, verbose_name='Имя клиента')
    customer_patronymic = models.CharField(max_length=MAX_LEN, blank=True, verbose_name='Отчество клиента')

    delivery_email = models.CharField(max_length=MAX_LEN, verbose_name='Адрес почты для доставки')
    payment_type = models.CharField(max_length=3, choices=PAYMENT, verbose_name='Способ оплаты')

    commentary = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')

    software = models.ManyToManyField('Software', through='Pos_order', verbose_name='Программное обеспечение')

    def fio_customer(self):
        return f"{self.customer_firstname} {self.customer_name} {self.customer_patronymic}"

    def __str__(self):
        if self.customer_patronymic:
            return f"{self.pk} {self.customer_firstname} {self.customer_name[0]}.{self.customer_patronymic[0]}."
        return f"{self.pk} {self.customer_firstname} {self.customer_name[0]}."


    class Meta:
        verbose_name ='Заказ'
        verbose_name_plural = 'Заказы'

class Pos_order(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Закупка')
    software = models.ForeignKey('Software', on_delete=models.PROTECT, verbose_name='Программное обеспечение')

    count = models.PositiveIntegerField(verbose_name='Кол-во цифровых копий')
    discount = models.IntegerField(default=0, verbose_name='Скидка')

    def __str__(self):
        return f"{self.order} {self.software.name}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Похиции заказа'


class Parametr(models.Model):
    name = models.CharField(unique=True, max_length=MAX_LEN, verbose_name='Характеристика')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товара'


class Pos_parametr(models.Model):
    parametr = models.ForeignKey(Parametr, on_delete=models.PROTECT, verbose_name='Характеристика')
    software = models.ForeignKey('Software', on_delete=models.PROTECT, verbose_name='Книга')

    value = models.CharField(max_length=MAX_LEN, verbose_name='Значение характеристики')

    def __str__(self):
        return f"{self.software.name} | {self.parametr.name} : {self.value}"

    class Meta:
        verbose_name = 'Позиция характеристики'
        verbose_name_plural = 'Позиции характеристики'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=MAX_LEN, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описании категории')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Developer(models.Model):
    name = models.CharField(unique=True, max_length=MAX_LEN, verbose_name='Наименование разработчика')
    description = models.TextField(blank=True, verbose_name='Описании разработчика')
    photo = models.ImageField(upload_to="developer/%Y/%m/%d", blank=True, verbose_name='Изображение')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Разработчик'
        verbose_name_plural = 'Разработчики'


class Software(models.Model):
    name = models.CharField(max_length=MAX_LEN, verbose_name='Наименование ПО')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_length=10, decimal_places=2, default=990, verbose_name='Цена')
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    datetime_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    image = models.ImageField(upload_to="software/%Y/%m/%d", blank=True, verbose_name='Изображение')
    is_exists = models.BooleanField(default=True, verbose_name='Существует ли?')

    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, verbose_name='Разработчик')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    parametr = models.ManyToManyField(Parametr, through=Pos_parametr, verbose_name='Характеристики')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
