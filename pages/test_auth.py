import streamlit as st
from philoui.authentication_v2 import AuthenticateWithKey
import yaml
from yaml import SafeLoader




with open('data/credentials.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = AuthenticateWithKey(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
fields = {'Form name':'Forge access key', 'Email':'Email', 'Username':'Username',
            'Password':'Password', 'Repeat password':'Repeat password',
            'Register':' Here • Now ', 'Captcha':'Captcha'}


if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["username"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Access key does not open')
elif st.session_state['authentication_status'] is None:
    authenticator.login('Connect', 'main', fields = fields)
    st.warning('Please use your access key')
    try:
        match = True
        success, access_key, response = authenticator.register_user(data = match, captcha=True, pre_authorization=False, fields = fields)
        if success:
            st.success('Registered successfully')
            st.toast(f'Access key: {access_key}')
            st.write(response)
    except Exception as e:
        st.error(e)
