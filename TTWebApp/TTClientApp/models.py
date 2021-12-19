from django.db import models

class Attributes(models.Model):
    attributeid = models.IntegerField(db_column='AttributeID', blank=True, primary_key=True)  # Field name made lowercase.
    attributename = models.CharField(db_column='AttributeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attributes'


class Category(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', blank=True, primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Category'


class Categoryattribute(models.Model):
    categoryid = models.ForeignKey(Category, db_column='CategoryID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    attributeid = models.ForeignKey(Attributes, db_column='AttributeID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CategoryAttribute'


class Cities(models.Model):
    cityid = models.AutoField(db_column='CityID', blank=True, primary_key=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cities'


class Supllier(models.Model):
    supllierid = models.AutoField(db_column='SupllierID', blank=True, primary_key=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=50)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=50)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=50)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=50, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Supllier'

        
class Product(models.Model):
    productid = models.AutoField(db_column='ProductID', blank=True, primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=50)  # Field name made lowercase.
    categoryid = models.ForeignKey(Category, db_column='CategoryID', on_delete=models.PROTECT, blank=True)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=50)  # Field name made lowercase.
    price = models.CharField(db_column='Price', max_length=50, null=True)  # Field name made lowercase.
    supllierid = models.ForeignKey(Supllier, db_column='SupllierID', on_delete=models.SET_NULL, blank=True, null=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=50, null=True)  # Field name made lowercase.
    discription = models.TextField(db_column='Discription', null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Product'


class Cutomers(models.Model):
    customerid = models.AutoField(db_column='CustomerID', blank=True, primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', unique=True, max_length=50)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=50)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', unique=True, max_length=25)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128)  # Field name made lowercase.
    registerdate = models.DateField(auto_now_add=True, db_column='RegisterDate')  # Field name made lowercase.
    lastlogin = models.DateField(auto_now_add=True, db_column='LastLogin')  # Field name made lowercase.
    isactive = models.TextField(db_column='IsActive')  # Field name made lowercase. This field type is a guess.
    isadmin = models.TextField(db_column='IsAdmin')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Cutomers'


class Productattribute(models.Model):
    productid = models.ForeignKey(Product, db_column='ProductID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    attributeid = models.ForeignKey(Attributes, db_column='AttributeID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    attributevalue = models.TextField(db_column='AttributeValue', blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProductAttribute'


class Customercart(models.Model):
    customerid = models.ForeignKey(Cutomers, db_column='CustomerID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, db_column='ProductID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count')  # Field name made lowercase.
    adddate = models.DateField(auto_now_add=True, db_column='AddDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerCart'


class Customerwishlist(models.Model):
    customerid = models.ForeignKey(Cutomers, db_column='CustomerID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, db_column='ProductID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    adddate = models.DateField(auto_now_add=True, db_column='AddDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerWishList'


class Guestcart(models.Model):
    guestid = models.AutoField(db_column='GuestID', blank=True, primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, db_column='ProductID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', null=True)  # Field name made lowercase.
    adddate = models.DateField(auto_now_add=True, db_column='AddDate')  # Field name made lowercase.
    conectionvalue = models.TextField(db_column='ConectionValue')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GuestCart'


class Status(models.Model):
    statusid = models.AutoField(db_column='StatusID', blank=True, primary_key=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Status'


class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', blank=True, primary_key=True)  # Field name made lowercase.
    cutomerid = models.ForeignKey(Cutomers, db_column='CutomerID', on_delete=models.PROTECT, blank=True)  # Field name made lowercase.
    orderdate = models.DateField(auto_now_add=True, db_column='OrderDate')  # Field name made lowercase.
    cityid = models.ForeignKey(Cities, db_column='CityID', on_delete=models.PROTECT, blank=True)  # Field name made lowercase.
    shippostalcode = models.CharField(db_column='ShipPostalCode', max_length=50)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50)  # Field name made lowercase.
    statusid = models.ForeignKey(Status, db_column='StatusID', on_delete=models.PROTECT, blank=True)  # Field name made lowercase.
    paymenttype = models.CharField(db_column='PaymentType', max_length=50)  # Field name made lowercase.
    statusdate = models.IntegerField(db_column='StatusDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Orders'


class Orderdetails(models.Model):
    orderid = models.ForeignKey(Orders, db_column='OrderID', on_delete=models.CASCADE, blank=True)  # Field name made lowercase.
    productid = models.ForeignKey(Product, db_column='ProductID', on_delete=models.PROTECT, blank=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    discount = models.IntegerField(db_column='Discount')  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    total = models.IntegerField(db_column='Total')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrderDetails'

