import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sistema Bancario Argentino - BCRA",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Sistema Bancario Argentino - BCRA")
st.markdown("**Deploy Test - Verificando conexión**")

st.success("✅ Deploy funcionando correctamente!")
st.info("🚀 Aplicación conectada a Streamlit Cloud")

# Test básico de imports
try:
    from BCRA_.tools import procesar_datos_bcra_con_nombres
    st.success("✅ Import tools.py - OK")
except Exception as e:
    st.error(f"❌ Error import tools: {e}")

try:
    from BCRA_.tabs import tab_resumen
    st.success("✅ Import tabs - OK")
except Exception as e:
    st.error(f"❌ Error import tabs: {e}")

try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    st.success("✅ Librerías de gráficos - OK")
except Exception as e:
    st.error(f"❌ Error librerías: {e}")

st.markdown("---")
st.markdown("### 🎯 Próximo paso: Activar aplicación completa")
st.markdown("Una vez que este test funcione, cambiaremos al app.py completo")