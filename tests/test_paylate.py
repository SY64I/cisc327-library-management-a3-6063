import pytest
import pytest_mock
from unittest.mock import Mock
from services.library_service import (
    pay_late_fees
)
from services.payment_service import PaymentGateway
'''
This script is designed to test the library_service.py pay_late_fees function.
NOTE: There is a statement inside an if statement in this function I cannot test here, since it creates a real PaymentGateway class, which is prohibited.
'''

def test_payment_valid(mocker):
    """Test a successful late fee payment."""

    # First, stub return values for calculate_late_fee and get_book_by_id
    test_fees = {'fee_amount': 1.5}
    test_book = {'title' : '3-Day Late'}
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)

    # Then, mock a payment gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_613483_time", "Payment of $1.50 processed successfully")

    # Then test the function
    success, msg, txn = pay_late_fees("613483", 17, mock_gateway)
    
    # Then assert message, assert success and assert the mock was called once
    assert success
    assert 'successful' in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="613483", amount=1.5, description=f"Late fees for '{test_book['title']}'")


def test_payment_invalid_patron(mocker):
    """Test a payment with being declined with invalid patron ID"""

    # Mock a payment gateway to encounter an error
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_1_time", "Payment of $3.00 processed successfully")

    # Test the function
    success, msg, txn = pay_late_fees("1", 17, mock_gateway)
    
    # Then assert success. For this test, additionally assert the mock was used by using assert_called_once or assert_called_with
    assert not success
    assert 'patron ID' in msg
    mock_gateway.process_payment.assert_not_called()


def test_payment_invalid_calculation_error(mocker):
    """Test a payment with being declined due to an invalid late fee"""

    # First, stub return values for calculate_late_fee to simulate no late fee
    test_fees = None
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)

    # Then, mock a payment gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_613483_time", "Payment of None processed successfully")

    # Then test the function
    success, msg, txn = pay_late_fees("613483", 17, mock_gateway)
    
    # Then assert message, assert success and assert the mock was not called
    assert 'Unable to calculate late fees' in msg
    assert success == False
    mock_gateway.process_payment.assert_not_called()

def test_payment_invalid_no_late_fee(mocker):
    """Test a payment with being declined due to no late fee existing"""

    # First, stub return values for calculate_late_fee to simulate no late fee
    test_fees = {'fee_amount': 0}
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)

    # Then, mock a payment gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_613483_time", "Payment of $0.00 processed successfully")

    # Then test the function
    success, msg, txn = pay_late_fees("613483", 17, mock_gateway)
    
    # Then assert message, assert success and assert the mock was not called
    assert not success
    assert 'No late fees' in msg
    mock_gateway.process_payment.assert_not_called()


def test_payment_invalid_book_id(mocker):
    """Test a payment with being declined due to no book being found"""

    # Stub the function values required
    test_fees = {'fee_amount': 3.5}
    test_book = None
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)

    # Then, mock a payment gateway to return a declined payment
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_613483_time", "Payment of $4.50 processed successfully")

    # Test the function
    success, msg, txn = pay_late_fees("613483", 17, mock_gateway)
    
    # Then assert message, assert success and assert the mock was not called
    assert 'Book not found' in msg
    assert success == False
    mock_gateway.process_payment.assert_not_called()


def test_payment_invalid_failed_payment(mocker):
    """Test a payment with being declined by the gateway"""

    # Stub the function values required
    test_fees = {'fee_amount': 1}
    test_book = {'title' : '2-Day Late'}
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)

    # Then, mock a payment gateway to return a declined payment
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "-1", "Payment not processed")

    # Test the function
    success, msg, txn = pay_late_fees("613483", 17, mock_gateway)
    
    # Then assert message, assert success and assert the mock was called once
    assert not success
    assert 'failed' in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="613483", amount=1, description=f"Late fees for '{test_book['title']}'")

def test_payment_invalid_processing_error(mocker):
    """Test a payment with being declined due to a network error"""

    # Stub the function values required
    test_fees = {'fee_amount': 0.5}
    test_book = {'title' : '1-Day Late'}
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)

    # Then, mock a payment gateway to encounter an error
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = False

    # Test the function
    success, msg, txn = pay_late_fees("613483", 17, mock_gateway)
    
    # Then assert message, assert success and assert the mock was called once
    assert not success
    assert 'processing error' in msg
    mock_gateway.process_payment.assert_called_once_with(patron_id="613483", amount=0.5, description=f"Late fees for '{test_book['title']}'")

