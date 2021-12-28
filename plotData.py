from datetime import datetime as dt, timedelta
import numpy as np
import pandas as pd
import pymongo
# from pymongo import MongoClient
# cluster = MongoClient(
#     'mongodb+srv://digitalcommerce:digitalcommerce@cluster0.i5rre.mongodb.net/line_db?retryWrites=true&w=majority')
# db = cluster['line_db']

# collection = db['line_log']


df = pd.read_csv(
    r'C:\Users\tatpi\wan\internDPlus\python_selenium\chat_log.csv')

df.columns = ['message_id', 'user_id', 'cs_id',
              'sent_by', 'message_type', 'time', 'message']

# drop chat that is not the first one in section
t = df[['user_id', 'cs_id', 'sent_by']]
df = df[(t.ne(t.shift())).any(axis=1)]
# df = df.drop(['message_id', 'message_type',
#              'message'], axis=1)
df['time'] = pd.to_datetime(df['time'])

# ----------------------------
# df['clock_out'] = dt.strptime('17.30', '%H.%M').time()
# df['clock_out'] = dt.combine(df['time'], dt.strptime(
#     '17.30', '%H.%M').time())
# print(df.head(10))

# print(df['time'].dtypes)


# df['hour_min'] = df['time'].dt.time
# df['clock_out'] = dt.timestamp(dt(2019, 11, 11, 17, 30)).dt.time
# df['clock_in'] = dt(2019, 11, 11, 8, 30).time()
# print(df.head(40))
# print(dt.fromtimestamp(df['time']) > df['clock_out'])
# -----------------------------------


# calculate time difference
df['delta'] = (df['time']-df['time'].shift()).fillna(0)

# print(df) #มีทั้งเวลารอ customer ตอบ และ sale ตอบ
df.drop(df.index[df['sent_by'] == 'customer'], inplace=True)
# ต้องเอาข้อความแรกออก ไม่งั้นคิดเวลาข้ามแชท
df = df[df["message"].str.contains("ขอบคุณที่เป็นเพื่อนกับ Bewell") == False]
# df = df[df["message"].str.contains(
#     "ต้องขออภัยเป็นอย่างยิ่งที่บัญชีนี้ไม่สามารถตอบข้อความใดๆ") == False]


df = df.drop(['message_id', 'message_type',
             'message', 'sent_by'], axis=1)
# print(df)
# print(df = df.groupby([df['Date_Time'].dt.date]).mean())
# for unique_sale_id in df['sale_id'].unique():
#     # print(df.drop(['sale_id'], axis=1))
#     # print(df.groupby([df['time'].dt.date]).mean(numeric_only=False))
#     df_cs = df
#     df_cs['new'] = df_cs['delta'].values.astype(np.int64)
#     df_cs['time'] = df_cs['time'].dt.date
#     df_cs = df_cs.drop(['delta'], axis=1)
#     print(df_cs)
#     means = df_cs.groupby('time').mean()
#     means['new'] = pd.to_timedelta(means['new'])
#     print(means)

#     # means['new'] = pd.to_timedelta(means['new'])

#     # print(means)
print('----------------------------------------')
print(df['cs_id'].unique())
for unique_cs_id in df['cs_id'].unique():

    # print(type(unique_cs_id))
    if not(str(unique_cs_id).find('ข้อความตอบกลับ')):
        continue
    cs = df.loc[df['cs_id'] == unique_cs_id]
    cs['avg_time'] = cs['delta'].values.astype(np.int64)

    cs['time'] = cs['time'].dt.date

    cs = cs.drop(['delta'], axis=1)
    # print(cs)
    means = cs.groupby('time').mean()
    means['customer_num'] = cs.groupby('time')['user_id'].nunique()
    # means['avg_time'] = pd.to_timedelta(means['avg_time'])
    # means['avg_timex'] = pd.to_timedelta(means['avg_time'])
    means['avg_time_min'] = means['avg_time']/60000000000
    means['cs_id'] = unique_cs_id
    # means['timex'] = cs['time']

    # .apply(list).to_dict()
    # print(unique_cs_id)
    means = means.reset_index()

    # print(cs)
    # .dt.strftime('%Y, %m, %d')
    means['time'] = means['time'].apply(lambda x: x.strftime('%Y%m%d'))
    # means['time'] = means['time'].strftime("%Y, %m, %d")
    # means['avg_time'] = str(means['avg_time'])
    means.rename(columns={'time': 'date'}, inplace=True)
    means = means.drop(['avg_time'], axis=1)
    print(means)

    # db.line_log.insert_many(means.to_dict('records'))
