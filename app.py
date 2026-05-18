# ============================================================
#  METALNATI — Sistema de Control de Inventario
#  Archivo único: app.py
#  Ejecutar: streamlit run app.py
# ============================================================

import streamlit as st
import hashlib
from datetime import datetime, date, timezone
from supabase import create_client, Client

st.set_page_config(
    page_title="MetalNati — Sistema de Control de Inventario",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────

@st.cache_resource
def get_supabase() -> Client:
    try:
        url = st.secrets["SUPA_URL"]
        key = st.secrets["SUPA_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Error al conectar con Supabase: {e}")
        st.info("Verifica que existe el archivo `.streamlit/secrets.toml` con SUPA_URL y SUPA_KEY.")
        st.stop()


# ─────────────────────────────────────────────────────────────
# AUDITORÍA
# ─────────────────────────────────────────────────────────────

def log_action(accion: str, tabla: str, usuario: str, detalle: str = ""):
    try:
        sb = get_supabase()
        sb.table("auditoria").insert({
            "accion":  accion,
            "tabla":   tabla,
            "usuario": usuario,
            "detalle": detalle,
            "fecha":   datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
# ESTILOS GLOBALES — Diseño Corporativo Azul Naval
# ─────────────────────────────────────────────────────────────

def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --navy:       #0f172a;
        --blue:       #1d4ed8;
        --blue-light: #3b82f6;
        --blue-muted: #dbeafe;
        --surface:    #ffffff;
        --bg:         #f1f5f9;
        --border:     #e2e8f0;
        --text-main:  #0f172a;
        --text-muted: #64748b;
        --text-light: #94a3b8;
        --green:      #16a34a;
        --red:        #dc2626;
        --amber:      #d97706;
        --radius:     10px;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }

    #MainMenu, footer, .stDeployButton { display: none !important; }

    .stApp { background: var(--bg) !important; }

    [data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        width: 240px !important;
        min-width: 240px !important;
        background: var(--navy) !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding: 0 !important;
    }

    /* Ocultar botón de colapsar */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Wrapper */
    section[data-testid="stSidebar"] .stButton {
        margin: 0 !important;
        padding: 4px 12px !important;
    }
    section[data-testid="stSidebar"] .stButton > div {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Botón: reset total, sin movimiento en ningún estado */
    section[data-testid="stSidebar"] .stButton button {
        all: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        cursor: pointer !important;
        color: #94a3b8 !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 11px 14px !important;
        border-radius: 8px !important;
        line-height: 1.4 !important;
        transform: none !important;
        position: static !important;
        transition: background 0.15s, color 0.15s !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.07) !important;
        color: #e2e8f0 !important;
        transform: none !important;
        position: static !important;
    }
    section[data-testid="stSidebar"] .stButton button:active,
    section[data-testid="stSidebar"] .stButton button:focus {
        background: rgba(255,255,255,0.07) !important;
        color: #e2e8f0 !important;
        transform: none !important;
        position: static !important;
        top: 0 !important;
        margin: 0 !important;
        padding: 11px 14px !important;
        box-shadow: none !important;
        outline: none !important;
    }
    /* <p> interno que Streamlit centra */
    section[data-testid="stSidebar"] .stButton button p,
    section[data-testid="stSidebar"] .stButton button div,
    section[data-testid="stSidebar"] .stButton button span {
        all: unset !important;
        text-align: left !important;
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: var(--border);
        border-radius: 8px;
        padding: 3px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        color: var(--text-muted) !important;
        padding: 7px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: var(--blue) !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }

    /* ── MÉTRICAS ── */
    [data-testid="metric-container"] {
        background: white !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 18px 20px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        color: var(--text-muted) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        color: var(--text-main) !important;
    }

    /* ── INPUTS ── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-color: var(--border) !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
    }

    /* ── BOTONES ── */
    .stButton > button[kind="primary"] {
        background: var(--blue) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.2px !important;
        transition: background 0.15s !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #1e40af !important;
    }
    .stButton > button[kind="secondary"] {
        border-color: var(--border) !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }

    /* ── EXPANDER ── */
    .streamlit-expanderHeader {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        background: var(--bg) !important;
        border-radius: 6px !important;
    }

    /* ── ALERTAS ── */
    .stAlert {
        border-radius: 8px !important;
        font-size: 13px !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

    /* Expander */
    .streamlit-expanderHeader p,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary {
        color: #475569 !important;
    }

    /* Labels de inputs, selectbox, etc */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    label[data-testid="stWidgetLabel"],
    .stTextInput label, .stSelectbox label,
    .stNumberInput label, .stTextArea label,
    .stDateInput label, .stFileUploader label {
        color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# COMPONENTES UI REUTILIZABLES
# ─────────────────────────────────────────────────────────────

def page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="
        padding: 22px 0 18px;
        margin-bottom: 20px;
        border-bottom: 1px solid #e2e8f0;
    ">
        <h1 style="
            font-family: 'Syne', sans-serif;
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.3px;
        ">{title}</h1>
        {'<p style="font-size:12px;color:#64748b;margin:3px 0 0;font-weight:400;">' + subtitle + '</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def badge(text: str, color: str = "gray") -> str:
    palettes = {
        "green":  ("#dcfce7", "#15803d"),
        "amber":  ("#fef9c3", "#92400e"),
        "red":    ("#fee2e2", "#b91c1c"),
        "blue":   ("#dbeafe", "#1d4ed8"),
        "gray":   ("#f1f5f9", "#475569"),
        "navy":   ("#1e3a5f", "#bfdbfe"),
    }
    bg, fg = palettes.get(color, palettes["gray"])
    return (
        f'<span style="background:{bg};color:{fg};font-size:10px;font-weight:700;'
        f'padding:3px 9px;border-radius:20px;display:inline-block;letter-spacing:0.3px;">'
        f'{text}</span>'
    )


def empty_state(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 48px 24px;
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-top: 8px;
    ">
        <div style="font-size: 36px; margin-bottom: 12px; opacity: 0.5;">{icon}</div>
        <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;
                    color:#0f172a;margin-bottom:4px;">{title}</div>
        {'<div style="font-size:12px;color:#64748b;">' + subtitle + '</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def section_card_open(title: str = ""):
    if title:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;border:1px solid #e2e8f0;
                    padding:20px 22px;margin-bottom:16px;">
            <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
                        color:#0f172a;margin-bottom:14px;letter-spacing:-0.2px;">{title}</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:white;border-radius:12px;border:1px solid #e2e8f0;
                    padding:20px 22px;margin-bottom:16px;">
        """, unsafe_allow_html=True)


def section_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def info_banner(text: str, tipo: str = "info"):
    colors = {
        "info":    ("#eff6ff", "#1d4ed8", "#bfdbfe"),
        "warning": ("#fffbeb", "#92400e", "#fde68a"),
        "success": ("#f0fdf4", "#15803d", "#bbf7d0"),
    }
    bg, fg, border = colors.get(tipo, colors["info"])
    st.markdown(f"""
    <div style="background:{bg};border:1px solid {border};border-radius:8px;
                padding:10px 14px;margin-bottom:14px;font-size:12px;color:{fg};font-weight:500;">
        {text}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────

SYSTEM_USERS = {
    "admin": {
        "hash":   hashlib.sha256("metalnati2024".encode()).hexdigest(),
        "nombre": "Administrador",
        "rol":    "admin",
    },
    "almacen": {
        "hash":   hashlib.sha256("almacen123".encode()).hexdigest(),
        "nombre": "Almacenero",
        "rol":    "almacenero",
    },
}


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def render_login():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(145deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%) !important;
    }
    section[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 1.1, 1])
    with col_center:
        st.markdown("<div style='height:64px'></div>", unsafe_allow_html=True)

        # Logo
        st.markdown("""
        <div style="text-align:center;margin-bottom:36px;">
            <div style="
                display:inline-flex;align-items:center;justify-content:center;
                width:60px;height:60px;
                background:linear-gradient(135deg,#3b82f6,#1d4ed8);
                border-radius:16px;margin-bottom:16px;
                box-shadow:0 8px 32px rgba(59,130,246,0.35);
            ">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
                     stroke="white" stroke-width="2.2" stroke-linecap="round">
                    <rect x="2" y="7" width="20" height="14" rx="2"/>
                    <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
                    <line x1="12" y1="12" x2="12" y2="16"/>
                    <line x1="10" y1="14" x2="14" y2="14"/>
                </svg>
            </div>
            <h1 style="
                font-family:'Syne',sans-serif;
                font-size:26px;font-weight:800;
                color:#ffffff;margin:0;letter-spacing:-0.5px;
            ">Metalnati</h1>
            <p style="font-size:12px;color:#64748b;margin:4px 0 0;font-weight:400;">
                Sistema de Control de Inventario
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card de login
        st.markdown("""
        <div style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.09);
            border-radius:16px;
            padding:32px;
            backdrop-filter:blur(12px);
        ">
        """, unsafe_allow_html=True)

        tab_sistema, tab_supabase = st.tabs(["Usuario del sistema", "Cuenta Supabase"])

        # ── Tab 1: Usuarios del sistema (sin cambios) ──────────────
        with tab_sistema:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            usuario  = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="login_user")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_pass")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("Ingresar al sistema", type="primary", use_container_width=True, key="btn_login_system"):
                if usuario and password:
                    user_data = SYSTEM_USERS.get(usuario.strip().lower())
                    if user_data and user_data["hash"] == _hash(password):
                        st.session_state.authenticated = True
                        st.session_state.auth_method   = "system"
                        st.session_state.user_name     = user_data["nombre"]
                        st.session_state.user_rol      = user_data["rol"]
                        st.session_state.user_email    = usuario
                        log_action("login", "auth", usuario, f"Login sistema: {usuario}")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos.")
                else:
                    st.warning("Completa todos los campos.")

        # ── Tab 2: Cuenta Supabase — login + registro ──────────────
        with tab_supabase:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            sub_login, sub_registro = st.tabs(["Iniciar sesión", "Crear cuenta"])

            # Sub-tab: Iniciar sesión
            with sub_login:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                email     = st.text_input("Correo electrónico", placeholder="correo@empresa.com", key="supa_email")
                supa_pass = st.text_input("Contraseña", type="password", placeholder="••••••••", key="supa_pass")
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                if st.button("Ingresar con Supabase", type="primary", use_container_width=True, key="btn_login_supa"):
                    if email and supa_pass:
                        try:
                            sb       = get_supabase()
                            response = sb.auth.sign_in_with_password({"email": email, "password": supa_pass})
                            if response.user:
                                st.session_state.authenticated = True
                                st.session_state.auth_method   = "supabase"
                                st.session_state.user_name     = response.user.email.split("@")[0].title()
                                st.session_state.user_rol      = "admin"
                                st.session_state.user_email    = response.user.email
                                st.session_state.supa_session  = response.session
                                log_action("login", "auth", email, f"Login Supabase: {email}")
                                st.rerun()
                            else:
                                st.error("Credenciales incorrectas.")
                        except Exception as e:
                            st.error(f"Error de autenticación: {str(e)}")
                    else:
                        st.warning("Completa todos los campos.")

            # Sub-tab: Crear cuenta
            with sub_registro:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                reg_email    = st.text_input("Correo electrónico", placeholder="correo@empresa.com", key="reg_email")
                reg_pass     = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres", key="reg_pass")
                reg_pass2    = st.text_input("Confirmar contraseña", type="password", placeholder="Repite la contraseña", key="reg_pass2")
                st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

                if st.button("Crear cuenta", type="primary", use_container_width=True, key="btn_register"):
                    # Validaciones
                    if not reg_email or not reg_pass or not reg_pass2:
                        st.warning("Completa todos los campos.")
                    elif "@" not in reg_email or "." not in reg_email.split("@")[-1]:
                        st.error("Ingresa un correo electrónico válido.")
                    elif len(reg_pass) < 6:
                        st.error("La contraseña debe tener al menos 6 caracteres.")
                    elif reg_pass != reg_pass2:
                        st.error("Las contraseñas no coinciden.")
                    else:
                        try:
                            sb       = get_supabase()
                            response = sb.auth.sign_up({"email": reg_email, "password": reg_pass})

                            # Supabase puede requerir confirmación de email o no
                            if response.user:
                                # Si la sesión ya está activa (email confirm deshabilitado en Supabase)
                                if response.session:
                                    st.session_state.authenticated = True
                                    st.session_state.auth_method   = "supabase"
                                    st.session_state.user_name     = response.user.email.split("@")[0].title()
                                    st.session_state.user_rol      = "admin"
                                    st.session_state.user_email    = response.user.email
                                    st.session_state.supa_session  = response.session
                                    log_action("register", "auth", reg_email, f"Registro Supabase: {reg_email}")
                                    st.success("✅ Cuenta creada. ¡Bienvenido!")
                                    st.rerun()
                                else:
                                    # Supabase envió un correo de confirmación
                                    st.markdown("""
                                    <div style="
                                        background: #f0fdf4;
                                        border: 1px solid #bbf7d0;
                                        border-radius: 10px;
                                        padding: 16px 18px;
                                        margin-top: 8px;
                                    ">
                                        <div style="font-size:14px;font-weight:700;color:#15803d;margin-bottom:4px;">
                                            ✅ Cuenta creada exitosamente
                                        </div>
                                        <div style="font-size:12px;color:#166534;">
                                            Revisa tu bandeja de entrada y confirma tu correo
                                            <b>{}</b> para poder iniciar sesión.
                                        </div>
                                    </div>
                                    """.format(reg_email), unsafe_allow_html=True)
                                    log_action("register", "auth", reg_email, f"Registro pendiente confirmación: {reg_email}")
                            else:
                                st.error("No se pudo crear la cuenta. Intenta con otro correo.")
                        except Exception as e:
                            err_msg = str(e)
                            # Mensajes de error más amigables
                            if "already registered" in err_msg or "User already registered" in err_msg:
                                st.error("Este correo ya está registrado. Inicia sesión en la pestaña anterior.")
                            elif "invalid email" in err_msg.lower():
                                st.error("El correo electrónico no es válido.")
                            elif "password" in err_msg.lower():
                                st.error("La contraseña no cumple los requisitos de seguridad.")
                            else:
                                st.error(f"Error al registrar: {err_msg}")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;font-size:11px;color:#334155;margin-top:20px;">
            Metalnati © 2026 · Ingeniería Industrial
        </p>
        """, unsafe_allow_html=True)


def logout():
    if st.session_state.get("auth_method") == "supabase":
        try:
            get_supabase().auth.sign_out()
        except Exception:
            pass
    log_action("logout", "auth", st.session_state.get("user_email", ""), "Sesión cerrada")
    for key in ["authenticated", "auth_method", "user_name", "user_rol", "user_email", "supa_session"]:
        st.session_state.pop(key, None)
    st.rerun()


# ─────────────────────────────────────────────────────────────
# SIDEBAR / NAVEGACIÓN
# ─────────────────────────────────────────────────────────────

PAGES = [
    {"key": "dashboard",   "label": "Dashboard",          "icon": "🏠", "section": "PRINCIPAL"},
    {"key": "movimientos", "label": "Movimientos",         "icon": "🔄", "section": "GESTIÓN"},
    {"key": "productos",   "label": "Productos",           "icon": "📦", "section": "GESTIÓN"},
    {"key": "categorias",  "label": "Categorías",          "icon": "🏷️", "section": "GESTIÓN"},
    {"key": "proveedores", "label": "Proveedores",         "icon": "🏢", "section": "GESTIÓN"},
    {"key": "ordenes",     "label": "Órdenes de Compra",   "icon": "📋", "section": "GESTIÓN"},
    {"key": "operaciones", "label": "Operaciones",         "icon": "⚙️", "section": "GESTIÓN"},
]


def render_sidebar() -> str:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding:22px 18px 16px;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="
                    width:34px;height:34px;
                    background:linear-gradient(135deg,#3b82f6,#1d4ed8);
                    border-radius:9px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow:0 4px 12px rgba(59,130,246,0.3);
                    flex-shrink:0;
                ">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none"
                         stroke="white" stroke-width="2.2" stroke-linecap="round">
                        <rect x="2" y="7" width="20" height="14" rx="2"/>
                        <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
                    </svg>
                </div>
                <div>
                    <div style="
                        font-family:'Syne',sans-serif;
                        font-size:15px;font-weight:800;
                        color:#f8fafc;letter-spacing:-0.3px;
                    ">Metalnati</div>
                    <div style="font-size:10px;color:#475569;margin-top:0px;">Inventario</div>
                </div>
            </div>
        </div>
        <div style="height:1px;background:rgba(255,255,255,0.06);margin:0 14px 10px;"></div>
        """, unsafe_allow_html=True)

        # Usuario
        nombre   = st.session_state.get("user_name", "Usuario")
        rol      = st.session_state.get("user_rol", "")
        initials = "".join([w[0].upper() for w in nombre.split()[:2]])
        st.markdown(f"""
        <div style="
            margin:0 12px 14px;
            padding:10px 12px;
            background:rgba(255,255,255,0.05);
            border-radius:9px;
            display:flex;align-items:center;gap:10px;
        ">
            <div style="
                width:30px;height:30px;border-radius:50%;
                background:linear-gradient(135deg,#3b82f6,#1d4ed8);
                display:flex;align-items:center;justify-content:center;
                font-size:11px;font-weight:800;color:white;flex-shrink:0;
            ">{initials}</div>
            <div>
                <div style="font-size:12px;font-weight:600;color:#e2e8f0;">{nombre}</div>
                <div style="font-size:10px;color:#475569;text-transform:capitalize;">{rol}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navegación
        current_section = None
        current_page = st.session_state.current_page
        for page in PAGES:
            if page["section"] != current_section:
                current_section = page["section"]
                st.markdown(f"""
                <div style="padding:16px 16px 6px;font-size:9px;font-weight:700;
                            color:#334155;letter-spacing:1.2px;text-transform:uppercase;">
                {current_section}</div>
                """, unsafe_allow_html=True)

            is_active = current_page == page["key"]
            icon = page.get("icon", "")
            if is_active:
                st.markdown(f"""
                <div style="padding:4px 12px;">
                  <div style="padding:11px 14px;background:rgba(59,130,246,0.18);
                              border-radius:8px;border-left:3px solid #3b82f6;
                              font-size:13px;font-weight:600;color:#93c5fd;
                              display:flex;align-items:center;gap:10px;">
                    <span>{icon}</span><span>{page['label']}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {page['label']}", key=f"nav_{page['key']}",
                              use_container_width=True):
                    st.session_state.current_page = page["key"]
                    st.rerun()

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='height:1px;background:rgba(255,255,255,0.06);margin:0 14px 8px;'></div>",
                    unsafe_allow_html=True)
        if st.button("🚪  Cerrar sesión", use_container_width=True, key="btn_logout"):
            logout()

    return st.session_state.current_page


# ─────────────────────────────────────────────────────────────
# VISTA: DASHBOARD
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# VISTA: DASHBOARD  (reemplaza la función render_dashboard completa)
# ─────────────────────────────────────────────────────────────

def render_dashboard():
    import plotly.graph_objects as go
    from collections import defaultdict

    page_header("Dashboard", "Resumen ejecutivo del inventario en tiempo real")
    sb = get_supabase()

    # ── Cargar datos ──────────────────────────────────────────
    try:
        prods_all          = sb.table("producto").select("nombre,stock_actual,stock_minimo,unidad,id_categoria,categoria(nombre)").execute().data or []
        total_productos    = len(prods_all)
        stock_critico      = sum(1 for p in prods_all if (p["stock_actual"] or 0) < (p["stock_minimo"] or 0))
        ordenes_pendientes = sb.table("orden_compra").select("id", count="exact").eq("estado", "pendiente").execute().count or 0
        today              = date.today().isoformat()
        movimientos_hoy    = sb.table("movimiento").select("id", count="exact").gte("fecha", f"{today}T00:00:00").execute().count or 0
    except Exception as e:
        st.error(f"Error cargando datos del dashboard: {e}")
        prods_all = []
        total_productos = stock_critico = ordenes_pendientes = movimientos_hoy = 0

    # ── KPIs ──────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    def kpi_card(col, label, value, sub, accent, value_color="#0f172a"):
        with col:
            st.markdown(f"""
            <div style="
                background: #ffffff;
                border-radius: 14px;
                border: 1px solid #e2e8f0;
                border-top: 4px solid {accent};
                padding: 22px 24px 20px;
                min-height: 110px;
            ">
                <div style="
                    font-size: 11px;
                    font-weight: 700;
                    color: #64748b;
                    text-transform: uppercase;
                    letter-spacing: 0.8px;
                    margin-bottom: 10px;
                ">{label}</div>
                <div style="
                    font-family: 'Syne', sans-serif;
                    font-size: 38px;
                    font-weight: 800;
                    color: {value_color};
                    line-height: 1;
                    margin-bottom: 6px;
                ">{value}</div>
                <div style="
                    font-size: 11px;
                    color: #94a3b8;
                    font-weight: 400;
                ">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    kpi_card(col1, "Total Productos",     total_productos,    "productos registrados", "#3b82f6")
    kpi_card(col2, "Stock Crítico",       stock_critico,      "productos bajo mínimo",
             "#dc2626" if stock_critico > 0 else "#16a34a",
             "#dc2626" if stock_critico > 0 else "#16a34a")
    kpi_card(col3, "Órdenes Pendientes",  ordenes_pendientes, "por recibir",           "#f59e0b")
    kpi_card(col4, "Movimientos Hoy",     movimientos_hoy,    "entradas y salidas",    "#10b981")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if stock_critico > 0:
        st.markdown(f"""
        <div style="
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-radius: 10px;
            padding: 12px 18px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #92400e;
            font-weight: 500;
        ">
            ⚠️ Hay <b>{stock_critico} producto{'s' if stock_critico > 1 else ''}</b>
            con stock por debajo del mínimo. Revisa el gráfico de alertas a continuación.
        </div>
        """, unsafe_allow_html=True)

    # ── Fila 1: Movimientos 7 días + Donut órdenes ───────────
    col_g1, col_g2 = st.columns([3, 2], gap="medium")

    with col_g1:
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            padding: 22px 24px 16px;
            margin-bottom: 20px;
        ">
            <div style="
                font-family: 'Syne', sans-serif;
                font-size: 14px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 16px;
                letter-spacing: -0.2px;
            ">Movimientos de Stock — Últimos 7 días</div>
        """, unsafe_allow_html=True)

        try:
            from datetime import timedelta
            hace_7 = (date.today() - timedelta(days=6)).isoformat()
            movs_semana = sb.table("movimiento").select("tipo,cantidad,fecha").gte("fecha", f"{hace_7}T00:00:00").execute().data or []
            entradas_por_dia = defaultdict(float)
            salidas_por_dia  = defaultdict(float)
            for m in movs_semana:
                dia = (m.get("fecha", ""))[:10]
                if m.get("tipo") == "entrada":
                    entradas_por_dia[dia] += float(m.get("cantidad", 0))
                else:
                    salidas_por_dia[dia]  += float(m.get("cantidad", 0))

            dias        = [(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
            labels_dias = [(date.today() - timedelta(days=i)).strftime("%d %b") for i in range(6, -1, -1)]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Entradas", x=labels_dias,
                y=[entradas_por_dia.get(d, 0) for d in dias],
                marker_color="#3b82f6", marker_line_width=0,
            ))
            fig.add_trace(go.Bar(
                name="Salidas", x=labels_dias,
                y=[salidas_por_dia.get(d, 0) for d in dias],
                marker_color="#f87171", marker_line_width=0,
            ))
            fig.update_layout(
                barmode="group",
                paper_bgcolor="white", plot_bgcolor="white",
                margin=dict(l=0, r=0, t=4, b=0),
                height=240,
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1,
                    font=dict(size=12, color="#475569", family="DM Sans"),
                ),
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, family="DM Sans", color="#475569"),
                    linecolor="#e2e8f0",
                ),
                yaxis=dict(
                    showgrid=True, gridcolor="#f1f5f9",
                    tickfont=dict(size=11, family="DM Sans", color="#64748b"),
                    zeroline=False,
                ),
                font=dict(family="DM Sans", color="#0f172a"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            if not movs_semana:
                st.markdown('<div style="text-align:center;color:#94a3b8;font-size:13px;padding:20px 0;">Sin movimientos en los últimos 7 días</div>', unsafe_allow_html=True)
        except Exception:
            st.warning("No se pudo cargar el gráfico de movimientos.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            padding: 22px 24px 16px;
            margin-bottom: 20px;
        ">
            <div style="
                font-family: 'Syne', sans-serif;
                font-size: 14px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 16px;
                letter-spacing: -0.2px;
            ">Órdenes por Estado</div>
        """, unsafe_allow_html=True)

        try:
            ordenes_all = sb.table("orden_compra").select("estado").execute().data or []
            if not ordenes_all:
                st.markdown('<div style="text-align:center;padding:40px 0;color:#94a3b8;font-size:13px;">Sin órdenes registradas</div>', unsafe_allow_html=True)
            else:
                conteo  = defaultdict(int)
                for o in ordenes_all:
                    conteo[o.get("estado", "desconocido")] += 1
                labels  = [k.capitalize() for k in conteo.keys()]
                values  = list(conteo.values())
                colores = {"Pendiente": "#f59e0b", "Recibida": "#22c55e", "Cancelada": "#f87171"}
                colors  = [colores.get(l, "#94a3b8") for l in labels]
                fig2 = go.Figure(go.Pie(
                    labels=labels, values=values, hole=0.58,
                    marker=dict(colors=colors, line=dict(color="white", width=3)),
                    textinfo="label+percent",
                    textfont=dict(size=12, family="DM Sans", color="#0f172a"),
                    hovertemplate="%{label}: %{value}<extra></extra>",
                ))
                fig2.update_layout(
                    paper_bgcolor="white",
                    margin=dict(l=0, r=0, t=4, b=0),
                    height=240,
                    showlegend=False,
                    annotations=[dict(
                        text=f"<b style='font-size:20px'>{len(ordenes_all)}</b><br>órdenes",
                        x=0.5, y=0.5,
                        font=dict(size=14, family="DM Sans", color="#0f172a"),
                        showarrow=False,
                    )],
                    font=dict(family="DM Sans", color="#0f172a"),
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            st.warning("No se pudo cargar el gráfico de órdenes.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Fila 2: Stock crítico + Últimos movimientos ───────────
    col_g3, col_g4 = st.columns([3, 2], gap="medium")

    with col_g3:
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            padding: 22px 24px 16px;
        ">
            <div style="
                font-family: 'Syne', sans-serif;
                font-size: 14px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 16px;
                letter-spacing: -0.2px;
            ">Stock Actual vs. Mínimo — Productos Críticos</div>
        """, unsafe_allow_html=True)

        try:
            criticos = [p for p in prods_all if (p["stock_actual"] or 0) < (p["stock_minimo"] or 0)]
            if not criticos:
                st.markdown("""
                <div style="text-align:center;padding:40px 0;">
                    <div style="font-size:32px;margin-bottom:10px;">✅</div>
                    <div style="font-size:14px;color:#15803d;font-weight:600;">
                        Todos los productos tienen stock suficiente
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                top       = criticos[:8]
                nombres   = [p["nombre"][:30] + ("…" if len(p["nombre"]) > 30 else "") for p in top]
                stock_act = [float(p.get("stock_actual") or 0) for p in top]
                stock_min = [float(p.get("stock_minimo") or 0) for p in top]

                fig3 = go.Figure()
                fig3.add_trace(go.Bar(
                    name="Stock Mínimo", y=nombres, x=stock_min,
                    orientation="h", marker_color="#fecaca", marker_line_width=0,
                ))
                fig3.add_trace(go.Bar(
                    name="Stock Actual", y=nombres, x=stock_act,
                    orientation="h", marker_color="#3b82f6", marker_line_width=0,
                ))
                fig3.update_layout(
                    barmode="overlay",
                    paper_bgcolor="white", plot_bgcolor="white",
                    margin=dict(l=0, r=0, t=4, b=0),
                    height=max(220, len(top) * 38),
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1,
                        font=dict(size=12, color="#475569", family="DM Sans"),
                    ),
                    xaxis=dict(
                        showgrid=True, gridcolor="#f1f5f9",
                        tickfont=dict(size=11, family="DM Sans", color="#64748b"),
                        zeroline=False,
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(size=12, family="DM Sans", color="#0f172a"),
                    ),
                    font=dict(family="DM Sans", color="#0f172a"),
                )
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            st.warning("No se pudo cargar el gráfico de stock crítico.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_g4:
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            padding: 22px 24px 16px;
        ">
            <div style="
                font-family: 'Syne', sans-serif;
                font-size: 14px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 16px;
                letter-spacing: -0.2px;
            ">Últimos Movimientos</div>
        """, unsafe_allow_html=True)

        try:
            movs = sb.table("movimiento").select(
                "tipo,cantidad,saldo,fecha,producto(nombre,unidad)"
            ).order("fecha", desc=True).limit(7).execute().data or []

            if not movs:
                st.markdown('<div style="text-align:center;padding:40px 0;color:#94a3b8;font-size:13px;">Sin movimientos registrados aún.</div>', unsafe_allow_html=True)
            else:
                for m in movs:
                    tipo     = m.get("tipo", "")
                    color_t  = "#16a34a" if tipo == "entrada" else "#dc2626"
                    bg_t     = "#dcfce7"  if tipo == "entrada" else "#fee2e2"
                    signo    = "+" if tipo == "entrada" else "−"
                    prod     = (m.get("producto") or {})
                    nombre_p = prod.get("nombre", "—")
                    nombre_p = nombre_p[:24] + "…" if len(nombre_p) > 24 else nombre_p
                    unidad   = prod.get("unidad", "")
                    fecha_s  = (m.get("fecha", ""))[:10]
                    st.markdown(f"""
                    <div style="
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        padding: 10px 0;
                        border-bottom: 1px solid #f1f5f9;
                    ">
                        <div style="display:flex;align-items:center;gap:10px;">
                            <div style="
                                width: 30px; height: 30px;
                                border-radius: 50%;
                                background: {bg_t};
                                display: flex; align-items: center; justify-content: center;
                                font-size: 13px; font-weight: 700;
                                color: {color_t}; flex-shrink: 0;
                            ">{'↑' if tipo=='entrada' else '↓'}</div>
                            <div>
                                <div style="font-size: 13px; font-weight: 600; color: #0f172a;">{nombre_p}</div>
                                <div style="font-size: 11px; color: #94a3b8; margin-top: 1px;">{fecha_s}</div>
                            </div>
                        </div>
                        <div style="font-size: 13px; font-weight: 700; color: {color_t}; white-space: nowrap;">
                            {signo}{m.get('cantidad', 0)} {unidad}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception:
            st.warning("No se pudieron cargar los movimientos.")

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# VISTA: PRODUCTOS
# ─────────────────────────────────────────────────────────────

def render_productos():
    page_header("Productos", "Gestión de materiales, insumos y herramientas del almacén")
    sb      = get_supabase()
    usuario = st.session_state.get("user_email", "")

    tab_lista, tab_nuevo, tab_editar = st.tabs(["Lista de productos", "Nuevo producto", "Editar / Eliminar"])

    with tab_lista:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        col_search, col_cat = st.columns([2, 1])
        with col_search:
            buscar = st.text_input("Buscar producto", placeholder="Escribe nombre o código y presiona Enter...")
        with col_cat:
            try:
                cats     = sb.table("categoria").select("id,nombre").order("nombre").execute().data or []
                cat_opts = {"Todas las categorías": None} | {c["nombre"]: c["id"] for c in cats}
            except Exception:
                cat_opts = {"Todas las categorías": None}
            cat_sel = st.selectbox("Categoría", list(cat_opts.keys()))

        # Solo mostrar tabla si el usuario busca algo o filtra
        hay_filtro = bool(buscar.strip()) or cat_opts[cat_sel] is not None
        if not hay_filtro:
            empty_state(
                "📦",
                "Usa el buscador para encontrar productos",
                "Escribe un nombre o código, o selecciona una categoría para ver los resultados."
            )
        else:
            try:
                data = sb.table("producto").select("*,categoria(nombre)").order("nombre").execute().data or []
                if buscar.strip():
                    data = [p for p in data if buscar.lower() in (p.get("nombre","") + p.get("codigo","")).lower()]
                if cat_opts[cat_sel]:
                    data = [p for p in data if p.get("id_categoria") == cat_opts[cat_sel]]
                if not data:
                    empty_state("🔍", "Sin resultados", "No se encontraron productos con esos criterios de búsqueda.")
                else:
                    st.markdown(f"""
                    <div style="font-size:11px;color:#64748b;margin-bottom:10px;font-weight:500;">
                        {len(data)} producto{'s' if len(data) != 1 else ''} encontrado{'s' if len(data) != 1 else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    for p in data:
                        stock_a    = p.get("stock_actual", 0) or 0
                        stock_m    = p.get("stock_minimo", 0) or 0
                        critico    = stock_a < stock_m
                        cat_nombre = (p.get("categoria") or {}).get("nombre", "—")
                        bd_stock   = badge("⚠ Crítico", "red") if critico else badge("OK", "green")
                        st.markdown(f"""
                        <div style="
                            background:white;border-radius:10px;
                            border:1px solid {'#fecaca' if critico else '#e2e8f0'};
                            border-left:4px solid {'#dc2626' if critico else '#22c55e'};
                            padding:14px 18px;margin-bottom:8px;
                        ">
                            <div style="display:flex;align-items:center;justify-content:space-between;">
                                <div>
                                    <span style="font-size:13px;font-weight:600;color:#0f172a;">{p['nombre']}</span>
                                    <span style="font-size:11px;color:#94a3b8;margin-left:10px;">{p.get('codigo','')}</span>
                                </div>
                                <div style="display:flex;gap:8px;align-items:center;">
                                    {bd_stock}
                                    <span style="font-size:11px;color:#475569;background:#f1f5f9;
                                                 padding:3px 9px;border-radius:20px;">{cat_nombre}</span>
                                </div>
                            </div>
                            <div style="display:flex;gap:20px;margin-top:8px;">
                                <span style="font-size:11px;color:#64748b;">
                                    Stock: <b style="color:#0f172a;">{stock_a} {p.get('unidad','')}</b>
                                </span>
                                <span style="font-size:11px;color:#64748b;">
                                    Mínimo: <b style="color:#0f172a;">{stock_m} {p.get('unidad','')}</b>
                                </span>
                                <span style="font-size:11px;color:#64748b;">
                                    Precio: <b style="color:#0f172a;">S/ {p.get('precio_unitario',0):.2f}</b>
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error cargando productos: {e}")

    with tab_nuevo:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.form("form_nuevo_producto", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                codigo = st.text_input("Código *", placeholder="MP-001")
                nombre = st.text_input("Nombre *", placeholder="Plancha de acero A36")
                unidad = st.selectbox("Unidad *", ["kg","unidad","m","lt","m2","m3","caja","par","rollo"])
            with c2:
                try:
                    cats2    = sb.table("categoria").select("id,nombre").order("nombre").execute().data or []
                    cat_map2 = {c["nombre"]: c["id"] for c in cats2}
                except Exception:
                    cat_map2 = {}
                cat_nombre_s = st.selectbox("Categoría", list(cat_map2.keys()) if cat_map2 else ["Sin categorías"])
                stock_min    = st.number_input("Stock mínimo", min_value=0.0, step=1.0)
                precio       = st.number_input("Precio unitario (S/)", min_value=0.0, step=0.01, format="%.2f")
            if st.form_submit_button("Guardar producto", type="primary", use_container_width=True):
                if not codigo or not nombre:
                    st.error("Código y Nombre son obligatorios.")
                else:
                    try:
                        sb.table("producto").insert({
                            "codigo":         codigo.strip().upper(),
                            "nombre":         nombre.strip(),
                            "unidad":         unidad,
                            "id_categoria":   cat_map2.get(cat_nombre_s),
                            "stock_actual":   0,
                            "stock_minimo":   stock_min,
                            "precio_unitario":precio,
                        }).execute()
                        log_action("insert", "producto", usuario, f"Nuevo producto: {nombre}")
                        st.success(f"✅ Producto '{nombre}' creado correctamente.")
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

    with tab_editar:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        try:
            prods_e    = sb.table("producto").select("id,nombre,codigo").order("nombre").execute().data or []
            if not prods_e:
                empty_state("📦", "No hay productos registrados", "Crea uno en la pestaña 'Nuevo producto'.")
            else:
                prod_map_e = {f"[{p['codigo']}] {p['nombre']}": p["id"] for p in prods_e}
                sel_label  = st.selectbox("Seleccionar producto a editar", list(prod_map_e.keys()))
                prod_id    = prod_map_e.get(sel_label)
                if prod_id:
                    prod       = sb.table("producto").select("*,categoria(nombre)").eq("id", prod_id).single().execute().data
                    cats_e     = sb.table("categoria").select("id,nombre").order("nombre").execute().data or []
                    cat_map_e  = {c["nombre"]: c["id"] for c in cats_e}
                    cat_names_e= list(cat_map_e.keys())
                    cat_actual = (prod.get("categoria") or {}).get("nombre", cat_names_e[0] if cat_names_e else "")
                    UNIDADES   = ["kg","unidad","m","lt","m2","m3","caja","par","rollo"]
                    with st.form("form_editar_producto"):
                        c1, c2 = st.columns(2)
                        with c1:
                            e_codigo = st.text_input("Código", value=prod.get("codigo",""))
                            e_nombre = st.text_input("Nombre", value=prod.get("nombre",""))
                            e_unidad = st.selectbox("Unidad", UNIDADES,
                                index=UNIDADES.index(prod.get("unidad","unidad")) if prod.get("unidad") in UNIDADES else 0)
                        with c2:
                            e_cat    = st.selectbox("Categoría", cat_names_e,
                                index=cat_names_e.index(cat_actual) if cat_actual in cat_names_e else 0)
                            e_stock_m= st.number_input("Stock mínimo", value=float(prod.get("stock_minimo",0)), min_value=0.0)
                            e_precio = st.number_input("Precio unitario", value=float(prod.get("precio_unitario",0)),
                                                        min_value=0.0, format="%.2f")
                        col_save, col_del = st.columns([3, 1])
                        with col_save:
                            if st.form_submit_button("Actualizar producto", type="primary", use_container_width=True):
                                sb.table("producto").update({
                                    "codigo":           e_codigo.strip().upper(),
                                    "nombre":           e_nombre.strip(),
                                    "unidad":           e_unidad,
                                    "id_categoria":     cat_map_e.get(e_cat),
                                    "stock_minimo":     e_stock_m,
                                    "precio_unitario":  e_precio,
                                }).eq("id", prod_id).execute()
                                log_action("update", "producto", usuario, f"Editado: {e_nombre}")
                                st.success("✅ Producto actualizado.")
                                st.rerun()
                        with col_del:
                            if st.form_submit_button("Eliminar", use_container_width=True):
                                sb.table("producto").delete().eq("id", prod_id).execute()
                                log_action("delete", "producto", usuario, f"Eliminado: {prod.get('nombre')}")
                                st.success("Producto eliminado.")
                                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")


# ─────────────────────────────────────────────────────────────
# VISTA: CATEGORÍAS
# ─────────────────────────────────────────────────────────────

def render_categorias():
    page_header("Categorías", "Clasificación de productos del inventario")
    sb      = get_supabase()
    usuario = st.session_state.get("user_email", "")

    tab_lista, tab_nuevo, tab_editar = st.tabs(["Lista", "Nueva categoría", "Editar / Eliminar"])

    with tab_lista:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        try:
            cats = sb.table("categoria").select("id,nombre").order("nombre").execute().data or []
            if not cats:
                empty_state("🏷️", "No hay categorías registradas",
                            "Crea la primera categoría en la pestaña 'Nueva categoría'.")
            else:
                cols = st.columns(3)
                for i, c in enumerate(cats):
                    prods = sb.table("producto").select("id", count="exact").eq("id_categoria", c["id"]).execute().count or 0
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div style="
                            background:white;border-radius:10px;
                            border:1px solid #e2e8f0;
                            padding:18px 16px;margin-bottom:10px;text-align:center;
                        ">
                            <div style="
                                width:40px;height:40px;border-radius:10px;
                                background:#dbeafe;
                                display:inline-flex;align-items:center;justify-content:center;
                                font-size:18px;margin-bottom:8px;
                            ">🏷️</div>
                            <div style="font-size:13px;font-weight:600;color:#0f172a;">{c['nombre']}</div>
                            <div style="font-size:11px;color:#64748b;margin-top:4px;">
                                {prods} producto{'s' if prods != 1 else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error cargando categorías: {e}")

    with tab_nuevo:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.form("form_nueva_cat", clear_on_submit=True):
            nombre = st.text_input("Nombre de la categoría *", placeholder="Ej: Materia prima")
            if st.form_submit_button("Guardar categoría", type="primary", use_container_width=True):
                if not nombre.strip():
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        sb.table("categoria").insert({"nombre": nombre.strip()}).execute()
                        log_action("insert", "categoria", usuario, f"Nueva categoría: {nombre}")
                        st.success(f"✅ Categoría '{nombre}' creada.")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab_editar:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        try:
            cats    = sb.table("categoria").select("id,nombre").order("nombre").execute().data or []
            if not cats:
                empty_state("🏷️", "No hay categorías para editar")
            else:
                cat_map = {c["nombre"]: c["id"] for c in cats}
                sel     = st.selectbox("Seleccionar categoría", list(cat_map.keys()))
                cat_id  = cat_map.get(sel)
                if cat_id:
                    with st.form("form_editar_cat"):
                        nuevo_nombre = st.text_input("Nuevo nombre", value=sel)
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            if st.form_submit_button("Actualizar", type="primary", use_container_width=True):
                                sb.table("categoria").update({"nombre": nuevo_nombre.strip()}).eq("id", cat_id).execute()
                                log_action("update", "categoria", usuario, f"Editada: {nuevo_nombre}")
                                st.success("✅ Categoría actualizada.")
                                st.rerun()
                        with c2:
                            if st.form_submit_button("Eliminar", use_container_width=True):
                                sb.table("categoria").delete().eq("id", cat_id).execute()
                                log_action("delete", "categoria", usuario, f"Eliminada: {sel}")
                                st.success("Eliminada.")
                                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")


# ─────────────────────────────────────────────────────────────
# VISTA: PROVEEDORES
# ─────────────────────────────────────────────────────────────

def render_proveedores():
    page_header("Proveedores", "Empresas y personas que abastecen el almacén")
    sb      = get_supabase()
    usuario = st.session_state.get("user_email", "")

    tab_lista, tab_nuevo, tab_editar = st.tabs(["Lista", "Nuevo proveedor", "Editar / Eliminar"])

    with tab_lista:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        buscar = st.text_input("Buscar proveedor", placeholder="Escribe nombre o RUC para buscar...")

        if not buscar.strip():
            empty_state(
                "🚚",
                "Busca un proveedor para verlo aquí",
                "Escribe el nombre o RUC en el campo de búsqueda. Para ver todos, escribe un espacio."
            )
        else:
            try:
                provs = sb.table("proveedor").select("*").order("nombre").execute().data or []
                if buscar.strip() != " ":
                    provs = [p for p in provs if buscar.lower() in (p.get("nombre","") + (p.get("ruc") or "")).lower()]
                if not provs:
                    empty_state("🔍", "Sin resultados", "No se encontraron proveedores con ese criterio.")
                else:
                    st.markdown(f"""
                    <div style="font-size:11px;color:#64748b;margin-bottom:10px;font-weight:500;">
                        {len(provs)} proveedor{'es' if len(provs) != 1 else ''} encontrado{'s' if len(provs) != 1 else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    for p in provs:
                        initial = p['nombre'][0].upper()
                        st.markdown(f"""
                        <div style="
                            background:white;border-radius:10px;
                            border:1px solid #e2e8f0;
                            padding:14px 18px;margin-bottom:8px;
                            display:flex;align-items:center;gap:14px;
                        ">
                            <div style="
                                width:40px;height:40px;border-radius:50%;
                                background:linear-gradient(135deg,#3b82f6,#1d4ed8);
                                display:flex;align-items:center;justify-content:center;
                                font-size:15px;font-weight:800;color:white;flex-shrink:0;
                            ">{initial}</div>
                            <div style="flex:1;">
                                <div style="font-size:13px;font-weight:600;color:#0f172a;">{p['nombre']}</div>
                                <div style="font-size:11px;color:#64748b;margin-top:2px;">
                                    RUC: {p.get('ruc') or '—'}
                                    &nbsp;&nbsp;·&nbsp;&nbsp;
                                    Tel: {p.get('telefono') or '—'}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error cargando proveedores: {e}")

    with tab_nuevo:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.form("form_nuevo_prov", clear_on_submit=True):
            nombre = st.text_input("Razón social / Nombre *", placeholder="Aceros del Perú S.A.C.")
            c1, c2 = st.columns(2)
            with c1:
                ruc = st.text_input("RUC", placeholder="20123456789")
            with c2:
                tel = st.text_input("Teléfono", placeholder="01-234-5678")
            if st.form_submit_button("Guardar proveedor", type="primary", use_container_width=True):
                if not nombre.strip():
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        sb.table("proveedor").insert({
                            "nombre":   nombre.strip(),
                            "ruc":      ruc.strip() or None,
                            "telefono": tel.strip() or None,
                        }).execute()
                        log_action("insert", "proveedor", usuario, f"Nuevo proveedor: {nombre}")
                        st.success(f"✅ Proveedor '{nombre}' creado.")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab_editar:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        try:
            provs    = sb.table("proveedor").select("id,nombre").order("nombre").execute().data or []
            if not provs:
                empty_state("🚚", "No hay proveedores registrados", "Crea uno en la pestaña 'Nuevo proveedor'.")
            else:
                prov_map = {p["nombre"]: p["id"] for p in provs}
                sel      = st.selectbox("Seleccionar proveedor", list(prov_map.keys()))
                prov_id  = prov_map.get(sel)
                if prov_id:
                    prov = sb.table("proveedor").select("*").eq("id", prov_id).single().execute().data
                    with st.form("form_editar_prov"):
                        e_nombre = st.text_input("Nombre", value=prov.get("nombre",""))
                        c1, c2   = st.columns(2)
                        with c1:
                            e_ruc = st.text_input("RUC", value=prov.get("ruc","") or "")
                        with c2:
                            e_tel = st.text_input("Teléfono", value=prov.get("telefono","") or "")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if st.form_submit_button("Actualizar", type="primary", use_container_width=True):
                                sb.table("proveedor").update({
                                    "nombre":   e_nombre.strip(),
                                    "ruc":      e_ruc.strip() or None,
                                    "telefono": e_tel.strip() or None,
                                }).eq("id", prov_id).execute()
                                log_action("update", "proveedor", usuario, f"Editado: {e_nombre}")
                                st.success("✅ Proveedor actualizado.")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Eliminar", use_container_width=True):
                                sb.table("proveedor").delete().eq("id", prov_id).execute()
                                log_action("delete", "proveedor", usuario, f"Eliminado: {sel}")
                                st.success("Eliminado.")
                                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")


# ─────────────────────────────────────────────────────────────
# VISTA: ÓRDENES DE COMPRA
# ─────────────────────────────────────────────────────────────

def render_ordenes():
    page_header("Órdenes de Compra", "Gestión de órdenes emitidas a proveedores")
    sb      = get_supabase()
    usuario = st.session_state.get("user_email", "")

    tab_lista, tab_nuevo, tab_estado = st.tabs(["Lista", "Nueva orden", "Cambiar estado"])

    with tab_lista:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        c1, _ = st.columns([1, 2])
        with c1:
            filtro_estado = st.selectbox("Filtrar por estado", ["Todos","pendiente","recibida","cancelada"])

        buscar_orden = st.text_input("Buscar por número de orden", placeholder="Escribe el número o deja vacío para ver todas...")

        hay_filtro = filtro_estado != "Todos" or bool(buscar_orden.strip())
        if not hay_filtro:
            empty_state(
                "📋",
                "Filtra o busca para ver órdenes",
                "Selecciona un estado o escribe el número de orden para ver los resultados."
            )
        else:
            try:
                ordenes = sb.table("orden_compra").select("*,proveedor(nombre)").order("fecha", desc=True).execute().data or []
                if filtro_estado != "Todos":
                    ordenes = [o for o in ordenes if o.get("estado") == filtro_estado]
                if buscar_orden.strip():
                    ordenes = [o for o in ordenes if buscar_orden.lower() in (o.get("numero","")).lower()]
                estado_color = {"pendiente":"amber","recibida":"green","cancelada":"red"}
                if not ordenes:
                    empty_state("🔍", "Sin resultados", "No se encontraron órdenes con esos criterios.")
                else:
                    for o in ordenes:
                        prov = (o.get("proveedor") or {}).get("nombre","—")
                        bd   = badge(o.get("estado","").capitalize(), estado_color.get(o.get("estado",""),"gray"))
                        st.markdown(f"""
                        <div style="background:white;border-radius:10px;border:1px solid #e2e8f0;
                                    padding:14px 18px;margin-bottom:8px;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <div>
                                    <span style="font-size:14px;font-weight:700;color:#0f172a;
                                                 font-family:'Syne',sans-serif;">{o.get('numero','')}</span>
                                    <span style="font-size:11px;color:#64748b;margin-left:10px;">🚚 {prov}</span>
                                </div>
                                <div style="display:flex;gap:10px;align-items:center;">
                                    <span style="font-size:11px;color:#94a3b8;">{o.get('fecha','')}</span>
                                    {bd}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        with st.expander(f"Ver ítems — {o.get('numero','')}"):
                            try:
                                detalles = sb.table("detalle_orden").select(
                                    "*,producto(nombre,unidad)"
                                ).eq("id_orden", o["id"]).execute().data or []
                                if not detalles:
                                    st.info("Esta orden no tiene ítems registrados.")
                                else:
                                    total = 0
                                    for d in detalles:
                                        prod = (d.get("producto") or {})
                                        sub  = d.get("subtotal") or (d["cantidad"] * d["precio_unitario"])
                                        total += sub
                                        st.markdown(f"""
                                        <div style="display:flex;justify-content:space-between;
                                                    padding:7px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">
                                            <span style="color:#0f172a;font-weight:600;">{prod.get('nombre','—')}</span>
                                            <span style="color:#64748b;">{d['cantidad']} {prod.get('unidad','')} × S/ {d['precio_unitario']:.2f}</span>
                                            <span style="font-weight:700;color:#0f172a;">S/ {sub:.2f}</span>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    st.markdown(f"""
                                    <div style="text-align:right;margin-top:8px;font-size:13px;
                                                font-weight:700;color:#1d4ed8;">
                                        Total: S/ {total:.2f}
                                    </div>
                                    """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Error cargando detalle: {e}")
            except Exception as e:
                st.error(f"Error cargando órdenes: {e}")

    with tab_nuevo:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.form("form_nueva_orden"):
            c1, c2 = st.columns(2)
            with c1:
                numero = st.text_input("N° de Orden *", placeholder="OC-2026-019")
                try:
                    provs    = sb.table("proveedor").select("id,nombre").order("nombre").execute().data or []
                    prov_map = {p["nombre"]: p["id"] for p in provs}
                except Exception:
                    provs, prov_map = [], {}
                prov_sel = st.selectbox("Proveedor *", list(prov_map.keys()) if prov_map else ["Sin proveedores"])
            with c2:
                fecha  = st.date_input("Fecha", value=date.today())
                estado = st.selectbox("Estado inicial", ["pendiente","recibida","cancelada"])
            st.markdown("---")
            st.markdown("**Ítems de la orden**")
            try:
                prods    = sb.table("producto").select("id,nombre,unidad,precio_unitario").order("nombre").execute().data or []
                prod_map = {f"{p['nombre']} ({p['unidad']})": p for p in prods}
            except Exception:
                prods, prod_map = [], {}
            n_items = st.number_input("Cantidad de ítems", min_value=1, max_value=20, value=1, step=1)
            items = []
            for i in range(int(n_items)):
                st.markdown(f"**Ítem {i+1}**")
                ic1, ic2, ic3 = st.columns([3,1,1])
                with ic1:
                    prod_label = st.selectbox("Producto", list(prod_map.keys()), key=f"prod_{i}")
                with ic2:
                    cant = st.number_input("Cantidad", min_value=0.0, step=1.0, key=f"cant_{i}")
                with ic3:
                    precio_sug = prod_map[prod_label]["precio_unitario"] if prod_label in prod_map else 0.0
                    precio_u   = st.number_input("P. Unit (S/)", min_value=0.0, value=float(precio_sug), step=0.01, key=f"pu_{i}")
                items.append((prod_label, cant, precio_u))
            if st.form_submit_button("Crear orden de compra", type="primary", use_container_width=True):
                if not numero.strip() or not prov_map:
                    st.error("Número de orden y proveedor son obligatorios.")
                else:
                    try:
                        orden_resp = sb.table("orden_compra").insert({
                            "numero":       numero.strip().upper(),
                            "id_proveedor": prov_map.get(prov_sel),
                            "fecha":        fecha.isoformat(),
                            "estado":       estado,
                        }).execute()
                        orden_id = orden_resp.data[0]["id"]
                        for (pl, c, pu) in items:
                            if c > 0 and pl in prod_map:
                                sb.table("detalle_orden").insert({
                                    "id_orden":        orden_id,
                                    "id_producto":     prod_map[pl]["id"],
                                    "cantidad":        c,
                                    "precio_unitario": pu,
                                }).execute()
                        log_action("insert", "orden_compra", usuario, f"Nueva orden: {numero}")
                        st.success(f"✅ Orden '{numero}' creada con {int(n_items)} ítem(s).")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab_estado:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        try:
            ordenes = sb.table("orden_compra").select("id,numero,estado").order("fecha", desc=True).execute().data or []
            if not ordenes:
                empty_state("📋", "No hay órdenes registradas")
            else:
                ord_map   = {f"{o['numero']}  [{o['estado'].upper()}]": o for o in ordenes}
                sel_label = st.selectbox("Seleccionar orden", list(ord_map.keys()))
                orden     = ord_map.get(sel_label)
                if orden:
                    ESTADOS      = ["pendiente","recibida","cancelada"]
                    nuevo_estado = st.selectbox("Nuevo estado", ESTADOS,
                                                index=ESTADOS.index(orden["estado"]) if orden["estado"] in ESTADOS else 0)
                    if st.button("Actualizar estado", type="primary"):
                        sb.table("orden_compra").update({"estado": nuevo_estado}).eq("id", orden["id"]).execute()
                        log_action("update", "orden_compra", usuario, f"Estado {orden['numero']}: {nuevo_estado}")
                        st.success(f"✅ Estado actualizado a '{nuevo_estado}'.")
                        st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")


# ─────────────────────────────────────────────────────────────
# VISTA: OPERACIONES DE ALMACÉN
# ─────────────────────────────────────────────────────────────

def render_operaciones():
    page_header("Operaciones de Almacén", "Registro de entradas y salidas de materiales")
    sb      = get_supabase()
    usuario = st.session_state.get("user_email", "")

    tab_lista, tab_nuevo = st.tabs(["Historial", "Nueva operación"])

    with tab_lista:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            filtro_tipo   = st.selectbox("Tipo", ["Todos","entrada","salida"])
        with c2:
            filtro_motivo = st.selectbox("Motivo", ["Todos","compra","devolucion","produccion","ajuste"])

        buscar_op = st.text_input("Buscar por N° de documento", placeholder="Escribe el número o deja vacío para ver todas...")
        hay_filtro = filtro_tipo != "Todos" or filtro_motivo != "Todos" or bool(buscar_op.strip())

        if not hay_filtro:
            empty_state(
                "🏗️",
                "Aplica un filtro para ver operaciones",
                "Filtra por tipo, motivo, o busca por número de documento."
            )
        else:
            try:
                ops = sb.table("operacion_almacen").select(
                    "*,proveedor(nombre)"
                ).order("fecha", desc=True).limit(100).execute().data or []
                if filtro_tipo   != "Todos": ops = [o for o in ops if o.get("tipo")   == filtro_tipo]
                if filtro_motivo != "Todos": ops = [o for o in ops if o.get("motivo") == filtro_motivo]
                if buscar_op.strip():        ops = [o for o in ops if buscar_op.lower() in (o.get("numero_doc","")).lower()]

                if not ops:
                    empty_state("🔍", "Sin resultados", "No se encontraron operaciones con esos filtros.")
                else:
                    tipo_color   = {"entrada":"green","salida":"red"}
                    motivo_color = {"compra":"blue","devolucion":"amber","produccion":"green","ajuste":"gray"}
                    for op in ops:
                        prov         = (op.get("proveedor") or {}).get("nombre","—")
                        fecha_str    = (op.get("fecha",""))[:16].replace("T"," ")
                        bd_tipo      = badge(op.get("tipo","").capitalize(), tipo_color.get(op.get("tipo",""),"gray"))
                        bd_motivo    = badge(op.get("motivo","").capitalize(), motivo_color.get(op.get("motivo",""),"gray"))
                        color_border = "#22c55e" if op.get("tipo") == "entrada" else "#ef4444"
                        prov_line    = f"🚚 {prov}" if op.get("id_proveedor") else ""
                        obs_line     = f" · 📝 {op['observacion']}" if op.get("observacion") else ""
                        meta_line    = prov_line + obs_line
                        st.markdown(f"""
                        <div style="background:white;border-radius:10px;border:1px solid #e2e8f0;
                                    border-left:4px solid {color_border};padding:14px 18px;margin-bottom:8px;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <div>
                                    <span style="font-size:13px;font-weight:700;color:#0f172a;
                                                 font-family:'Syne',sans-serif;">{op.get('numero_doc','')}</span>
                                    <span style="font-size:10px;color:#94a3b8;margin-left:8px;">{fecha_str}</span>
                                </div>
                                <div style="display:flex;gap:6px;">{bd_tipo} {bd_motivo}</div>
                            </div>
                            <div style="font-size:11px;color:#64748b;margin-top:6px;">{meta_line}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        with st.expander(f"Ver ítems — {op.get('numero_doc','')}"):
                            try:
                                dets = sb.table("detalle_operacion").select(
                                    "*,producto(nombre,unidad)"
                                ).eq("id_operacion", op["id"]).execute().data or []
                                if not dets:
                                    st.info("Esta operación no tiene ítems detallados.")
                                else:
                                    for d in dets:
                                        prod = (d.get("producto") or {})
                                        st.markdown(f"""
                                        <div style="display:flex;justify-content:space-between;
                                                    padding:7px 0;border-bottom:1px solid #f1f5f9;font-size:12px;">
                                            <span style="color:#0f172a;font-weight:600;">{prod.get('nombre','—')}</span>
                                            <span style="color:#64748b;">
                                                {d.get('cantidad',0)} {prod.get('unidad','')} ×
                                                S/ {d.get('precio_unitario',0):.2f}
                                            </span>
                                        </div>
                                        """, unsafe_allow_html=True)
                            except Exception:
                                st.info("No se pudo cargar el detalle de esta operación.")
            except Exception as e:
                st.error(f"Error cargando operaciones: {e}")

    with tab_nuevo:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        info_banner("ℹ️ Al registrar una operación, el stock de cada producto se actualiza automáticamente.", "info")
        with st.form("form_nueva_op", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                numero_doc = st.text_input("N° Documento *", placeholder="OP-2026-001")
                tipo       = st.selectbox("Tipo *", ["entrada","salida"])
            with c2:
                motivo = st.selectbox("Motivo *", ["compra","devolucion","produccion","ajuste"])
                try:
                    provs    = sb.table("proveedor").select("id,nombre").order("nombre").execute().data or []
                    prov_map = {"— Sin proveedor —": None} | {p["nombre"]: p["id"] for p in provs}
                except Exception:
                    prov_map = {"— Sin proveedor —": None}
                prov_sel = st.selectbox("Proveedor (opcional)", list(prov_map.keys()))
                observacion = st.text_area("Observación", placeholder="Notas adicionales...", height=70)
            st.markdown("---")
            st.markdown("**Ítems de la operación**")
            try:
                prods    = sb.table("producto").select("id,nombre,unidad,stock_actual,precio_unitario").order("nombre").execute().data or []
                prod_map = {f"{p['nombre']} ({p['unidad']}) — Stock: {p['stock_actual']}": p for p in prods}
            except Exception:
                prods, prod_map = [], {}
            n_items = st.number_input("Cantidad de ítems", min_value=1, max_value=20, value=1, step=1)
            items = []
            for i in range(int(n_items)):
                st.markdown(f"**Ítem {i+1}**")
                ic1, ic2, ic3 = st.columns([3,1,1])
                with ic1:
                    prod_label = st.selectbox("Producto", list(prod_map.keys()), key=f"op_prod_{i}")
                with ic2:
                    cant = st.number_input("Cantidad", min_value=0.0, step=1.0, key=f"op_cant_{i}")
                with ic3:
                    precio_sug = prod_map[prod_label]["precio_unitario"] if prod_label in prod_map else 0.0
                    precio_u   = st.number_input("P. Unit (S/)", min_value=0.0, value=float(precio_sug), step=0.01, key=f"op_pu_{i}")
                items.append((prod_label, cant, precio_u))
            if st.form_submit_button("Registrar operación", type="primary", use_container_width=True):
                if not numero_doc.strip():
                    st.error("El número de documento es obligatorio.")
                else:
                    try:
                        op_resp = sb.table("operacion_almacen").insert({
                            "numero_doc":   numero_doc.strip().upper(),
                            "tipo":         tipo,
                            "motivo":       motivo,
                            "id_proveedor": prov_map.get(prov_sel),
                            "observacion":  observacion.strip() or None,
                            "fecha":        datetime.now(timezone.utc).isoformat(),
                        }).execute()
                        op_id   = op_resp.data[0]["id"]
                        errores = []
                        for (pl, c, pu) in items:
                            if c <= 0 or pl not in prod_map:
                                continue
                            prod_data = prod_map[pl]
                            prod_id   = prod_data["id"]
                            stock_ant = float(prod_data.get("stock_actual", 0) or 0)
                            if tipo == "salida" and c > stock_ant:
                                errores.append(f"{prod_data['nombre']}: stock insuficiente ({stock_ant} disponible)")
                                continue
                            sb.table("detalle_operacion").insert({
                                "id_operacion":    op_id,
                                "id_producto":     prod_id,
                                "cantidad":        c,
                                "precio_unitario": pu,
                            }).execute()
                            nuevo_stock = stock_ant + c if tipo == "entrada" else stock_ant - c
                            sb.table("producto").update({"stock_actual": nuevo_stock}).eq("id", prod_id).execute()
                            sb.table("movimiento").insert({
                                "id_producto":  prod_id,
                                "id_operacion": op_id,
                                "tipo":         tipo,
                                "cantidad":     c,
                                "saldo":        nuevo_stock,
                                "fecha":        datetime.now(timezone.utc).isoformat(),
                            }).execute()
                        log_action("insert", "operacion_almacen", usuario, f"Op: {numero_doc} | {tipo} | {motivo}")
                        if errores:
                            for err in errores:
                                st.warning(f"⚠️ {err}")
                        else:
                            st.success(f"✅ Operación '{numero_doc}' registrada. Stock actualizado automáticamente.")
                    except Exception as e:
                        st.error(f"Error al registrar: {e}")


# ─────────────────────────────────────────────────────────────
# VISTA: MOVIMIENTOS (solo lectura)
# ─────────────────────────────────────────────────────────────

def render_movimientos():
    page_header("Historial de Movimientos", "Registro cronológico de todos los cambios de stock")
    sb = get_supabase()

    info_banner("🔒 Este historial es de <b>solo lectura</b>. Se genera automáticamente al registrar operaciones.", "info")

    c1, c2, c3 = st.columns(3)
    with c1:
        filtro_tipo = st.selectbox("Tipo", ["Todos","entrada","salida"])
    with c2:
        try:
            prods     = sb.table("producto").select("id,nombre").order("nombre").execute().data or []
            prod_opts = {"Todos los productos": None} | {p["nombre"]: p["id"] for p in prods}
            filtro_prod = st.selectbox("Producto", list(prod_opts.keys()))
        except Exception:
            filtro_prod = "Todos los productos"
            prod_opts   = {"Todos los productos": None}
    with c3:
        limite = st.selectbox("Mostrar últimos", [20, 50, 100, 200], index=0)

    hay_filtro = filtro_tipo != "Todos" or prod_opts.get(filtro_prod) is not None

    if not hay_filtro:
        empty_state(
            "🔄",
            "Aplica un filtro para ver el historial",
            "Filtra por tipo de movimiento o selecciona un producto específico."
        )
    else:
        try:
            query = sb.table("movimiento").select(
                "*,producto(nombre,unidad),operacion_almacen(numero_doc,motivo)"
            ).order("fecha", desc=True).limit(limite)
            if prod_opts.get(filtro_prod):
                query = query.eq("id_producto", prod_opts[filtro_prod])
            if filtro_tipo != "Todos":
                query = query.eq("tipo", filtro_tipo)
            movs = query.execute().data or []

            if not movs:
                empty_state("🔍", "Sin movimientos", "No hay movimientos con los filtros seleccionados.")
                return

            # Tabla de movimientos
            st.markdown("""
            <div style="background:white;border-radius:12px;border:1px solid #e2e8f0;overflow:hidden;">
            <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1.5fr;
                        padding:10px 16px;background:#f8fafc;border-bottom:1px solid #e2e8f0;
                        font-size:10px;font-weight:700;color:#64748b;
                        letter-spacing:0.6px;text-transform:uppercase;">
                <span>Producto</span><span>Tipo</span>
                <span>Cantidad</span><span>Saldo</span>
                <span>Motivo</span><span>Fecha</span>
            </div>
            """, unsafe_allow_html=True)

            tipo_color   = {"entrada":"green","salida":"red"}
            motivo_color = {"compra":"blue","devolucion":"amber","produccion":"green","ajuste":"gray"}

            for m in movs:
                prod    = (m.get("producto") or {})
                op      = (m.get("operacion_almacen") or {})
                nombre  = prod.get("nombre","—")
                unidad  = prod.get("unidad","")
                tipo    = m.get("tipo","")
                motivo  = op.get("motivo","—")
                num_doc = op.get("numero_doc","")
                fecha   = (m.get("fecha",""))[:16].replace("T"," ")
                cant    = m.get("cantidad",0)
                saldo   = m.get("saldo",0)
                signo   = "+" if tipo == "entrada" else "−"
                color   = "#16a34a" if tipo == "entrada" else "#dc2626"
                bd_tipo = badge(tipo.capitalize(), tipo_color.get(tipo,"gray"))
                bd_mot  = badge(motivo.capitalize(), motivo_color.get(motivo,"gray"))
                st.markdown(f"""
                <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1.5fr;
                            padding:10px 16px;border-bottom:1px solid #f1f5f9;align-items:center;">
                    <div>
                        <div style="font-size:12px;font-weight:600;color:#0f172a;">{nombre}</div>
                        <div style="font-size:10px;color:#94a3b8;">{num_doc}</div>
                    </div>
                    <span>{bd_tipo}</span>
                    <span style="font-size:13px;font-weight:700;color:{color};">{signo}{cant} {unidad}</span>
                    <span style="font-size:12px;font-weight:500;color:#0f172a;">{saldo} {unidad}</span>
                    <span>{bd_mot}</span>
                    <span style="font-size:11px;color:#94a3b8;">{fecha}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <p style="font-size:11px;color:#94a3b8;text-align:right;margin-top:8px;">
                Mostrando {len(movs)} movimiento{"s" if len(movs)!=1 else ""}
            </p>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error cargando movimientos: {e}")


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────

apply_global_styles()

if not st.session_state.get("authenticated", False):
    render_login()
    st.stop()

page = render_sidebar()

VIEWS = {
    "dashboard":   render_dashboard,
    "productos":   render_productos,
    "categorias":  render_categorias,
    "proveedores": render_proveedores,
    "ordenes":     render_ordenes,
    "operaciones": render_operaciones,
    "movimientos": render_movimientos,
}

try:
    VIEWS.get(page, render_dashboard)()
except Exception as e:
    st.error(f"No se pudo cargar esta sección. Por favor intenta nuevamente.")
    st.caption(f"Detalle técnico: {e}")