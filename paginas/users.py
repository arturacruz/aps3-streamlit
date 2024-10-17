from functions import make_request, handle_errors
import streamlit as st

if "error" in st.session_state:
    handle_errors(st.session_state.error)

st.header("Usuários")

@st.dialog("Edite o usuário")
def edit_user(user: dict) -> None:
    nome = st.text_input("Nome:", value=user['nome'])
    cpf = st.text_input("CPF:", value=user['cpf'])
    data_nasc = st.text_input("Data de nascimento", value=user['data-de-nascimento'])

    data: dict = {
        "nome": nome,
        "cpf": cpf,
        "data-de-nascimento": data_nasc
    }

    if st.button("Atualizar"):
        err = make_request("usuarios/" + user['_id'], method="PUT", data=data)
        if isinstance(err, Exception):
            st.session_state.error = err
        st.rerun()

@st.dialog("Apagar usuário")
def delete_user(user: dict) -> None:
    st.write("Tem certeza de que quer apagar esse usuário?")
    st.write("Essa ação não pode ser desfeita.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancelar", type="primary"):
            st.rerun()
    with col2:
        if st.button("Apagar"):
            err = make_request("usuarios/" + user['_id'], method="DELETE")
            if isinstance(err, Exception):
                st.session_state.error = err
            st.rerun()


def write_user(user: dict) -> None:
    col1, col2, col3, col4, col5 = st.columns([0.2, 0.15, 0.25, 0.2, 0.2])
    with col1:
        st.write(user['_id'])
    with col2:
        st.write(user['nome'])
    with col3:
        st.write(user['data-de-nascimento'])
    with col4:
        st.write(user['cpf'])
    with col5:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            if st.button("🖊️", key=f"edit_{user['_id']}", use_container_width=True): edit_user(user)
        with subcol2:
            if st.button("🗑️", key=f"erase_{user['_id']}", use_container_width=True): delete_user(user)

@st.dialog("Criar novo usuário")
def add_user() -> None:
    nome = st.text_input("Nome:")
    cpf = st.text_input("CPF:")
    data_nasc = st.text_input("Data de nascimento:")

    data: dict = {
        "nome": nome,
        "cpf": cpf,
        "data-de-nascimento": data_nasc
    }
    if st.button("Criar"):
        err = make_request("usuarios", method="POST", data=data)
        if isinstance(err, Exception):
            st.session_state.error = err
        st.rerun()

def list_users(id: int | str = -1) -> None:
    users = make_request("usuarios")

    if isinstance(users, Exception):
        st.session_state.error = users
        return 
    if users == None:
        return
    with st.container(height=500):

        fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns([0.2, 0.15, 0.25, 0.2, 0.2])
        with fcol1: 
            st.write("#### ID")
        with fcol2: 
            st.write("#### Nome")
        with fcol3: 
            st.write("#### Nascimento")
        with fcol4: 
            st.write("#### CPF")
        with fcol5:
            if st.button("Adicionar", use_container_width=True):
                add_user()

        if id == -1:
            for user in users['usuarios']:
                write_user(user)
            return

        user = make_request("usuarios/" + str(id))
        if isinstance(user, Exception):
            st.session_state.error = user
            return
        if user == None: return
        write_user(user["usuario"])

user_id: str = st.text_input("Procure um usuário por ID")
        
if user_id:
    list_users(id=user_id)
else:
    list_users()

