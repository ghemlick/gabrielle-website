# Gabrielle Hemlick — Personal Website

A minimal static personal site with About, Work, Blog, and Contact pages.

## Preview locally

Open `index.html` in your browser, or run a simple server:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000

## Customize

- **Home hero & copy:** `index.html`
- **About page:** `about.html`
- **Projects:** `work.html` — swap the placeholder cards with your real work
- **Contact links:** `contact.html` — update email, LinkedIn, GitHub URLs
- **Blog posts:** duplicate any file in `blog/` and add a card to `blog/index.html`
- **Email signup:** see [Newsletter setup](#newsletter-setup) below
- **Colors & fonts:** `css/styles.css` (see `:root` variables at the top)

## Newsletter setup

The site uses [Buttondown](https://buttondown.com) for email subscriptions — free for up to 100 subscribers.

1. Create a free account at [buttondown.com](https://buttondown.com)
2. Open `js/config.js` and set your `buttondownUsername`
3. Update `siteUrl` in `js/config.js` and the URLs in `feed.xml` to match your live domain

Subscribers see a signup form on the home page, blog index, and individual posts. They'll get a confirmation email before they're fully subscribed (double opt-in).

### Free way to email subscribers when you publish

Buttondown's built-in RSS automation costs $9/month, but you can automate this for free with GitHub Actions and Buttondown's API (API access is free on all plans).

When you push an update to `feed.xml`, the workflow in `.github/workflows/notify-subscribers.yml` creates a **draft email** in Buttondown for each new post. You review it in Buttondown and click send — one extra click, no monthly fee.

**Setup:**

1. In Buttondown, go to **Settings → API** and create an API key
2. Push this repo to GitHub
3. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
4. Add a secret named `BUTTONDOWN_API_KEY` with your API key
5. When you publish a new post, add an `<item>` to `feed.xml` and push to `main`

**Optional:** To send immediately without reviewing, change `EMAIL_STATUS` in the workflow from `draft` to `about_to_send`.

**Even simpler (100% manual, also free):** Skip automation entirely. When you publish a post, open Buttondown, write a short email with a link to the post, and send it yourself.

### Adding a new blog post

1. Add the HTML file in `blog/`
2. Add a card to `blog/index.html`
3. Add an `<item>` to `feed.xml`
4. Push to GitHub (if using the free automation above)


## Deploy

This site has no build step. Upload the folder to any static host:

- [GitHub Pages](https://pages.github.com/)
- [Netlify](https://www.netlify.com/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
