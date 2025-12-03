import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import FileResponse, Http404, HttpResponseRedirect
import stripe
from .productoins import PACKAGES

stripe.api_key = settings.STRIPE_SECRET_KEY

# Track which Stripe sessions already got emails
SENT_MAILS = set()


# Homepage
def index(request):
    return render(request, "index.html", {"packages": PACKAGES})


# Create Checkout Session
def create_checkout_session(request):
    if request.method != "POST":
        return redirect("index")

    pack_id = str(request.POST.get("packId"))
    package = PACKAGES.get(pack_id)
    if not package:
        return redirect("index")

    domain_url = request.build_absolute_uri('/')[:-1]  # remove trailing slash

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "cad",
                "unit_amount": int(package["price_cents"]),
                "product_data": {"name": package["name"]},
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=domain_url + f"/success/{pack_id}/{{CHECKOUT_SESSION_ID}}/",
        cancel_url=domain_url + "/",
    )

    return HttpResponseRedirect(checkout_session.url)


# Success page after payment
def success(request, pack_id, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return redirect("index")

    if session.payment_status != "paid" or pack_id not in PACKAGES:
        return redirect("index")

    package = PACKAGES[pack_id]
    customer_email = session.customer_details.email

    # Send email only once per session
    if session_id not in SENT_MAILS:
        send_mail(
            subject="Your Purchase from Funny Store",
            message=(
                f"Thank you for purchasing {package['name']} for ${package['price_cents']/100:.2f}!\n\n"
                f"Download your package here: "
                f"{request.build_absolute_uri(f'/download/{pack_id}/{session_id}/')}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            fail_silently=False,
        )
        SENT_MAILS.add(session_id)

    return render(request, "success.html", {
        "package_name": package["name"],
        "price": package["price_cents"] / 100,
        "download_url": f"/download/{pack_id}/{session_id}/",
        "customer_email": customer_email,
    })


# Serve the file (no email here, just the file)
def download_package(request, pack_id, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return redirect("index")

    if session.payment_status != "paid" or pack_id not in PACKAGES:
        return redirect("index")

    package = PACKAGES[pack_id]

    filepath = os.path.join(
        settings.BASE_DIR, 'static', 'packages', os.path.basename(package['file_url'])
    )
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), as_attachment=True,
                            filename=os.path.basename(filepath))
    else:
        raise Http404("File not found")
