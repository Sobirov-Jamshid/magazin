from django.db import models


# Create your models here.

class BotUser(models.Model):
    objects = models.Manager()
    user_id = models.IntegerField()                 #Foydalanuvchi telegram chat_id si
    full_name = models.CharField(max_length=50)     #Ismi
    bot_state = models.IntegerField(default=0)      #bu qaysi bosqichda ekanligi ro`yxatda otish
    address = models.CharField(max_length=100)      #Manzili
    number1 = models.IntegerField(default=0)        #Bo`lib to`lash usulini tanlash
    contact = models.CharField(max_length=15)       #Telefon raqami
    number = models.IntegerField(default=1)         #Nechta ekanligini tanlash
    month = models.IntegerField(default=3)          #Necha oyga olish
    protsent = models.IntegerField(default=0)       #Necha % dan olishi
    created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10)      #Qaysi tilni tanlaganligi

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = verbose_name + "lar"


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    uzs = "So`m"
    dollar = "$"
    STATUS = [(uzs, "So`m"), (dollar, "$")]
    objects = models.Manager()
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_choice = models.CharField(max_length=50, choices=STATUS, default=uzs)
    price = models.IntegerField()
    image = models.ImageField(
        upload_to='image',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = verbose_name + "lar"

class ShopCard(models.Model):
    new = 'Tezkor Xarid 🛍'
    checked = 'Bo`lib to`lash'
    STATUS = [
        (new, 'Tezkor Xarid 🛍'),
        (checked, 'Bo`lib to`lash ⏳'),
    ]
    objects = models.Manager()
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default=new
        )

    chec = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    percent = models.IntegerField(default=0)
    month = models.IntegerField(default=0)

    payments = models.IntegerField(default=0)
    month_pay = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def shop_list(self):
        return list(self.products.all())

    def __str__(self):
        return str(self.product)


class Order(models.Model):
    objects = models.Manager()
    CANCELLED = 'Bekor qilingan ❌'
    new = 'Yangi 🆕'
    checked = 'Tayyoranmoqda ⏳'
    confirmed = 'Tayyor ✅'
    STATUS = [
        (CANCELLED, 'Bekor qilingan ❌'),
        (new, 'Yangi 🆕'),
        (checked, 'Tayyorlanmoqda ⏳'),
        (confirmed, 'Tayyor ✅')
    ]
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    products = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    all_price = models.IntegerField(default=0)
    currency = models.CharField(max_length=10)
    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default=new
    )
    check = models.BooleanField(default=False)

    def __str__(self):
        return str(self.products)


    class Meta:
        verbose_name = "Buyutma"
        verbose_name_plural = verbose_name + "lar"

class OrderCredit(models.Model):
    CANCELLED = 'Bekor qilingan ❌'
    new = 'Yangi 🆕'
    checked = 'Tekshirilmoqda ⏳'
    confirmed = 'Tayyor ✅'
    STATUS = [
        (CANCELLED, 'Bekor qilingan ❌'),
        (new, 'Yangi 🆕'),
        (checked, 'Tekshirilmoqda ⏳'),
        (confirmed, 'Tayyor ✅')
    ]
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=STATUS,
        default=new
    )
    products = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    protsent = models.IntegerField(default=0)
    month = models.IntegerField(default=12)
    payments = models.IntegerField(default=0)
    month_pay = models.IntegerField(default=0)
    all_price = models.IntegerField(default=0)
    currency = models.CharField(max_length=10)
    check = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.products)

    class Meta:
        verbose_name = "Buyurtma Kredit"
        verbose_name_plural = verbose_name + "lar"

class ShopCardOrderCredit(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    products = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    protsent = models.IntegerField(default=0)
    month = models.IntegerField(default=12)
    payments = models.IntegerField(default=0)
    month_pay = models.IntegerField(default=0)
    all_price = models.IntegerField(default=0)
    check = models.BooleanField(default=False)

    def __str__(self):
        return str(self.products)
        