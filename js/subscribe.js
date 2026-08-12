(function () {
  const config = window.SITE_CONFIG?.newsletter;
  const username = config?.buttondownUsername?.trim();

  function createSubscribeSection() {
    const section = document.createElement("section");
    section.className = "subscribe section";
    section.setAttribute("aria-labelledby", "subscribe-heading");

    section.innerHTML = `
      <div class="subscribe-inner">
        <h2 id="subscribe-heading">Get new posts by email</h2>
        <p class="subscribe-lead">
          Occasional notes when I publish — no spam, unsubscribe anytime.
        </p>
        <form class="subscribe-form" novalidate>
          <label class="visually-hidden" for="subscribe-email">Email address</label>
          <input
            type="email"
            id="subscribe-email"
            name="email"
            autocomplete="email"
            placeholder="you@example.com"
            required
          />
          <button type="submit" class="button">Subscribe</button>
          <input type="text" name="bot-field" class="subscribe-honeypot" tabindex="-1" autocomplete="off" />
        </form>
        <p class="subscribe-message" role="status" aria-live="polite" hidden></p>
      </div>
    `;

    return section;
  }

  function showMessage(form, text, type) {
    const message = form.parentElement.querySelector(".subscribe-message");
    if (!message) return;

    message.textContent = text;
    message.hidden = false;
    message.className = `subscribe-message subscribe-message--${type}`;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const honeypot = form.elements.namedItem("bot-field");
    if (honeypot && honeypot.value) return;

    if (!username) {
      showMessage(
        form,
        "Email signup is not configured yet. Check back soon.",
        "error"
      );
      return;
    }

    const emailInput = form.elements.namedItem("email");
    const button = form.querySelector('button[type="submit"]');
    const email = emailInput.value.trim();

    if (!email) {
      showMessage(form, "Please enter your email address.", "error");
      return;
    }

    button.disabled = true;
    showMessage(form, "Subscribing…", "pending");

    const endpoint = `https://buttondown.email/api/emails/embed-subscribe/${encodeURIComponent(username)}`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        form.reset();
        showMessage(
          form,
          "Almost done — check your inbox for a confirmation email.",
          "success"
        );
        return;
      }

      const data = await response.json().catch(() => ({}));
      showMessage(
        form,
        data.detail || data.email?.[0] || "Something went wrong. Please try again.",
        "error"
      );
    } catch (error) {
      form.action = endpoint;
      form.method = "post";
      form.submit();
    } finally {
      button.disabled = false;
    }
  }

  document.querySelectorAll("[data-subscribe-mount]").forEach((mount) => {
    const section = createSubscribeSection();
    mount.replaceWith(section);

    const form = section.querySelector(".subscribe-form");
    form.addEventListener("submit", handleSubmit);
  });
})();
