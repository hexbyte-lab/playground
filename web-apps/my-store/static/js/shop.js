// shop.js

// document.querySelectorAll(".btn-buy").forEach(button => {
//   button.addEventListener("click", () => {
//     const pack = JSON.parse(button.dataset.pack);

//     // Fill modal fields
//     document.getElementById("packId").value = pack.id;
//     document.getElementById("packTitleDisplay").textContent = pack.title;
//     document.getElementById("packTitle").value = pack.title;
//     document.getElementById("packPriceDisplay").textContent = `$${pack.price.toFixed(2)}`;
//     document.getElementById("packPrice").value = pack.price;

//     // Show modal
//     new bootstrap.Modal(document.getElementById("checkoutModal")).show();
//   });
// });

// Enable/disable gift message
const isGiftCheckbox = document.getElementById("isGift");
const giftMessageTextarea = document.getElementById("giftMessage");
isGiftCheckbox.addEventListener("change", () => {
  giftMessageTextarea.disabled = !isGiftCheckbox.checked;
});

// Checkout form submission
document.getElementById("toPayment").addEventListener("click", async () => {
  const packId = document.getElementById("packId").value;
  const recipientEmail = document.getElementById("recipientEmail").value;
  const senderName = document.getElementById("senderName").value;
  const isGift = document.getElementById("isGift").checked;
  const giftMessage = document.getElementById("giftMessage").value;

  if (!recipientEmail) {
    alert("Please enter a valid email.");
    return;
  }

  const response = await fetch("/create-checkout-session/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({packId, recipientEmail, senderName, isGift, giftMessage})
  });

  const data = await response.json();
  window.location.href = data.url;  // Redirect to Stripe Checkout
});
