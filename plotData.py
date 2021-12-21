import pandas as pd
import numpy as np
from datetime import datetime as dt, timedelta

df = pd.read_csv(
    r'C:\Users\tatpi\wan\internDPlus\python_selenium\chat_log.csv')

df.columns = ['message_id', 'user_id', 'sale_id',
              'sent_by', 'message_type', 'time', 'message']

# drop chat that is not the first one
t = df[['user_id', 'sale_id', 'sent_by']]
df = df[(t.ne(t.shift())).any(axis=1)]

# calculate time difference
df['time'] = pd.to_datetime(df['time'])
df['delta'] = (df['time']-df['time'].shift()).fillna(0)

# print(df) #มีทั้งเวลารอ customer ตอบ และ sale ตอบ
df.drop(df.index[df['sent_by'] == 'customer'], inplace=True)
# ต้องเอาข้อความแรกออก ไม่งั้นคิดเวลาข้ามแชท
df = df[df["message"].str.contains("ขอบคุณที่เป็นเพื่อนกับ Test Bot") == False]
df = df[df["message"].str.contains(
    "ต้องขออภัยเป็นอย่างยิ่งที่บัญชีนี้ไม่สามารถตอบข้อความใดๆ") == False]


df = df.drop(['message_id', 'user_id', 'message_type',
             'message', 'sent_by'], axis=1)
# print(df)
# print(df = df.groupby([df['Date_Time'].dt.date]).mean())
for unique_sale_id in df['sale_id'].unique():
    # print(df.drop(['sale_id'], axis=1))
    # print(df.groupby([df['time'].dt.date]).mean(numeric_only=False))

    df['new'] = df['delta'].values.astype(np.int64)
    df['time'] = df['time'].dt.date
    df = df.drop(['delta'], axis=1)
    print(df)
    means = df.groupby('time').mean()
    print(means)

    # means['new'] = pd.to_timedelta(means['new'])

    # print(means)
