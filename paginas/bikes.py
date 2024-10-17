from functions import make_request, handle_errors
import streamlit as st

if "error" in st.session_state:
    handle_errors(st.session_state.error)

st.header("Bikes")

@st.dialog("Edite a bike")
def edit_bike(bike: dict) -> None:
    cidade = st.text_input("Cidade:", value=bike['cidade'])
    marca = st.text_input("Marca:", value=bike['marca'])
    modelo = st.text_input("Modelo:", value=bike['modelo'])

    data: dict = {
        "cidade": cidade,
        "marca": marca,
        "modelo": modelo,
    }

    if st.button("Atualizar"):
        err = make_request("bikes/" + bike['_id'], method="PUT", data=data)
        if isinstance(err, Exception):
            st.session_state.error = err
        st.rerun()

@st.dialog("Apagar usuario")
def delete_bike(bike: dict) -> None:
    st.write("Tem certeza de que quer apagar essa bike?")
    st.write("Essa ação não pode ser desfeita.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancelar", type="primary"):
            st.rerun()
    with col2:
        if st.button("Apagar"):
            # TODO: delete REQUEST
            err = make_request("bikes/" + bike['_id'], method="DELETE")
            if isinstance(err, Exception):
                st.session_state.error = err
            st.rerun()


def write_bike(bike: dict) -> None:
    col1, col2, col3, col4, col5, col6 = st.columns([0.2, 0.15, 0.15, 0.15, 0.15, 0.2])
    with col1:
        st.write(bike['_id'])
    with col2:
        st.write(bike['cidade'])
    with col3:
        st.write(bike['marca'])
    with col4:
        st.write(bike['modelo'])
    with col5:
        st.write(bike['status'])
    with col6:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            if st.button("🖊️", key=f"edit_{bike['_id']}", use_container_width=True): edit_bike(bike)
        with subcol2:
            if st.button("🗑️", key=f"erase_{bike['_id']}", use_container_width=True): delete_bike(bike)

@st.dialog("Criar nova bike")
def add_bike() -> None:
    cidade = st.text_input("Cidade:")
    marca = st.text_input("Marca:")
    modelo = st.text_input("Modelo:")

    data: dict = {
        "cidade": cidade,
        "marca": marca,
        "modelo": modelo,
    }
    if st.button("Criar"):
        err = make_request("bikes", method="POST", data=data)
        if isinstance(err, Exception):
            st.session_state.error = err
        st.rerun()

def list_bikes(id: int | str = -1) -> None:
    bikes = make_request("bikes")

    if isinstance(bikes, Exception):
        st.session_state.error = bikes
        return 
    if bikes == None:
        return
    with st.container(height=500):

        fcol1, fcol2, fcol3, fcol4, fcol5, fcol6 = st.columns([0.2, 0.15, 0.15, 0.15, 0.15, 0.2])
        with fcol1: 
            st.write("#### ID")
        with fcol2: 
            st.write("#### Cidade")
        with fcol3: 
            st.write("#### Marca")
        with fcol4: 
            st.write("#### Modelo")
        with fcol5: 
            st.write("#### Status")
        with fcol6:
            if st.button("Adicionar", use_container_width=True):
                add_bike()

        if id == -1:
            for bike in bikes['bikes']:
                write_bike(bike)
            return

        bike = make_request("bikes/" + str(id))
        if isinstance(bike, Exception):
            st.session_state.error = bike
            return
        if bike == None: return
        write_bike(bike["bike"])

bike_id: str = st.text_input("Procure uma bike por ID")
        
if bike_id:
    list_bikes(id=bike_id)
else:
    list_bikes()

