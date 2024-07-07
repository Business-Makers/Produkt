"""
A class that provides PayPal payment integration for an application.

This class uses the PayPal SDK to create and execute payments. It configures the SDK with the necessary credentials and offers methods for creating and executing payments.

"""
"""
Initializes the Paypal class and configures the PayPal SDK with credentials.

Args:
    None
"""
"""
Creates a PayPal payment.

Creates a payment with the specified parameters and returns the approval_url if the payment is successfully created, or an error if something goes wrong.

Args:
    currency (str): The currency of the payment.
    price (float): The amount of the payment.
    product_name (str): The name of the product or service being paid for.

Returns:
    dict: A dictionary with the approval_url if the payment is successfully created, or an error.
"""

"""

Executes a PayPal payment.

Executes a payment with the given payment_id and payer_id and returns a success message if the payment was successful, or an error if something goes wrong.

Args:
    payment_id (str): The ID of the payment to be executed.
    payer_id (str): The ID of the payer who approved the payment.

Returns:
    str: A success message if the payment was successfully executed, or an error.

"""

import paypalrestsdk
import os


class Paypal:
    """
        A class to handle PayPal payment processing using the PayPal REST SDK.

        Attributes:
            None

        Methods:
            __init__(): Initializes the PayPal SDK with configuration details.
            create_payment(currency, price, product_name): Creates a PayPal payment.
            execute_payment(payment_id, payer_id): Executes a PayPal payment.
        """

    def __init__(self):
        """
               Initializes the PayPal SDK with configuration details.
               """

        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": "AVeNWfKsQumK7ComO_g60tC9LX_noDUI2hZ6BSToi_ZU6tcQVabHuGtxTJxSQq5C815pd622WoB7TI3D",
            "client_secret": "EEa3DYYaAoWpGxDjfGw-gOk5TzgrZI_qiWvZY1KzoU_4KKK_sc93M7qmxvlW-iUG4fgNgXRZ1oWvM-QA"
        })

    def create_payment(self, currency, price, product_name):
        """
        Creates a PayPal payment.

        Args:
            currency (str): The currency code (e.g., 'USD').
            price (float): The price of the product.
            product_name (str): The name of the product.

        Returns:
            dict: A dictionary containing the approval URL if the payment was created successfully,
                  or an error message if the payment creation failed.
        """

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": product_name,
                        "sku": "001",
                        "price": f"{price:.2f}",
                        "currency": currency,
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": f"{price:.2f}",
                    "currency": currency
                }
            }],
            "redirect_urls": {
                "return_url": os.getenv("PAYPAL_RETURN_URL", "http://51.20.249.18:8001/payment/execute"),
                "cancel_url": os.getenv("PAYPAL_CANCEL_URL", "http://51.20.249.18:3000/subscription")
            }
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return {"approval_url": str(link.href), "payment_id": payment.id}
        else:
            return {"error": payment.error}, 400

    def execute_payment(self, payment_id, payer_id):
        """
                Executes a PayPal payment.

                Args:
                    payment_id (str): The ID of the payment to be executed.
                    payer_id (str): The ID of the payer.

                Returns:
                    str or dict: A success message if the payment was executed successfully,
                                 or an error message if the payment execution failed.
                """

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            return "Payment executed successfully"
        else:
            return {"error": payment.error}, 400
