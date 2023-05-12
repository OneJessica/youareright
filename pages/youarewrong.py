import streamlit as st
from config import setting
from utl.analysis import analysis_wrong
from utl.get_res import get_api
from utl import get_words
import requests
import json
from datetime import datetime
setting()
st.title('错题本')
with st.expander('错题统计'):

    url = 'http://127.0.0.1:5000/questions/api/'
    analysis = analysis_wrong()
    st.dataframe(analysis)
    wrong_index = set(analysis['序号'].to_list())
    wrong_index = [str(i) for i in wrong_index]
st.subheader('错题回顾')
st.write(url+'_'.join(wrong_index))
content = get_api(url = url+'_'.join(wrong_index),method='get',is_jsonify= True)
# st.json(content)
if 'wrong_index' not in st.session_state:
    st.session_state.wrong_index = 0
def incre_index():
    if st.session_state.wrong_index < len(content)-1:
        st.session_state.wrong_index += 1
def decre_index():
    if st.session_state.wrong_index > 0:
        st.session_state.wrong_index -= 1
def get_explain(text):
    explain_list = []

    text_list = text[2:].split(r' ')

    text_list = [i.strip() for i in text_list if i]
    for text in text_list:
        words_explain=get_words(text)
        if len(words_explain)>0:
            explain_list.append(words_explain)
    return explain_list
col1_1,col1_2,col2_1 = st.columns([1,2,2])
with col1_1:
    st.button('上一道', on_click = decre_index)
with col1_2:
    st.button('下一道', on_click=incre_index)
col1,col2 = st.columns(2)
with col1:
    questions = content[str(st.session_state.wrong_index)]
    num = questions['序号']
    st.subheader(f'第{num}题')
    if not content:
        st.info('暂无错题')
        st.stop()

    st.markdown(questions['试题'])
    right_answer = questions['答案']

    myanswer_full = st.radio('请选择',['不确定']+json.loads(questions['选项']),index = 0,horizontal = True)
    myanswer_choice = myanswer_full.split(':')[0]
    myanswer_content = myanswer_full.split(r'[A-D]:')[-1]
    if myanswer_choice == '不确定':
        notsure = questions['试题']
    elif  right_answer== myanswer_choice:
        st.success('You are right')
    else:
        with open('data/错题本.csv','a+') as f:
            f.write(f"{num}, 错选为{myanswer_choice}', {datetime.now()}")
            f.write('\n')

        st.error('You are wrong. The right answer is {}'.format(right_answer))



@st.cache(suppress_st_warning=True)
def ai_helper(questions):
    st.write({"text":"解释以下词语或句子的含义 "+str(questions['试题'])})
    res1 = requests.post('ai_url', data=json.dumps({"text":"解释以下词语或句子的含义"+str(questions['试题'])}))
    return res1
with col2:
    if st.button('解析'):
        st.markdown(questions['解析'])
        for i in json.loads(questions['选项']):
            st.text(i)
            st.write(get_explain(i))
    if st.button('AI helper'):
        st.markdown('建设中')
        # st.markdown(ai_helper(questions['答案']))