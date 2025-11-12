import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Splitter", page_icon="🧮")
st.title("🧮 Expense Splitter")

def settle_transactions(df, total_override=None):
    total = total_override if total_override and total_override > 0 else float(df["Contributed"].sum())
    n = len(df)
    share = round(total / n, 2) if n else 0.0

    df = df.copy()
    df["Fair Share"] = share
    df["Balance"] = (df["Contributed"] - df["Fair Share"]).round(2)

    creditors = [(r.Name, float(r.Balance)) for r in df.itertuples(index=False) if r.Balance > 0]
    debtors   = [(r.Name, float(-r.Balance)) for r in df.itertuples(index=False) if r.Balance < 0]

    creditors.sort(key=lambda x: x[1], reverse=False)
    debtors.sort(key=lambda x: x[1], reverse=False)

    i, j = 0, 0
    txns = []
    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]
        pay = round(min(d_amt, c_amt), 2)
        if pay > 0:
            txns.append((d_name, c_name, pay))
        d_amt = round(d_amt - pay, 2)
        c_amt = round(c_amt - pay, 2)
        debtors[i]   = (d_name, d_amt)
        creditors[j] = (c_name, c_amt)
        if d_amt == 0: i += 1
        if c_amt == 0: j += 1

    per_person_msgs = {name: [] for name in df["Name"]}
    for debtor, creditor, amt in txns:
        per_person_msgs[debtor].append(f"owes {creditor} ₹{amt:,.2f}")

    for name in per_person_msgs:
        if not per_person_msgs[name]:
            per_person_msgs[name] = ["owes No One"]

    return df, txns, per_person_msgs, share, total

with st.form("splitter"):
    total = st.number_input("Total amount (optional if you fill contributions)", min_value=0.0, step=100.0, value=0.0)
    n = st.number_input("Number of people", min_value=1, step=1, value=2)
    df = st.data_editor(
        pd.DataFrame({"Name": [f"Person {i+1}" for i in range(int(n))],
                      "Contributed": [0.0]*int(n)}),
        use_container_width=True
    )
    submit = st.form_submit_button("Calculate")

if submit:
    if len(df) == 0:
        st.warning("Add at least one person.")
    else:
        res_df, txns, per_person_msgs, share, eff_total = settle_transactions(df, total_override=total)
        st.subheader("Balances")
        st.dataframe(res_df, use_container_width=True)
        st.write(f"Effective total: **₹{eff_total:,.2f}** · Fair share per person: **₹{share:,.2f}**")

        st.subheader("Who owes whom")
        if not txns:
            st.success("All settled. No one owes anyone. 🎉")
        else:
            tx_table = pd.DataFrame(txns, columns=["From (Debtor)", "To (Creditor)", "Amount"])
            st.dataframe(tx_table, use_container_width=True)

        st.subheader("Per-person summary")
        summary_rows = [{"Name": name, "Summary": "; ".join(lines)} for name, lines in per_person_msgs.items()]
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
