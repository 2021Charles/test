# https://github.com/Sven-Bo/streamlit-sales-dashboard.git
# @Email:  contact@pythonandvba.com# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="ESG Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    # df = pd.read_excel(
    #     io="supermarkt_sales.xlsx",
    #     engine="openpyxl",
    #     sheet_name="Sales",
    #     skiprows=3,
    #     usecols="B:R",
    #     nrows=1000,
    # )
    df = pd.read_csv(
        "dummy_esg_data.csv",
        # engine="openpyxl",
        # sheet_name="Sales",
        # skiprows=3,
        # usecols="B:R",
        # nrows=1000,
    )
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df


df = get_data_from_excel()
options_id = df['ID'].unique()

st.sidebar.header("Please Filter Here:")
select_id = st.sidebar.selectbox(
    "Select Home ID",
    options_id
)

options_year = df['date'].dt.year.unique() #연도
options_month = df['date'].dt.month.unique() #월

select_year = st.sidebar.selectbox(
    "Select Year",
    options_year
)
#
# # value_initial = ['all']
# value_initial.extend(list(options_month))

select_month = st.sidebar.selectbox(
    "Select Month",
    options_month
    # value_initial
)

print(f'id :{select_id} {type(select_id)} year:{select_year} {type(select_year)} month:{select_month}')


add = '서울시 서초구 바우뫼로 38'
phone = '010-1234-5678'

df_selection = df.query("ID == @select_id & date.dt.year == @select_year & date.dt.month == @select_month")
df_selection_year_total = df.query("ID == @select_id & date.dt.year == @select_year")

# TOP KPI's
df_total = df.query("date.dt.year == @select_year & date.dt.month == @select_month")
average_rating = round(df_selection["meter"].mean() / df_total["meter"].mean(),1) * 10
star_rating = ":star:" * int(round(average_rating, 0))
average_consumption = round(df_selection["meter"].mean(),2)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader(f'Home ID : {select_id}')
    st.text(f"위치 : {add}")
    st.text(f"연락처 : {phone}")

with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("평균소비전력")
    st.subheader(f"{average_consumption}  KW/h ")


st.markdown("""---""")

# ---- MAINPAGE ----
st.title(":bar_chart: ESG Data Dashboard")

meter_by_date = df_selection.groupby(by=["date"]).sum()[["meter"]]
meter_by_month = df_selection_year_total.groupby(by=["date"])['meter'].sum().resample('1M').agg(['sum','mean'])

# 일간데이터(월별)
fig_product_date = px.bar(
    meter_by_date,
    y="meter",
    x=meter_by_date.index,
    labels={'meter':'사용량','date':''},
    orientation="v",
    title="<b>사용량(일)</b>",
    color_discrete_sequence=["#0083B8"] * len(meter_by_date),
    template="plotly_white",
)
fig_product_date.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


#년간데이터(총사용량)
fig_product_month_sum = px.bar(
    meter_by_month,
    y = 'sum',
    x=meter_by_month.index,
    labels={'sum':'사용량','date':''},
    orientation="v",
    title="<b>총사용량(월)</b>",
    color_discrete_sequence=["#0083B8"] * len(meter_by_month),
    template="plotly_white",
)
fig_product_month_sum.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#년간데이터(평균사용량)
fig_product_month_mean = px.bar(
    meter_by_month,
    y = 'mean',
    x=meter_by_month.index,
    labels={'mean':'사용량','date':''},
    orientation="v",
    title="<b>평균사용량(월)</b>",
    color_discrete_sequence=["#0083B8"] * len(meter_by_month),
    template="plotly_white",
)
fig_product_month_mean.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Group으로 표현하고자할때...여기서는 scale차가커서 하나가 작아보여 따로빠로 표시하기로..
# fig_product_month = go.Figure(data=[
#     go.Bar(name='총사용량', x=meter_by_month.index, y= meter_by_month['sum']),
#     go.Bar(name='평균사용량', x=meter_by_month.index, y= meter_by_month['mean'])
# ])

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_date, use_container_width=True)
right_column.plotly_chart(fig_product_month_mean, use_container_width=True)
right_column.plotly_chart(fig_product_month_sum, use_container_width=True)




# ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
#
# st.markdown(hide_st_style, unsafe_allow_html=True)


#
# st.title("제목출력")
# st.text("Text출력")
# st.header("Header출력")
# st.subheader("Subheader출력")
# st.markdown('___')
#
# st.success("성공했을때")
# st.warning("경고할때")
# st.info("정보표시")
# st.error("에러표시")
# st.exception("예외상황표시")

