import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

df = pd.read_csv("vhi_final.csv")
df.replace(-1, pd.NA, inplace=True)
df.dropna(inplace=True)

parameters = ['VCI', 'TCI', 'VHI']
regions = {
    1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська",
    6: "Закарпатська", 7: "Запорізька", 8: "Івано-Франківська", 9: "Київ", 10: "Київська",
    11: "Кіровоградська", 12: "Луганська", 13: "Львівська", 14: "Миколаївська", 15: "Одеська",
    16: "Полтавська", 17: "Рівненська", 18: "Республіка Крим", 19: "Севастополь", 20: "Сумська",
    21: "Тернопільська", 22: "Харківська", 23: "Херсонська", 24: "Хмельницька", 25: "Черкаська",
    26: "Чернівецька", 27: "Чернігівська"
}

default_param = parameters[0]
default_week_range = (1, 52)
default_year_range = (int(df["Year"].min()), int(df["Year"].max()))

if "param" not in st.session_state:
    st.session_state.param = default_param
if "week_range" not in st.session_state:
    st.session_state.week_range = default_week_range
if "year_range" not in st.session_state:
    st.session_state.year_range = default_year_range
if "sort_order" not in st.session_state:
    st.session_state.sort_order = None

def reset_filters():
    st.session_state.param = default_param
    st.session_state.week_range = default_week_range
    st.session_state.year_range = default_year_range
    st.session_state.sort_order = None
    st.rerun()

def set_sort_order(order):
    if st.session_state.sort_order == order:
        st.session_state.sort_order = None
    else:
        st.session_state.sort_order = order

col1, col2 = st.columns([1, 3])

with col1:
    st.session_state.param = st.selectbox("Оберіть параметр:", parameters, index=parameters.index(st.session_state.param))
    st.session_state.region = st.selectbox("Оберіть область:", list(regions.values()))

    st.session_state.week_range = st.slider("Оберіть інтервал тижнів:", 1, 52, st.session_state.week_range)
    st.session_state.year_range = st.slider("Оберіть інтервал років:", int(df["Year"].min()), int(df["Year"].max()), st.session_state.year_range)

    st.checkbox("Сортувати за зростанням", value=st.session_state.sort_order == "asc", on_change=set_sort_order, args=("asc",))
    st.checkbox("Сортувати за спаданням", value=st.session_state.sort_order == "desc", on_change=set_sort_order, args=("desc",))

    if st.button("Скинути фільтри"):
        reset_filters()

region_id = next(key for key, value in regions.items() if value == st.session_state.region)
filtered_df = df[(df["Year"].between(*st.session_state.year_range)) & (df["Week"].between(*st.session_state.week_range))]
region_df = filtered_df[filtered_df["id"] == region_id]

if st.session_state.sort_order == "asc":
    region_df = region_df.sort_values(by=st.session_state.param, ascending=True)
elif st.session_state.sort_order == "desc":
    region_df = region_df.sort_values(by=st.session_state.param, ascending=False)

with col2:

    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Графік Порівнянь"])

    with tab1:
        st.write("### Дані для обраного регіону")
        st.dataframe(region_df)
    with tab2:
        st.write(f"### Часовий ряд для {st.session_state.param} у {st.session_state.region}")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=filtered_df, x="Year", y=st.session_state.param, label=st.session_state.region, ax=ax)
        ax.set(xlabel="Year", ylabel=st.session_state.param, title=f"Time Series of {st.session_state.param} for {st.session_state.region}")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
    with tab3:
        st.write(f"### Порівняння середніх значень {st.session_state.param} за вибраний діапазон")
        avg_selected_region = filtered_df[filtered_df["id"] == region_id][st.session_state.param].mean()
        avg_other_regions = filtered_df[filtered_df["id"] != region_id].groupby("id")[
            st.session_state.param].mean().reset_index()
        avg_other_regions["region"] = avg_other_regions["id"].map(regions)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=avg_other_regions, x="region", y=st.session_state.param, color="gray", ax=ax)
        ax.axhline(avg_selected_region, color="red", linestyle="--", label=st.session_state.region)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_title(f"Середні значення {st.session_state.param} для регіонів")
        ax.legend()
        st.pyplot(fig)