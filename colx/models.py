# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Cart(models.Model):
    itemitem_no = models.OneToOneField('Item', models.DO_NOTHING, db_column='Itemitem_no', primary_key=True)  # Field name made lowercase.
    studentroll = models.ForeignKey('Student', models.DO_NOTHING, db_column='Studentroll')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cart'
        unique_together = (('itemitem_no', 'studentroll'),)



class Item(models.Model):
    item_no = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    price = models.IntegerField()
    img = models.CharField(max_length=255)
    seller = models.ForeignKey('Student', models.DO_NOTHING, db_column='seller',related_name='seller')
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    buyer = models.ForeignKey('Student', models.DO_NOTHING, db_column='buyer', blank=True, null=True,related_name='buyer')

    class Meta:
        managed = False
        db_table = 'item'


class Student(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    roll_number = models.CharField(unique=True, max_length=255)
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    class_field = models.CharField(db_column='class', max_length=255)  # Field renamed because it was a Python reserved word.
    section = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    mobile_no = models.DecimalField(max_digits=10, decimal_places=0)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'
