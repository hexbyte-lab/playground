// cookie.js
window.onload = function() {
  if (document.cookie.includes("cookie_consent=accepted")) {
    document.getElementById('cookie-consent').style.display = 'none';
  }
}

// function acceptCookies() {
//   document.getElementById('cookie-consent').style.display = 'none';
//   document.cookie = "cookie_consent=accepted; path=/; max-age=31536000"; // 1 year
// }

// function denyCookies() {
//   document.getElementById('cookie-consent').style.display = 'none';
// }
