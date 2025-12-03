document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("theme-toggle");
  const body = document.body;

  const currentTheme = localStorage.getItem("theme") || "light";
  body.classList.add(`${currentTheme}-mode`);
  toggle.textContent = currentTheme === "dark" ? "☀️ حالت روز" : "🌙 حالت شب";

  toggle.addEventListener("click", () => {
    const newTheme = body.classList.contains("light-mode") ? "dark" : "light";
    body.classList.remove("light-mode", "dark-mode");
    body.classList.add(`${newTheme}-mode`);
    localStorage.setItem("theme", newTheme);
    toggle.textContent = newTheme === "dark" ? "☀️ حالت روز" : "🌙 حالت شب";
  });
});
