import streamlit as st


BASE_URL = "localhost:8501/"

def init_navigation() -> None:
    pages: list = [
        st.Page("paginas/home.py", icon="🚲", title="BorrowBike"),
        st.Page("paginas/users.py", icon="🚲", title="Usuários"),
        st.Page("paginas/bikes.py", icon="🚲", title="Bikes"),
        st.Page("paginas/loans.py", icon="🚲", title="Empréstimos")
    ]
    nav = st.navigation(pages)
    nav.run()

init_navigation()




