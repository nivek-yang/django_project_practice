from django.shortcuts import render, redirect
import braintree
from django.views.decorators.http import require_POST
from django.contrib import messages

import os 
from dotenv import load_dotenv
load_dotenv()

# Create your views here.

def index(req):
    return render(req, "pages/index.html")

def about(req):
    return render(req, "pages/about.html")

def contact(req):
    return render(req, "pages/contact.html")

def braintree_gateway():
    return braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=os.getenv("MERCHANT_ID"),
            public_key=os.getenv("PUBLIC_KEY"),
            private_key=os.getenv("PRIVATE_KEY"))
    )

@require_POST
def paid(req):
    result = braintree_gateway().transaction.sale({
        "amount": 10,
        "payment_method_nonce": req.POST.get("nonce")
    })

    if result.is_success:
        # TODO 把 user 的角色設定成 vip
        messages.success(req, "付款成功")
        
    else:
        messages.error(req, "付款失敗")
        
    return redirect("pages:index")


def payment(req):
    token = braintree_gateway().client_token.generate()
    return render(req, "pages/payment.html", {"token": token})


