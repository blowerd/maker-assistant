import streamlit as st

st.set_page_config(page_title="Project Kanban")
st.title("Project Kanban Board")
st.write("So many projects, so little time. See them all here!")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("## Backog")
    b1 = st.container(border = True)
    b1.markdown("## This is a triumph")
with col2:
    st.markdown("## Started")
    b2 = st.container(border = True)
    b2.write("I'm making a note here, huge success!")
with col3:
    st.markdown("## Blocked")
    b3 = st.container(border = True)
    with b3:
        if st.button("Delete me"):
            pass
with col4:
    st.markdown("## Done")
    b4 = st.container(border = True)
    with b4: 
        st.write("Candy!")