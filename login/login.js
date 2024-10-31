document.querySelector(".show-hide").addEventListener("click", function () {
    const passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
      passwordField.type = "text";
      this.textContent = "Hide";
    } else {
      passwordField.type = "password";
      this.textContent = "Show";
    }
  });
  