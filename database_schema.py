import datetime

from bson.objectid import ObjectId
from mongoengine import *

# ADMIN_STATES = ['up', 'down', 'UP', 'DOWN']

EXPENSE_TYPE = ['mortgage', 'car', 'utilities', 'grocery', 'misc', 'restaurants', 'milo', 'uthaya_personal', 'madhu_personal']


class ExpenseBase(EmbeddedDocument):
    transaction_date = DateTimeField(default=datetime.datetime.now())
    transaction_amount = FloatField()
    transaction_store = StringField()
    classification = StringField(choices=EXPENSE_TYPE, default='grocery')

    @queryset_manager
    def get_data_by_transaction_amount(doc_cls, queryset, transaction_amount):
        """
        Returns the keychain object based on the given keychain name
        :param queryset:
        :return: null or keychain object
        """
        return queryset.filter(Q(chain_name=transaction_amount)).first()



    # @queryset_manager
    # def get_latest_version_number_of_block(doc_cls, queryset, mw_id, wo_id, stage, scope, runat, block_index):
    #     """
    #     Returns latest version number of a block. If empty, it returns 0
    #     """
    #     most_recent = queryset.filter(Q(mw_id=mw_id) & Q(wo_id=wo_id) & Q(stage=stage) & Q(scope=scope) & Q(block_index=block_index) & Q(runat=runat)).order_by("-updated_at").first()
    #     if not most_recent:
    #         return 0
    #     return most_recent.version_numbe

class Month(Document):
    month = StringField(unique=True)
    expenses = EmbeddedDocumentListField(ExpenseBase)
