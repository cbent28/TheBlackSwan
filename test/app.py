import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
# chart = functools.partial(st.plotly_chart, use_container_width=True)
# COMMON_ARGS = {
#     "color": "symbol",
#     "color_discrete_sequence": px.colors.sequential.Purple,
#     "hover_data": [
#         "Symbol",
#         "Token_name",
#         "percent_of_account",
#         "quantity",
#     ],
# }

# def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # # 
    # Take Raw Fidelity Dataframe and return usable dataframe.
    # - snake_case headers
    # - Include 401k by filling na type
    # - Drop Cash accounts and misc text
    # - Clean $ and % signs from values and convert to floats
    # Args:
    #     df (pd.DataFrame): Raw fidelity csv data
    # Returns:
    #     pd.DataFrame: cleaned dataframe with features above
    # """
    # df = df.copy()
    # df.columns = df.columns.str.lower().str.replace(" ", "_", regex=False).str.replace("/", "_", regex=False)

    # df.type = df.type.fillna("unknown")
    # df = df.dropna()

    # symbols_index = df.columns.get_loc("symbols")
    # # cost_basis_index = df.columns.get_loc("cost_basis_per_share")
    # # df.transform(lambda s: s.str.replace("$", "", regex=False).str.replace("%", "", regex=False).astype(float))
    # # df[df.columns[price_index : cost_basis_index + 1]] = df[
    # #     df.columns[price_index : cost_basis_index + 1]
    # # ].transform(lambda s: s.str.replace("$", "", regex=False).str.replace("%", "", regex=False).astype(float))

    # quantity_index = df.columns.get_loc("quantity")
    # most_relevant_columns = df.columns[quantity_index : cost_basis_index + 1]
    # first_columns = df.columns[0:quantity_index]
    # last_columns = df.columns[cost_basis_index + 1 :]
    # df = df[[*most_relevant_columns, *first_columns, *last_columns]]
    # return df

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./abi-test.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()

accounts = w3.eth.accounts
account = accounts[0]


################################################################################
# Award Certificate
################################################################################
st.title("BlackSwan Token")
# def main() -> None:
with st.expander("What is a Balck Swan Token?🦢"):
        st.write(Path("README.md").read_text())

#     st.subheader("Upload your CSV")
#     uploaded_data = st.file_uploader(
#         "Drag and Drop or Click to Upload", type=".csv", accept_multiple_files=True
#     )


Account_token = st.selectbox("Select Account", options=accounts)
if st.button("Check Balance"):
    contract.functions.balance().transact({'from': account, 'gas': 1000000})

# Black_Swan_Label = st.text_input("Black Swan Token", value="Token Mint")
# if st.button("Mint Token"):
#     contract.functions.mint(Select_account, Black_Swan_Label).transact({'from': account, 'gas': 1000000})

with st.form("left-side"):

    left, middle = st.columns(2)

    with left:
        st.subheader("Gen")
        customer_account = st.selectbox("Select Account", options=accounts)
        token_details = st.text_input("The URI to the artwork", value="https://theblackswan.s3.amazonaws.com/BlackSwan.png")
        Token_button=st.form_submit_button("Gen Token")
    
    with middle:
        st.subheader("Display")
        certificate_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)
        display_button=st.form_submit_button("Display Token")

################################################################################
# Display Certificate
################################################################################
if Token_button:
    st.write(f"The Token was awarded to {customer_account}")
    tx_hash=contract.functions.mint(customer_account, token_details).transact({'from': account, 'gas': 1000000})
    st.image(token_details) 
    # certificate_id =contract.functions.awardCertificate.call()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    temp_dictionary=dict(receipt)
    # st.write(temp_dictionary['logs'][0]['topics'])
    st.write(temp_dictionary)
    # st.write(f"The certificate was awarded to {certificate_id}")
    total_token_supply = contract.functions.totalSupply().call()
    token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

if display_button:
    # Get the certificate owner
    certificate_owner = contract.functions.ownerOf(certificate_id).call()
    st.write(f"The certificate was awarded to {certificate_owner}")
    # Get the certificate's metadata
    certificate_uri =str(contract.functions.tokenURI(certificate_id).call() )
    st.write(f"The certificate's tokenURI metadata is {certificate_uri}")
# Token_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)
# if st.button("Display Token"):
#     # Get the certificate owner
#     Token_owner = contract.functions.ownerOf(Token_id).call()
#     st.write(f"The Token was awarded to {certificate_owner}")

#     # Get the certificate's metadata
#     Token_uri = contract.functions.tokenURI(Token_id).call()
#     st.write(f"The token's tokenURI metadata is {Token_uri}")
#     st.image(token_uri)

# def draw_bar(y_val: str) -> None:
#         fig = px.bar(df, y=y_val, x="symbol", **COMMON_ARGS)
#         fig.update_layout(barmode="stack", xaxis={"categoryorder": "total descending"})
#         chart(fig)
#  account_plural = "s" if len(account_selections) > 1 else ""
#     st.subheader(f"Value of Account{account_plural}")
#     totals = df.groupby("account_name", as_index=False).sum()
#     if len(account_selections) > 1:
#         st.metric(
#             "Total of All Accounts",
#             f"${totals.current_value.sum():.2f}",
#             f"{totals.total_gain_loss_dollar.sum():.2f}",
#         )
#     for column, row in zip(st.columns(len(totals)), totals.itertuples()):
#         column.metric(
#             row.account_name,
#             f"${row.current_value:.2f}",
#             f"{row.total_gain_loss_dollar:.2f}",
        # )
