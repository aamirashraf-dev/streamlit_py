import streamlit as st

st.set_page_config(page_title="Lånekalkylator (Sverige)", page_icon="🏠", layout="centered")
st.title("🏠 Lånekalkylator – grundnivå")
st.write("Enkel kalkyl med ränta per månad, före/efter 30% ränteavdrag. Ingen amortering.")

with st.sidebar:
    st.header("Inmatning")
    price = st.number_input("Bostadspris (kr)", min_value=0, step=50000, value=3_000_000)
    rate_pct = st.number_input("Ränta (% per år)", min_value=0.0, step=0.1, value=4.0, format="%.2f")
    use_default = st.checkbox("Använd standard handpenning 15%", value=True)
    if use_default:
        down_payment = 0.15 * price
    else:
        down_payment = st.number_input("Egen insats (kr)", min_value=0, step=10000, value=300_000)
    monthly_fee = st.number_input("Månadsavgift (kr/mån) – valfritt", min_value=0, step=100, value=0)

down_payment = min(down_payment, price)        # skydd
loan = max(price - down_payment, 0)

monthly_interest = (loan * (rate_pct / 100)) / 12 if loan > 0 else 0.0
monthly_interest_after = monthly_interest * 0.70  # förenklat 30% avdrag

total_before = monthly_interest + monthly_fee
total_after  = monthly_interest_after + monthly_fee

down_pct = (down_payment / price * 100) if price > 0 else 0.0
ltv_pct  = (loan / price * 100) if price > 0 else 0.0  # belåningsgrad

st.subheader("Resultat")
c1, c2 = st.columns(2)
with c1:
    st.metric("Insats (kr)", f"{int(down_payment):,}".replace(",", " "))
    st.metric("Insats (%)", f"{down_pct:.1f}%")
with c2:
    st.metric("Lån (kr)", f"{int(loan):,}".replace(",", " "))
    st.metric("Belåningsgrad", f"{ltv_pct:.1f}%")

st.divider()
c3, c4 = st.columns(2)
with c3:
    st.metric("Räntekostnad/mån (före avdrag)", f"{int(round(monthly_interest)): ,} kr".replace(",", " "))
with c4:
    st.metric("Räntekostnad/mån (efter avdrag)", f"{int(round(monthly_interest_after)): ,} kr".replace(",", " "))

if monthly_fee > 0:
    st.divider()
    st.write("**Total boendekostnad/mån** (inkl. månadsavgift):")
    st.write(f"- Före ränteavdrag: **{int(round(total_before)): ,} kr**".replace(",", " "))
    st.write(f"- Efter ränteavdrag: **{int(round(total_after)): ,} kr**".replace(",", " "))

st.caption("Förenklad modell: ingen amortering. Ränteavdrag antas 30% rakt av.")