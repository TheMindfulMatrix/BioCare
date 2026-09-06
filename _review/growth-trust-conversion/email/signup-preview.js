/* Review-only UI simulation. No network, storage, analytics, or real addresses. */
(() => {
  "use strict";
  const form = document.querySelector("[data-signup-preview]");
  const email = document.querySelector("#signup-email");
  const consent = document.querySelector("#signup-consent");
  const error = document.querySelector("#signup-error");
  const status = document.querySelector("#signup-status");
  const outcome = document.querySelector("#preview-state");
  const submit = form.querySelector("button");
  let busy = false;
  outcome.addEventListener("change", () => {
    const unavailable = outcome.value === "unavailable";
    email.disabled = consent.disabled = submit.disabled = unavailable;
    form.reset();
    error.textContent = "";
    email.removeAttribute("aria-invalid");
    consent.removeAttribute("aria-invalid");
    status.textContent = unavailable ? "Signup is not available on the public website." : "Simulation ready. Use reader@example.invalid. Nothing is transmitted.";
  });
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (busy || outcome.value === "unavailable") return;
    error.textContent = "";
    email.removeAttribute("aria-invalid");
    consent.removeAttribute("aria-invalid");
    if (!email.validity.valid || email.value.trim() !== "reader@example.invalid") {
      error.textContent = "Enter reader@example.invalid to test this private prototype. Do not enter a real email address.";
      email.setAttribute("aria-invalid", "true"); email.focus(); return;
    }
    if (!consent.checked) {
      error.textContent = "Choose the consent checkbox only if you want to test an opted-in submission.";
      consent.setAttribute("aria-invalid", "true"); consent.focus(); return;
    }
    busy = true; submit.disabled = true; outcome.disabled = true; status.textContent = "Simulating a request…";
    await new Promise(resolve => setTimeout(resolve, 150));
    if (outcome.value === "confirmation") {
      status.textContent = "Simulation only: check your inbox to confirm. No email was sent and no subscription was created.";
      form.reset();
    } else {
      error.textContent = "Simulated provider error. Your subscription has not been confirmed. Try again later.";
      status.textContent = "Nothing was sent or saved.";
    }
    busy = false; outcome.disabled = false; submit.disabled = outcome.value === "unavailable";
  });
})();
