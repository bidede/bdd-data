from common.db_utils import mk_db
import pendulum
import traceback

Ohlcv = mk_db.ohlcv


# 分钟级k线
def add_ohlcv_records(records):
    try:
        # int_timestamp = int(pendulum.now().float_timestamp * 1000)
        if records:
            Ohlcv.insert(records)
        else:
            print('records empty, not insert')
    except Exception as e:
        print('error: add_ohlcv_records')
        traceback.print_exc()


def add_order_record(record_dict):
    try:
        int_timestamp = int(pendulum.now().float_timestamp * 1000)
        record_dict['created'] = int_timestamp
        record_dict['updated'] = int_timestamp
        OrderRecords.insert(record_dict)
    except Exception as e:
        print('error: add_order_record', record_dict)
        traceback.print_exc()


def get_order_records(query_dict):
    try:
        filter_dict = query_dict['filter_dict']
        limit = query_dict.get('limit', 10)
        return list(OrderRecords.find(filter_dict).sort([('_id', -1)]).limit(limit))
    except Exception as e:
        print('error: get_order_records', query_dict)
        traceback.print_exc()


def update_order_record(order_id, record_dict):
    try:
        int_timestamp = int(pendulum.now().float_timestamp * 1000)
        record_dict['updated'] = int_timestamp
        OrderRecords.update_one({'order_id': order_id}, {'$set': record_dict}, False)
    except Exception as e:
        print('error: update_order_record', order_id, record_dict)
        traceback.print_exc()
