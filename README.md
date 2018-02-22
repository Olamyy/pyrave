# Pyrave

Pyrave is a python wrapper for the flutterwave's [rave](http://rave.frontendpwc.com/) payment platform 

It currently supports the following features:

*  Account charge (NG Banks)

* Account charge (International for US and ZAR).

* Card Charge (Bake in support for 3DSecure/PIN).

* Encryption

* Transaction status check (Normal requery flow and xrequery).

* Retry transaction status check flow.

* Preauth -> Capture -> Refund/void.

* Support for USSD and Mcash (Alternative payment methods).

* List of banks for NG Account charge. (Get banks list).

* Get fees endpoint.

* Integrity Checksum (https://flutterwavedevelopers.readme.io/docs/checksum).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Set Up

Go to [rave](http://rave.frontendpwc.com/) and sign up.
This would provide you with a public and private authorization key which would be used throughout the library.
Store these authorization keys in your environment as `RAVE_PUBLIC_KEY` for the public key and `RAVE_SECRET_KEY`.
    

### Installing

``` bash
pip install -U pyrave
```


Upon completion, try to import the library with

``` python
import pyrave
```

If the installation was successful, the code above should run without any error.

If an error like ```No module named pyrave``` pops up, then the installation was not successfull. You can either raise an issue here to get it looked at or attempt to reinstall it.


##Usage

1. Payment

The payment class was made simple enough to cover the following rave actions:

````python
from pyrave import Payment
   
rave_payment = Payment()

data = {...}

````
A. Payment with card and account
    
    
```python
## Payment with card and account
payment_with_card = rave_payment.pay(using="card", * * data)
payment_with_account = rave_payment.pay(using="account", * * data)
```
B. Getting encrypted data
To get the encrypted data, call the Payment class' `get_encrypted_data` method. This would return a tuple of data
```python
encrypted_data = rave_payment.get_encrypted_data(using="account", * * data)
```

An alternative approach to doing this is to call the pay method and pass the return_encrypted boolean as True

```python
encrypted_data = rave_payment.pay(using="card", return_encrypted=True , * * data)
```

In both cases, if the request was successful, you should be able to get each one of the encryption details by indexing `encrypted_data`


C. Charge Validation

To validate a charge, call the `validate_charge` method and pass the `reference` and `otp` as parameter. You can select the method that applies most to your transaction.
```python
validate_charge = rave_payment.validate_charge("reference", "otp", method="card")
```


D. Transaction Verification

To verify a transaction, call the `verify_transaction` method and pass the transaction reference.
```python
transaction_verification = rave_payment.verify_transaction("reference", "otp", method="card")
```

E. Disbursements

To make disbursements, call the `disburse` method and pass the `bank_code`, `account_number`, `currency`, `amount` as parameters

```python
disbursements = rave_payment.disburse("bank_code", "account_number", "currency", "amount")
```
F. Preauthorization Capture
To capture preauthorization, call the `capture_preauthorised_transaction` method and pass the `transaction_reference` as parameter
```python
preauthorization = rave_payment.capture_preauthorised_transaction("bank_code", "account_number", "currency", "amount")
```

G. Transaction Refund or Void
```python
refund_or_void = rave_payment.refund_or_void_transaction("bank_code", "account_number", "currency", "amount")
```

H. Charge Tokenization 
```python
tokenize = rave_payment.tokenize_charge(* * data)
```

I. Refund
```python
refud = rave_payment.refund(reference_id="reference_id")
```


2. Transaction
The transaction Class provides support for the following rave functions:
````python
from pyrave import Transaction
   
rave_transaction = Transaction()

data = {...}
````
A. Verify Transaction

```python
verify = rave_transaction.verify_transaction(* * data)
```

B. Verify Transaction with xrequery
```python
verify = rave_transaction.verify_transaction_with_xrequery(* * data)
```

C. Get Recurrent Transactions
```python
verify = rave_transaction.get_reccurent_transactions()
```
D. Get Recurrent Transaction
```python
verify = rave_transaction.get_reccurent_transaction(transaction_id="your transaction_id")
```
E. Stop Recurrent Transactions
```python
verify = rave_transaction.get_reccurent_transaction(transaction_data_id="your transaction_data_id")
```


3. Misc
The Misc class provides support for the following rave functions:
````python
from pyrave import Misc
   
misc = Misc()
````

A. Get list of banks
````python
banks = misc.get_banks()
````

B. Get fees
````python
banks = misc.get_fee(amount="your amount", currency="your currency", ptype="your ptype", card6="card's number")
````


B. Get Exchange Rates
````python
banks = misc.get_exchange_rates(origin_currency="your origin currency", destination_currency="your destination currency", amount=None)
````


## Contributing

To contribute, fork the repo, make your  changes and create a pull request.


##Todo
 More Tests

## Authors

*  [Olamilekan Wahab](https://github.com/Olamyy)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


