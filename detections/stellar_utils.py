# detections/stellar_utils.py
from stellar_sdk import Keypair, Server, TransactionBuilder, Network, Asset
from stellar_sdk.exceptions import BadRequestError, NotFoundError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

STELLAR_SECRET_KEY = settings.STELLAR_SECRET_KEY
STELLAR_PUBLIC_KEY = settings.STELLAR_PUBLIC_KEY
STELLAR_NETWORK = (Network.TESTNET_NETWORK_PASSPHRASE 
                   if settings.STELLAR_NETWORK == 'TESTNET' 
                   else Network.PUBLIC_NETWORK_PASSPHRASE)

SERVER_URL = ("https://horizon-testnet.stellar.org" 
              if settings.STELLAR_NETWORK == 'TESTNET' 
              else "https://horizon.stellar.org")

server = Server(SERVER_URL)

def create_transaction(destination: str, amount: str, memo: str = "Reward Transaction") -> dict:
    """
    Create and submit a Stellar transaction.

    Args:
    destination (str): The destination Stellar address.
    amount (str): The amount of XLM to send.
    memo (str, optional): Transaction memo. Defaults to "Reward Transaction".

    Returns:
    dict: The server's response to the transaction submission.

    Raises:
    BadRequestError: If the transaction is invalid.
    NotFoundError: If the destination account doesn't exist.
    """
    source_keypair = Keypair.from_secret(STELLAR_SECRET_KEY)
    source_account = server.load_account(source_keypair.public_key)
    
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=STELLAR_NETWORK,
            base_fee=server.fetch_base_fee()
        )
        .add_text_memo(memo)
        .append_payment_op(
            destination=destination,
            amount=amount,
            asset=Asset.native()
        )
        .set_timeout(30)
        .build()
    )
    
    transaction.sign(source_keypair)
    response = server.submit_transaction(transaction)
    return response

def reward_user_with_stellar(stellar_address: str, amount: str):
    try:
        response = create_transaction(stellar_address, amount)
        logger.info(f"Transaction successful. Hash: {response['hash']}")
        return response
    except (BadRequestError, NotFoundError) as e:
        logger.error(f"Transaction failed: {str(e)}")
        return None