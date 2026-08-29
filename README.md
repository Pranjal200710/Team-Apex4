# MediCare Patient Portal — GitHub Codespaces

This version unifies the **Current Diagnosis / Medical History** page with the visual design used by the supplied **Payments** page.

## Required files

Keep these files together in the repository root:

- `server.js` — Node.js server and redesigned Current Diagnosis page
- `package.json` — start configuration
- `indexf.html` — existing Payments page
- `styles.css` — existing Payments styles
- `app.js` — existing Payments interactions

## Run in GitHub Codespaces

Open **Terminal → New Terminal** and run:

```bash
npm start
```

Then open the **Ports** tab and open port **3000**.

## Routes

- `/` — Current Diagnosis / Medical History
- `/current-diagnosis` — Current Diagnosis / Medical History
- `/payments` — Payments page using `indexf.html`, `styles.css`, and `app.js`
- `/health` — JSON server health check

## What was changed

The Medical History page now uses the same UI language as the Payments page:

- dark green fixed sidebar
- MediCare branding
- DM Sans body typography
- Playfair Display headings
- mint / yellow / lavender status cards
- matching table, filters, buttons, spacing and responsive behavior

The original Medical History demo functionality is preserved:

- protected diagnosis and prescription fields
- access request flow
- approve / deny demo controls
- automatic 5-minute expiry
- visit filtering and search
- expandable consultation details
- prescriptions
- investigations
- latest vitals
- access audit trail
- Care Assistant widget
