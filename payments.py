import pandas as pd
import datetime


def add_payment_to_csv(payment_info, month):
    payments_df = pd.read_csv('payments/тест.csv')  # f'payments/{month}_платежи.csv для прода'
    df_row = pd.DataFrame([payment_info])
    payments_df = pd.concat([payments_df, df_row], ignore_index=True)
    payments_df.to_csv('payments/тест.csv', index=False)


def get_users(month):
    users_df = pd.read_csv('payments/тест.csv')
    users = users_df["Имя_Фамилия"].to_list()
    return users

