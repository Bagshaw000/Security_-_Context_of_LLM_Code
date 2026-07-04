import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import Dict, Optional, List, Final
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TransactionType(Enum):
    WITHDRAWAL = auto()
    DEPOSIT = auto()
    BALANCE_INQUIRY = auto()
    TRANSFER = auto()

class TransactionStatus(Enum):
    PENDING = auto()
    SUCCESS = auto()
    FAILED = auto()
    REVERSED = auto()

class ATMError(Exception):
    
    pass

class InsufficientFundsError(ATMError):
    pass

class AuthenticationError(ATMError):
    pass

class InvalidAccountError(ATMError):
    pass

@dataclass(frozen=True)
class Card:
    card_number: str
    encrypted_pin: str  
    account_id: str
    expiry_date: datetime

@dataclass
class Account:
    account_id: str
    owner_name: str
    balance: Decimal = Decimal('0.00')

    def deduct(self, amount: Decimal):
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal.")
        self.balance -= amount

    def add(self, amount: Decimal):
        self.balance += amount

@dataclass
class TransactionRecord:
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    account_id: str = ""
    atm_id: str = ""
    amount: Decimal = Decimal('0.00')
    tx_type: TransactionType = TransactionType.BALANCE_INQUIRY
    status: TransactionStatus = TransactionStatus.PENDING

class CentralBankServer:
    
    def __init__(self):
        self._accounts: Dict[str, Account] = {}
        self._cards: Dict[str, Card] = {}
        self._transaction_history: List[TransactionRecord] = []

    def register_account(self, account: Account):
        self._accounts[account.account_id] = account

    def register_card(self, card: Card):
        self._cards[card.card_number] = card

    def authenticate(self, card_number: str, pin: str) -> Optional[Card]:
        card = self._cards.get(card_number)
        
        if card and card.encrypted_pin == pin:
            return card
        return None

    def get_balance(self, account_id: str) -> Decimal:
        if account_id not in self._accounts:
            raise InvalidAccountError("Account not found.")
        return self._accounts[account_id].balance

    def process_transaction(self, record: TransactionRecord) -> TransactionStatus:
        account = self._accounts.get(record.account_id)
        if not account:
            record.status = TransactionStatus.FAILED
            return record.status

        try:
            if record.tx_type == TransactionType.WITHDRAWAL:
                account.deduct(record.amount)
            elif record.tx_type == TransactionType.DEPOSIT:
                account.add(record.amount)
            
            record.status = TransactionStatus.SUCCESS
            self._transaction_history.append(record)
            return record.status
        except ATMError as e:
            logger.error(f"Transaction failed: {e}")
            record.status = TransactionStatus.FAILED
            return record.status

class ATMController:
    
    def __init__(self, atm_id: str, bank_server: CentralBankServer):
        self.atm_id: Final[str] = atm_id
        self._server: CentralBankServer = bank_server
        self._current_card: Optional[Card] = None
        self._authenticated: bool = False
        self._cash_inventory: Decimal = Decimal('10000.00') 

    def insert_card(self, card_number: str, pin: str) -> bool:
        card = self._server.authenticate(card_number, pin)
        if card:
            self._current_card = card
            self._authenticated = True
            logger.info(f"Card {card_number} authenticated at ATM {self.atm_id}")
            return True
        logger.warning(f"Failed auth attempt for card {card_number}")
        return False

    def check_balance(self) -> Decimal:
        if not self._authenticated or not self._current_card:
            raise AuthenticationError("User not authenticated.")
        
        return self._server.get_balance(self._current_card.account_id)

    def withdraw_cash(self, amount: Decimal) -> bool:
        if not self._authenticated or not self._current_card:
            raise AuthenticationError("User not authenticated.")

        if amount > self._cash_inventory:
            raise ATMError("ATM out of cash.")

        tx = TransactionRecord(
            account_id=self._current_card.account_id,
            atm_id=self.atm_id,
            amount=amount,
            tx_type=TransactionType.WITHDRAWAL
        )

        status = self._server.process_transaction(tx)
        if status == TransactionStatus.SUCCESS:
            self._cash_inventory -= amount
            logger.info(f"Dispensed {amount} from ATM {self.atm_id}")
            return True
        return False

    def deposit_funds(self, amount: Decimal) -> bool:
        if not self._authenticated or not self._current_card:
            raise AuthenticationError("User not authenticated.")

        tx = TransactionRecord(
            account_id=self._current_card.account_id,
            atm_id=self.atm_id,
            amount=amount,
            tx_type=TransactionType.DEPOSIT
        )

        status = self._server.process_transaction(tx)
        if status == TransactionStatus.SUCCESS:
            self._cash_inventory += amount
            logger.info(f"Accepted deposit of {amount} at ATM {self.atm_id}")
            return True
        return False

    def eject_card(self):
        self._current_card = None
        self._authenticated = False
        logger.info("Session ended. Card ejected.")

def run_system_demo():
    
    bank_backend = CentralBankServer()
    
    
    acc1 = Account(account_id="ACC-7788", owner_name="Brad Principal", balance=Decimal('5000.00'))
    card1 = Card(card_number="1234-5678-9012", encrypted_pin="1234", account_id="ACC-7788", expiry_date=datetime(2028, 1, 1))
    
    bank_backend.register_account(acc1)
    bank_backend.register_card(card1)

    
    atm = ATMController(atm_id="SEA-001", bank_server=bank_backend)

    
    print(f"--- ATM Session Start ---")
    if atm.insert_card("1234-5678-9012", "1234"):
        current_bal = atm.check_balance()
        print(f"Initial Balance: ${current_bal}")
        
        withdrawal_amount = Decimal('200.00')
        if atm.withdraw_cash(withdrawal_amount):
            print(f"Successfully withdrew ${withdrawal_amount}")
            print(f"New Balance: ${atm.check_balance()}")
        
        atm.eject_card()
    else:
        print("Authentication Failed.")
    print(f"--- ATM Session End ---")

if __name__ == "__main__":
    run_system_demo()