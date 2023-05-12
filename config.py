import streamlit as st

def set_page(name):
    st.set_page_config(
        page_title=name,
        page_icon='🏠',
        layout='wide',
        initial_sidebar_state='collapsed',
        menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': None,
        }
    )
class HIDEN:
    def __init__(self):
        self.hiden_dict = {
        "hide_footer_style" :'''<style>footer {visibility: hidden;}''',
        "hide_menu_style" : '''<style>#MainMenu {visibility: hidden;}</style>'''
        }
    def hiden(self,hide):
        st.markdown(hide, unsafe_allow_html=True)
    def hide(self):
        for k,v in self.hiden_dict.items():
            self.hiden(v)

def setting():
    set_page('home')
    HIDEN().hide()