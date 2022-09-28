import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

def load_data(s3_path):
    data = pd.read_csv(s3_path)
    return data

def display_app_header(main_txt, sub_txt, is_sidebar=False):
    """
    Code Credit: https://github.com/soft-nougat/dqw-ivves
    function to display major headers at user interface
    :param main_txt: the major text to be displayed
    :param sub_txt: the minor text to be displayed
    :param is_sidebar: check if its side panel or major panel
    :return:
    """
    html_temp = f"""
    <h2 style = "text_align:center; font-weight: bold;"> {main_txt} </h2>
    <p style = "text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html=True)
    else:
        st.markdown(html_temp, unsafe_allow_html=True)

def divider():
    """
    Sub-routine to create a divider for webpage contents
    """
    st.markdown("""---""")

@st.cache
def read_file(s3_path):
    return load_data(s3_path)


def main():
    st.write("""
    # 360-degree customer view usecase
    In this application, we'll see how customer transactions across their different banks are compared.
    Let's start by uploading the sample dataframe from local storage
    """)
    input_help_text = """
    Enter s3 path
    """
    final_message = """
    The data was successfully analyzed
    """
    # s3_path = st.text_input(label='INPUT S3 Path',placeholder="Enter")
    s3_path = st.file_uploader("Upload a file")

    with st.sidebar:
        # st.image(Image.open("../data/image_data/start.png"))
        # st.markdown("**Step 1**")
        st.markdown("**Processing**")
        start_process = st.checkbox(
            label="Start",
            help="Starts the file load"
        )

    if start_process:
        # Fancy Header
        # Slik Wrangler default header
        display_app_header(
            main_txt='FUGAZ Demo Web Application',
            sub_txt='Upload csv file -> Load data -> Return dataframe -> Plot transactions'
        )
        divider()

        if s3_path is not None:
            st.info('Data loaded', icon="ℹ️")

            if st.sidebar.checkbox("Load Data"):
                with st.spinner('Wait for it...'):
                    df = read_file(s3_path)
                    option = st.selectbox('select profile',
                    (df[:500].msisdn.tolist()))
                    df = df[df.msisdn==str(option)]
                    st.dataframe(df)
                    st.success('Dataframe loaded successfully!!!')

            if st.sidebar.checkbox("Plot Account Balances"):
                with st.spinner('Wait for it...'):
                    acc_plot = plt.figure(figsize=(12,6))
                    sns.lineplot(x = "Date", y = "balance",
                                 data = df,hue='bank_name')
                    plt.legend(title='Bank Name')
                    plt.ylabel('Account Balance (x1000000)')
                    plt.xlabel('Date')
                    plt.xticks(rotation=20);
                    st.pyplot(acc_plot)

            if st.sidebar.checkbox("Plot Volume of Outflow"):
                with st.spinner('Wait for it...'):
                    acc_plot = plt.figure(figsize=(12,6))
                    sns.lineplot(x = "Date", y = "vol_of_outflow",
                                 data = df,hue='bank_name')
                    plt.legend(title='Bank Name')
                    plt.ylabel('Volume of Outflow (x1000000)')
                    plt.xlabel('Date')
                    plt.xticks(rotation=20);
                    st.pyplot(acc_plot)

            if st.sidebar.checkbox("Plot Volume of Inflow"):
                with st.spinner('Wait for it...'):
                    acc_plot = plt.figure(figsize=(12,6))
                    sns.lineplot(x = "Date", y = "vol_of_inflow",
                                 data = df,hue='bank_name')
                    plt.legend(title='Bank Name')
                    plt.ylabel('Volume of Inflow (x1000000)')
                    plt.xlabel('Date')
                    plt.xticks(rotation=20);
                    st.pyplot(acc_plot)

if __name__ == '__main__':
    main()
