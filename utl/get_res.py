import requests
import streamlit as st

@st.cache
def get_api(method, url,is_jsonify = True
            ):
    if  method == 'post':
        response = requests.post(url,
                                # proxies={'http':'127.0.0.1:33210'}
                                )
    else:
        response = requests.get(url,
                                # proxies={'http':'127.0.0.1:33210'}
        )
    # print(response.json())
    if response.status_code == 200:
        if is_jsonify:
            return response.json()
        else:
            return response.content
    else:
        raise Exception((f'{response.status_code} error'))