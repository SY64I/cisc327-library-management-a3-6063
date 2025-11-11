import pytest
from unittest.mock import Mock
from services.library_service import (
    refund_late_fee_payment
)
from services.payment_service import PaymentGateway
'''
This script is designed to test the library_service.py refund_late_fee_payment function.
NOTE: There is a statement inside an if statement in this function I cannot test here, since it creates a real PaymentGateway class, which is prohibited.
'''

def test_refund_valid():
    """Test successful late fee refund"""
    # Format: transaction id, with txn_### - amount, as float - PaymentGateway
    # Function only requires PaymentGateway to be mocked.
    test_txn = "txn_789"
    test_amount = 6.5
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $6.50 processed successfully. Refund ID: refund_txn_789_time")

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert success
    assert "processed successfully" in msg
    mock_gateway.refund_payment.assert_called_once_with(test_txn, test_amount)


def test_refund_invalid_transaction_id():
    """Test a refund with being declined due to an invalid transaction id"""
    
    test_txn = "transaction"
    test_amount = 6.5
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $6.50 processed successfully. Refund ID: refund_transaction_time")

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert not success
    assert "transaction" in msg
    mock_gateway.process_payment.assert_not_called()

def test_refund_invalid_amount_negative():
    """Test a refund with being declined due to a negative refund amount"""

    test_txn = "txn_789"
    test_amount = -3.5
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $-3.50 processed successfully. Refund ID: refund_txn_789_time")

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert not success
    assert "greater than 0" in msg
    mock_gateway.process_payment.assert_not_called()

def test_refund_invalid_amount_zero():
    """Test a refund with being declined due to a refund amount of zero"""

    test_txn = "txn_789"
    test_amount = 0
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $0.00 processed successfully. Refund ID: refund_txn_789_time")

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert not success
    assert "greater than 0" in msg
    mock_gateway.process_payment.assert_not_called()

def test_refund_invalid_amount_exceed_max():
    """Test a refund with being declined due to a refund amount of above the max 15$ limit"""

    test_txn = "txn_789"
    test_amount = 20.5
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund of $20.50 processed successfully. Refund ID: refund_txn_789_time")

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert not success
    assert "exceeds maximum" in msg
    mock_gateway.process_payment.assert_not_called()

def test_refund_invalid_failed_refund():
    """Test a refund with being declined by the gateway"""

    test_txn = "txn_789"
    test_amount = 6.5
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Refund not processed")

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert not success
    assert "Refund failed" in msg
    mock_gateway.refund_payment.assert_called_once_with(test_txn, test_amount)

def test_refund_invalid_processing_error():
    """Test a refund with being declined by the gateway"""

    test_txn = "txn_789"
    test_amount = 6.5
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = False

    success, msg = refund_late_fee_payment(test_txn, test_amount, mock_gateway)
    assert not success
    assert 'processing error' in msg
    mock_gateway.refund_payment.assert_called_once_with(test_txn, test_amount)
