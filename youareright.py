import streamlit as st
from config import setting
import requests,json
from utl import get_words
from datetime import datetime
from utl.get_res import get_api
import pandas as pd
def main():
    setting()
    st.title('试题')
    url = "http://127.0.0.1:5000/questions/api"
    ai_url ='http://127.0.0.1:5000/ai/api'


    content = get_api(url = url,method='get')
    if 'index' not in st.session_state:
        st.session_state.index = 1
    def incre_index():
        if st.session_state.index < len(content):
            st.session_state.index += 1
    def decre_index():
        if st.session_state.index > 1:
            st.session_state.index -= 1

    def get_explain(text):
        explain_list = []

        text_list = text[2:].split(r' ')

        text_list = [i.strip() for i in text_list if i]
        for text in text_list:
            words_explain=get_words(text)
            if len(words_explain)>0:
                explain_list.append(words_explain)
        return explain_list

    tab1,tab2 = st.tabs(['试题','统计'])
    col1,col2 = st.columns(2)


    with tab1:
        with st.container():
            col1_1, col1_2, col2_1 = st.columns([1, 2, 2])
            with col1_1:
                st.button('上一道', on_click=decre_index)
            with col1_2:
                st.button('下一道', on_click=incre_index)
            with col1:
                st.subheader(f'第{st.session_state.index}题')
                questions = content[str(st.session_state.index)]
                st.markdown(questions['试题'])
                right_answer = questions['答案']
                myanswer_full = st.radio('请选择',['不确定']+questions['选项'],index = 0,horizontal = True)
                myanswer_choice = myanswer_full.split(':')[0]
                myanswer_content = myanswer_full.split(r'[A-D]:')[-1]
                num = questions['序号']
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
                st.write({"text": "解释以下词语或句子的含义 " + str(questions['试题'])})
                res1 = requests.post(ai_url, data=json.dumps({"text": "解释以下词语或句子的含义" + str(questions['试题'])}))
                return res1


            with col2:
                with st.container():
                    if st.button('解析'):
                        st.markdown(questions['解析'])
                        for i in questions['选项']:
                            st.text(i)
                            st.write(get_explain(i))
                if st.button('AI helper'):
                    st.markdown('建设中')

    with tab2:
        st.markdown('This is a new day. --- That **bird** is sitting on the tree and singing.')
if __name__ == '__main__':
    main()



        # st.markdown(ai_helper(questions['答案']))