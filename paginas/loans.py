from functions import make_request, handle_errors
import streamlit as st

if "error" in st.session_state:
    handle_errors(st.session_state.error)

st.header("Empréstimos")

@st.dialog("Apagar empréstimo")
def delete_emprestimo(emprestimo: dict) -> None:
    st.write("Tem certeza de que quer apagar esse empréstimo?")
    st.write("Essa ação não pode ser desfeita.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancelar", type="primary"):
            st.rerun()
    with col2:
        if st.button("Apagar"):
            # TODO: delete REQUEST
            err = make_request("emprestimos/" + emprestimo['_id'], method="DELETE")
            if isinstance(err, Exception):
                st.session_state.error = err
            st.rerun()


def write_emprestimo(emprestimo: dict) -> None:
    col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
    with col1:
        st.write(emprestimo['_id'])
    with col2:
        st.write(emprestimo['usuario'])
    with col3:
        st.write(emprestimo['bike'])
    with col4:
        if st.button("🗑️", key=f"erase_{emprestimo['_id']}", use_container_width=True): delete_emprestimo(emprestimo)

@st.dialog("Criar novo empréstimo")
def add_emprestimo() -> None:
    user = st.text_input("ID Usuário:")
    bike = st.text_input("ID Bike:")

    data: dict = {
        "usuario": user,
        "bike": bike,
    }

    if st.button("Criar"):
        err = make_request("emprestimos/usuarios/" + user + "/bikes/" + bike, method="POST", data=data)
        if isinstance(err, Exception):
            st.session_state.error = err
        st.rerun()

def list_emprestimos(id: int | str = -1) -> None:
    emprestimos = make_request("emprestimos")

    if isinstance(emprestimos, Exception):
        st.session_state.error = emprestimos
        return 
    if emprestimos == None:
        return
    with st.container(height=500):

        fcol1, fcol2, fcol3, fcol4 = st.columns([0.25, 0.25, 0.25, 0.25])
        with fcol1: 
            st.write("#### ID")
        with fcol2: 
            st.write("#### ID Usuário")
        with fcol3: 
            st.write("#### ID Bike")
        with fcol4:
            if st.button("Adicionar", use_container_width=True):
                add_emprestimo()

        if id == -1:
            for emprestimo in emprestimos['emprestimos']:
                write_emprestimo(emprestimo)
            return

        emprestimo = make_request("emprestimos/" + str(id))
        if isinstance(emprestimo, Exception):
            st.session_state.error = emprestimo
            return
        if emprestimo == None: return
        write_emprestimo(emprestimo["emprestimo"])


emprestimo_id: str = st.text_input("Procure um empréstimo por ID")
        
if emprestimo_id:
    list_emprestimos(id=emprestimo_id)
else:
    list_emprestimos()

