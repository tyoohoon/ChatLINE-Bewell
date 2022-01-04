from datetime import datetime as dt
import constants as const
import numpy as np
import pandas as pd
from pymongo import MongoClient

client = MongoClient(const.MONGO_CONNECTION)
db = client[const.DATABASE_NAME]

filename = const.CSV_CHAT_LOG_PATH + \
    str(dt.today().strftime("%Y-%m-%d")) + "_chat_log.csv"
df = pd.read_csv(filename)

df.columns = ['message_id', 'user_id', 'cs_id',
              'sent_by', 'message_type', 'time', 'message']

# drop chat that is not the first one in section
t = df[['user_id', 'cs_id', 'sent_by']]
df = df[(t.ne(t.shift())).any(axis=1)]

# drop row that is not within working hour
df['time'] = pd.to_datetime(df['time'])
df['only_date'] = df['time'].apply(lambda x: x.replace(
    hour=0, minute=0, second=0, microsecond=0))
df['clock_in_time'] = df['only_date'] + \
    np.timedelta64(8, 'h') + np.timedelta64(30, 'm')
df['clock_out_time'] = df['only_date'] + \
    np.timedelta64(17, 'h') + np.timedelta64(30, 'm')
df.loc[df['time'] > df['clock_out_time'], 'time'] = df['clock_out_time']
df.loc[df['time'] < df['clock_in_time'], 'time'] = df['clock_in_time']
df = df.drop(['clock_in_time', 'clock_out_time',
             'message_id', 'message'], axis=1)

for unique_cs_id in df['cs_id'].unique():
    if not(str(unique_cs_id).find('ข้อความตอบกลับ')):
        continue

    cs = df.loc[df['cs_id'] == unique_cs_id]
    for unique_date in cs['only_date'].unique():
        if(not pd.to_datetime(unique_date).strftime('%Y-%m-%d') == const.TARGET_DATE):
            continue
        cs_date = cs.loc[cs['only_date'] == unique_date]
        d = {
            'date': unique_date,
            'cs_id': unique_cs_id,
            'customer': cs_date['user_id'].nunique(),
            'total_time': 0,
            'total_reply': cs_date.loc[cs_date['sent_by'] == 'sale'].count().user_id.item(),
            'avg_time': 0
        }

        for unique_customer in cs_date['user_id'].unique():
            cs_date_customer = cs_date.loc[cs_date['user_id']
                                           == unique_customer]
            cs_date_customer['delta'] = (
                cs_date_customer['time']-cs_date_customer['time'].shift()).fillna(0)
            cs_date_customer.drop(
                cs_date_customer.index[cs_date_customer['sent_by'] == 'customer'], inplace=True)
            cs_date_customer['delta_int'] = cs_date_customer['delta'].values.astype(
                np.int64)
            d['total_time'] += cs_date_customer['delta_int'].sum()

        if(d['total_reply'] == 0):
            d['total_reply'] = 1

        d['avg_time'] = d['total_time'] / d['total_reply'] / 60000000000

        db.line_log.insert_one({
            'date': pd.to_datetime(d['date']).strftime('%Y%m%d'),
            'customer_num': d['customer'],
            'avg_time_min': d['avg_time'],
            'cs_id': d['cs_id'],
        })

        print({
            'date': pd.to_datetime(d['date']).strftime('%Y%m%d'),
            'customer_num': d['customer'],
            'avg_time_min': d['avg_time'],
            'cs_id': d['cs_id'],
        })
