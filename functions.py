import requests
import streamlit as st

BASE_URL = "https://aps-3-flask-rest-mongo-marcelopenas.onrender.com/"
def make_request(endpoint: str, method:str="GET", data=None) -> None | Exception | dict:
    url: str = BASE_URL + endpoint
    response: requests.Response
    
    try:
        match method:
            case "GET":
                response = requests.get(url)
            case "POST":
                response = requests.post(url, json=data)
            case "PUT":
                response = requests.put(url, json=data)
            case "DELETE":
                response = requests.delete(url)
            case _:
                st.error("Invalid HTTP method.")
                return

        match response.status_code:
            case 200:
                return response.json()
            case 201:
                return response.json()
            case _:
                return

    except Exception as err:
        print(err)
        st.error(f"Erro {err}.")
        return err

@st.dialog("Erro")
def handle_errors(err) -> None:

    st.title("ERRO", str(err))
    if st.button("OK"):
        del st.session_state.error
        st.rerun()

