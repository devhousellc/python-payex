class PurchaseOperation:
    AUTHORIZATION = 'AUTHORIZATION'
    SALE = 'SALE'


class DefaultPaymentMethod:
    DIRECTDEBIT = 'DIRECTDEBIT'
    IDEAL = 'IDEAL'
    CPA = 'CPA'
    CREDITCARD = 'CREDITCARD'
    PX = 'PX'
    MICROACCOUNT = 'MICROACCOUNT'
    PAYPAL = 'PAYPAL'
    INVOICE = 'INVOICE'
    EVC = 'EVC'
    LOAN = 'LOAN'
    GC = 'GC'
    CA = 'GA'
    FINANCING = 'FINANCING'
    CREDITACCOUNT = 'CREDITACCOUNT'
    PREMIUMSMS = 'PREMIUMSMS'
    SWISH = 'SWISH'


class OrderStatus:
    # 0 = The order is completed (a purchase has been done, but check the transactionStatus to see the result).
    Completed = 0
    # 1 = The order is processing. The customer has not started the purchase. PxOrder.Complete can return
    # orderStatus 1 for 2 weeks after PxOrder.Initialize is called. Afterwards the orderStatus will be set to 2
    Processing = 1
    # 2 = No order or transaction is found.
    NotFound = 2


class TransactionStatus:
    Sale = 0
    Initialize = 1
    Credit = 2
    Authorize = 3
    Cancel = 4
    Failure = 5
    Capture = 6