Pyrave
======

Pyrave is a python wrapper for the flutterwave’s
`rave <http://rave.frontendpwc.com/>`__ payment platform

It currently supports the following features:

-  Account charge (NG Banks)

-  Account charge (International for US and ZAR).

-  Card Charge (Bake in support for 3DSecure/PIN).

-  Encryption

-  Transaction status check (Normal requery flow and xrequery).

-  Retry transaction status check flow.

-  Preauth -> Capture -> Refund/void.

-  Support for USSD and Mcash (Alternative payment methods).

-  List of banks for NG Account charge. (Get banks list).

-  Get fees endpoint.

-  Integrity Checksum
   (https://flutterwavedevelopers.readme.io/docs/checksum).

Getting Started
---------------

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes.

Set Up
~~~~~~

Go to `rave <http://rave.frontendpwc.com/>`__ and sign up. This would
provide you with a public and private authorization key which would be
used throughout the library. Store these authorization keys in your
environment as ``RAVE_PUBLIC_KEY`` for the public key and
``RAVE_SECRET_KEY``.

Installing
~~~~~~~~~~

.. code:: bash

    pip install -U pyrave

Upon completion, try to import the library with

.. code:: python

    import pyrave

If the installation was successful, the code above should run without
any error.

If an error like ``No module named pyrave`` pops up, then the
installation was not successfull. You can either raise an issue here to
get it looked at or attempt to reinstall it.

Usage
-----

Payment
-------

The payment class was made simple enough to cover the following rave
actions:

.. code:: python

    from pyrave import Payment

    rave_payment = Payment()

    data = {...}

Payment with card and account
'''''''''''''''''''''''''''''

.. code:: python

    ## Payment with card and account
    payment_with_card = rave_payment.pay(using="card", **data)
    payment_with_account = rave_payment.pay(using="account", **data)

Getting encrypted data
''''''''''''''''''''''

To get the encrypted data, call the Payment class’
``get_encrypted_data`` method. This would return a tuple of data

.. code:: python

    encrypted_data = rave_payment.get_encrypted_data(using="account", **data)

An alternative approach to doing this is to call the pay method and pass
the return_encrypted boolean as True

.. code:: python

    encrypted_data = rave_payment.pay(using="card", return_encrypted=True , **data)

In both cases, if the request was successful, you should be able to get
each one of the encryption details by indexing ``encrypted_data``

Charge Validation
'''''''''''''''''

To validate a charge, call the ``validate_charge`` method and pass the
``reference`` and ``otp`` as parameter. You can select the method that
applies most to your transaction.

.. code:: python

    validate_charge = rave_payment.validate_charge("reference", "otp", method="card")

Transaction Verification
''''''''''''''''''''''''

To verify a transaction, call the ``verify_transaction`` method and pass
the transaction reference.

.. code:: python

    transaction_verification = rave_payment.verify_transaction("reference", "otp", method="card")

Disbursements
'''''''''''''

To make disbursements, call the ``disburse`` method and pass the
``bank_code``, ``account_number``, ``currency``, ``amount`` as
parameters

.. code:: python

    disbursements = rave_payment.disburse("bank_code", "account_number", "currency", "amount")

Charge Tokenization
'''''''''''''''''''

.. code:: python

    tokenize = rave_payment.tokenize_charge(**data)

Refund
''''''

.. code:: python

    refud = rave_payment.refund(reference_id="reference_id")

Transaction
-----------

The transaction Class provides support for the following rave functions:

.. code:: python

    from pyrave import Transaction

    rave_transaction = Transaction()

    data = {...}

Verify Transaction
''''''''''''''''''

.. code:: python

    verify = rave_transaction.verify_transaction(**data)

Verify Transaction with xrequery
''''''''''''''''''''''''''''''''

.. code:: python

    verify = rave_transaction.verify_transaction_with_xrequery(**data)

Get Recurrent Transactions
''''''''''''''''''''''''''

.. code:: python

    verify = rave_transaction.get_reccurent_transactions()

Get Recurrent Transaction
'''''''''''''''''''''''''

.. code:: python

    verify = rave_transaction.get_reccurent_transaction(transaction_id="your transaction_id")

Stop Recurrent Transactions
'''''''''''''''''''''''''''

.. code:: python

    verify = rave_transaction.get_reccurent_transaction(transaction_data_id="your transaction_data_id")

Miscellaneous features
----------------------

The Misc class provides support for the following rave functions:

.. code:: python

    from pyrave import Misc

    misc = Misc()

Get list of banks
'''''''''''''''''

.. code:: python

    banks = misc.get_banks()

Get fees
''''''''

.. code:: python

    banks = misc.get_fee(amount="your amount", currency="your currency", ptype="your ptype", card6="card's number")

Get Exchange Rates
''''''''''''''''''

.. code:: python

    rates = misc.get_exchange_rates(origin_currency="your origin currency", destination_currency="your destination currency", amount=None)

Preauth
-------

.. code:: python

    from pyrave import Preauth

    preauth = Preauth()

Preauthorize card
^^^^^^^^^^^^^^^^^

Before preauthorizing a card, get the client and alg parameters by
calling the ``get_encrypted_data`` method of the Payment class.

.. code:: python

    preauth.preauthorise_card(client="client id", algo="algo used")

Preauthorization Capture
''''''''''''''''''''''''

To capture preauthorization, call the
``capture_preauthorised_transaction`` method and pass the
``transaction_reference`` as parameter

.. code:: python

    preauthorization = preauth.capture_preauthorised_transaction(transaction_reference="your transaction reference")

Transaction Refund or Void
''''''''''''''''''''''''''

.. code:: python

    refund_or_void = preauth.refund_or_void_transaction(action="refund or void", reference_id="your reference id")

Contributing
------------

To contribute, fork the repo, make your changes and create a pull
request.

Todo
----

More Tests

Authors
-------

-  `Olamilekan Wahab <https://github.com/Olamyy>`__

License
-------

This project is licensed under the MIT License - see the
`LICENSE.md <LICENSE.md>`__ file for details
