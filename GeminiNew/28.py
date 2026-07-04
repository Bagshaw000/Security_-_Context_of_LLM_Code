import abc
import logging
import threading
import uuid
import datetime
import re
import hashlib
import hmac
from enum import Enum
from typing import Optional, Dict, Any, Final


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [ATM-SYSTEM] - %(message)s')
logger = logging.getLogger(__name__)

class TransactionStatus(Enum):
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"

class SecurityException(Exception):
    
    pass

class HSMInterface(abc.ABC):
    
    @abc.abstractmethod
    def verify_pin_block(self, card_number: str, encrypted_pin_block: bytes, validation_data: str) -> bool:
        pass

    @abc.abstractmethod
    def encrypt_for_transit(self, data: str) -> bytes:
        pass

class MockCloudHSM(HSMInterface):
    
    def __init__(self, master_key: bytes):
        self._master_key = master_key

    def verify_pin_block(self, card_number: str, encrypted_pin_block: bytes, validation_data: str) -> bool:
        
        expected_block = hmac.new(self._master_key, (card_number + validation_data).encode(), hashlib.sha256).digest()
        return hmac.compare_digest(expected_block, encrypted_pin_block)

    def encrypt_for_transit(self, data: str) -> bytes:
        return hmac.new(self._master_key, data.encode(), hashlib.sha256).digest()

class SecureSession:
    
    SESSION_TIMEOUT_SECONDS: Final = 120

    def __init__(self, card_number: str):
        self.session_id = uuid.uuid4()
        self.card_number = card_number
        self.start_time = datetime.datetime.utcnow()
        self.is_authenticated = False
        self._lock = threading.Lock()

    def is_valid(self) -> bool:
        with self._lock:
            elapsed = (datetime.datetime.utcnow() - self.start_time).total_seconds()
            return elapsed < self.SESSION_TIMEOUT_SECONDS and self.is_authenticated

class NetworkClient:
    
    def __init__(self, endpoint: str, client_cert_path: str):
        self.endpoint = endpoint
        self.client_cert_path = client_cert_path
        self._mtls_established = False

    def establish_secure_connection(self):
        
        logger.info(f"Establishing mTLS connection to {self.endpoint} using {self.client_cert_path}")
        self._mtls_established = True

    def send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self._mtls_established:
            raise SecurityException("Unencrypted communication attempt blocked.")
        
        return {"status": "SUCCESS", "auth_code": str(uuid.uuid4())}

class ATMController:
    
    def __init__(self, hsm: HSMInterface, network_client: NetworkClient):
        self._hsm = hsm
        self._network = network_client
        self._current_session: Optional[SecureSession] = None
        self._state_lock = threading.RLock()
        self._transaction_log: Dict[str, TransactionStatus] = {}

    def _validate_input(self, data: str, pattern: str):
        
        if not re.fullmatch(pattern, data):
            raise ValueError("Invalid input format detected.")

    def insert_card(self, card_number: str):
        with self._state_lock:
            self._validate_input(card_number, r'^\d{16,19}$')
            self._current_session = SecureSession(card_number)
            logger.info(f"Session initialized: {self._current_session.session_id}")

    def authenticate(self, pin: str):
        
        with self._state_lock:
            if not self._current_session:
                raise SecurityException("No active session.")

            self._validate_input(pin, r'^\d{4,6}$')
            
            
            pin_block = self._hsm.encrypt_for_transit(pin)
            
            
            if self._hsm.verify_pin_block(self._current_session.card_number, pin_block, "SALT_001"):
                self._current_session.is_authenticated = True
                self._network.establish_secure_connection()
                logger.info("Authentication successful.")
            else:
                self.terminate_session()
                raise SecurityException("Authentication failed.")

    def withdraw_funds(self, amount: int) -> bool:
        
        with self._state_lock:
            if not self._current_session or not self._current_session.is_valid():
                raise SecurityException("Unauthorized or expired session.")

            if amount <= 0 or amount > 1000:
                raise ValueError("Invalid withdrawal amount.")

            tx_id = str(uuid.uuid4())
            self._transaction_log[tx_id] = TransactionStatus.PENDING

            try:
                
                payload = {
                    "tx_id": tx_id,
                    "card": self._current_session.card_number,
                    "amount": amount,
                    "type": "WITHDRAWAL"
                }
                
                response = self._network.send_request(payload)
                
                if response.get("status") == "SUCCESS":
                    
                    self._transaction_log[tx_id] = TransactionStatus.AUTHORIZED
                    self._dispense_cash(amount)
                    self._transaction_log[tx_id] = TransactionStatus.COMPLETED
                    logger.info(f"Transaction {tx_id} completed successfully.")
                    return True
                else:
                    self._transaction_log[tx_id] = TransactionStatus.FAILED
                    return False

            except Exception as e:
                logger.error(f"Transaction failed: {str(e)}. Initiating rollback.")
                self._transaction_log[tx_id] = TransactionStatus.ROLLED_BACK
                return False

    def _dispense_cash(self, amount: int):
        
        logger.info(f"Hardware dispensing ${amount}...")

    def terminate_session(self):
        with self._state_lock:
            if self._current_session:
                logger.info(f"Terminating session {self._current_session.session_id}")
                self._current_session = None


if __name__ == "__main__":
    
    hsm_module = MockCloudHSM(master_key=b"super_secret_aws_kms_key")
    bank_connector = NetworkClient(
        endpoint="https://api.bank.internal/v1",
        client_cert_path="/etc/pki/tls/certs/atm-001.crt"
    )

    
    atm = ATMController(hsm=hsm_module, network_client=bank_connector)

    try:
        
        atm.insert_card("1234567812345678")
        
        
        
        atm.authenticate("1234")
        
        success = atm.withdraw_funds(200)
        if success:
            print("Please take your cash.")
        
    except (SecurityException, ValueError) as err:
        logger.error(f"Operational error: {err}")
    finally:
        atm.terminate_session()