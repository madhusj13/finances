# author: rafals
# date: 2018-05-22
# email: rafal.sadowski@nokia.com

from bson import ObjectId, DBRef
# from cmd import input
from six.moves import input as raw_input

import datetime
import json
import random
import re
import csv
import database_schema
import mongoengine
from database_schema import *

if __name__ == '__main__':
    import sys
    import os.path

    sys.path.append(os.path.realpath('..'))


class DataHandler(object):
    def __init__(self):
        pass

    def create_month_entry(self, month):
        try:
            self.month_obj = Month(month=month).save()
        except mongoengine.errors.NotUniqueError:
            self.month_obj = Month.objects.filter(month=month).first()

    def add_default_expense(self, month, transaction_date, transaction_amount, transaction_store, classification):
        self.create_month_entry(month)
        eb = ExpenseBase(
            transaction_date=transaction_date,
            transaction_amount=transaction_amount,
            transaction_store=transaction_store,
            classification=classification
        )
        self.month_obj.expenses.append(
            eb
        )
        self.month_obj.save()

    def save_file(self, month, csv_file):
        self.create_month_entry(month)
        with open(csv_file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            total = 0
            for row in reader:
                if not row or 'Transaction Date' in row[0]:
                    continue
                if row and 'capital_one' in csv_file:
                    if row[5]:
                        if 'dining' in row[5].lower():
                            continue
                        # print (row)
                        classification = 'misc'
                        if 'Dining' in row[4]:
                            classification = 'restaurants'
                        elif 'Merchandise' in row[4]:
                            if 'apple' in row[3].lower():
                                classification = 'uthaya_personal'
                            else:
                                classification = 'grocery'
                        elif 'Automotive' in row[4]:
                            classification = 'utilities'
                        elif 'Internet' in row[4]:
                            if 'amzn' in row[3].lower():
                                classification = 'milo'
                        elif 'phone' in row[4].lower():
                            classification = 'utilities'

                        total += float(row[5])
                        eb = ExpenseBase(
                            transaction_date=row[0],
                            transaction_store=row[3],
                            transaction_amount=float(row[5]),
                            classification=classification,
                        )
                        self.month_obj.expenses.append(
                            eb
                        )
                elif row and 'cibc' in csv_file:
                    if 'Internet Banking INTERNET TRANSFER' in row[1]:
                        print('This row is skipped intentionally -- %s' %
                              (row[1]))
                        continue
                    if 'MASTERCARD' in row[1]:
                        print(
                            'This row is skipped intentionally MASTERCARD bill payment -- %s amount %s' % (row[1], row[2]))
                        continue
                    if 'QUESTRADE' in row[1]:
                        print(
                            'This row is skipped intentionally QT money transfer -- %s amount %s' % (row[1], row[2]))
                        continue
                    if 'GLOBAL MONEY TRANSFER' in row[1]:
                        print(
                            'This row is skipped intentionally QT money transfer -- %s amount %s' % (row[1], row[2]))
                        continue
                    if row[2]:
                        if 'VW' in row[1]:
                            classification = 'car'
                        if 'CHEQUE' in row[1]:
                            classification = 'milo'
                        if 'NETWORK FEE' in row[1] or 'PREAUTHORIZED' in row[1]:
                            classification = 'utilities'
                        if 'E-TRANSFER' in row[1]:
                            classification = 'madhu_personal'
                        if 'INTERNET BILL PAY' in row[1]:
                            classification = 'utilities'
                        if 'shawarma' in row[1].lower():
                            classification = 'restaurants'
                        try:
                            total += float(row[2])
                            eb = ExpenseBase(
                                transaction_date=row[0],
                                transaction_store=row[1],
                                transaction_amount=row[2],
                                classification=classification,
                            )
                        except Exception as e:
                            print("ERROR : ")
                            print(str(e))
                            print('Row in question :: %s' % (row))
                            raise

                        self.month_obj.expenses.append(
                            eb
                        )
            self.month_obj.save()
        return total


if __name__ == '__main__':
    month = raw_input("Month: ")
    # print ('You chose %s' % (month))
    mongoDb = 'mongodb://localhost:27017/expense_report'
    client = database_schema.connect(db='expense_report', host=mongoDb)
    print('remove expense_report')
    dt = DataHandler()
    mon = Month.objects.filter(month=month).first()
    if mon:
        mon.delete()
    print('processing capital one')
    total = dt.save_file(
        month=month, csv_file='/Users/msharma/Documents/csv_dir/%s/capital_one.csv' % (month))
    print('Capital one total :%s' % (total))
    print('processing cibc')
    total = dt.save_file(
        month=month, csv_file='/Users/msharma/Documents/csv_dir/%s/cibc.csv' % (month))
    print('CIBC total :%s' % (total))
    # dt.add_default_expense(
    #     month = month,
    #     transaction_amount = 2000,
    #     transaction_date = '03/01/2020',
    #     transaction_store = 'cibc',
    #     classification = 'mortgage'
    # )

    mon = Month.objects.filter(month=month).first()
    sum = 0
    print(mon.expenses.count())
    for obj in mon.expenses:
        # print (obj.transaction_store, obj.transaction_amount)
        sum += obj.transaction_amount
    print('Total : %s' % str(sum))
    print('Uthaya owes :: %s' % str((int(sum))/2))
