import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background:#ffffff; border:1px solid #525252; border-radius:14px; padding:18px 16px; margin-bottom:16px;">
            <h3 style="margin:0 0 12px; color:#111111; font-size:1rem; font-weight:600;">{name}</h3>
            <p style="color:#6b7280; margin:0; font-size:0.78rem;">
                Code:
                <span style="background:#e6e9ff; color:#4f46e5; padding:3px 7px; border-radius:4px; margin-left:3px;">{code}</span>
                <span style="margin-left:5px;">| Section: {section}</span>
            </p>
    """

    if stats:
        html += '<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:10px;">'
        for icon, label, value in stats:
            html += f'<div style="background:#fff5f8; color:#302a35; padding:4px 8px; border-radius:4px; font-size:0.7rem;">{icon} <b>{value}</b> {label}</div>'
        html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()