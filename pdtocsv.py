import pandas as pd

neg_df = pd.read_pickle('neg_df.pkl')
pos_df_raw = pd.read_pickle('pos_df_raw.pkl')
pos_df_proc = pd.read_pickle('pos_df_proc.pkl')

neg_df.to_csv('ndf.csv')
pos_df_raw.to_csv('pdr.csv')
pos_df_proc.to_csv('pdp.csv')
