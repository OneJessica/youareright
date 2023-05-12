import pandas as pd
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def analysis_wrong():
    wrong_text = pd.read_csv(f'{path}/data/错题本.csv')
    # with open(f'{path}/data/错题本.csv','w') as
    wrong_text.columns = ['序号','错选','时间']
    wrong_count = wrong_text.groupby(['序号','错选']).count()
    if len(wrong_count) > 0:
        wrong_count  = wrong_count.reset_index()
        wrong_count.columns = ['序号','错选','计数']
        return wrong_count
    return None
