# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# TRUNCATE TABLE dbtest.store_app_choice;
# SET FOREIGN_KEY_CHECKS = 0;
# TRUNCATE TABLE dbtest.store_app_question;
# SET FOREIGN_KEY_CHECKS = 1;
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=10, unique=True,
                            default="question")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Customer(models.Model):
    idcustomer = models.AutoField(db_column='idCustomer', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    address = models.TextField()
    tel = models.CharField(max_length=45)
    username = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    create = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customer'


class Document(models.Model):
    iddocument = models.AutoField(db_column='idDocument', primary_key=True)  # Field name made lowercase.
    no_field = models.CharField(db_column='No.', unique=True, max_length=45)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    create = models.DateTimeField()# (auto_now_add = True)
    goods_idgoods = models.ForeignKey('Goods', models.DO_NOTHING, db_column='Goods_idGoods')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'document'


class Goods(models.Model):
    idgoods = models.AutoField(db_column='idGoods', primary_key=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', unique=True, max_length=45)  # Field name made lowercase.
    detail = models.TextField(db_column='Detail')  # Field name made lowercase.
    staff_idstaff = models.ForeignKey('Staff', models.DO_NOTHING, db_column='Staff_idStaff')  # Field name made lowercase.
    customer_idcustomer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Customer_idCustomer')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'goods'


class Staff(models.Model):
    idstaff = models.AutoField(db_column='idStaff', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    address = models.TextField()
    tel = models.CharField(max_length=45)
    username = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'staff'


class Product(models.Model):


    device_name = models.CharField(max_length=255);
    path_number = models.CharField(max_length=255);
    serial_number = models.CharField(max_length=255);
    device_type = models.CharField(max_length=255);
    location = models.CharField(max_length=255);
    status = models.BooleanField(default=True);
 


    def __str__(self):
        return 'Id:{0} Name:{1}'.format(self.id, self.device_name)
 # return self.device_name
  
