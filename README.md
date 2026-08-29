# Medical History Demo — GitHub Codespaces

This repository runs the supplied `diagnosis_3.html` as a Node.js application without external npm dependencies.

## Run in GitHub Codespaces

1. Upload `server.js`, `package.json`, and `.gitignore` to your GitHub repository.
2. Open the repository in **GitHub Codespaces**.
3. In the terminal, run:

   ```bash
   npm start
   ```

4. Codespaces will detect port **3000**. Open the forwarded port from the **Ports** tab.

## Local run

```bash
npm start
```

Then open `http://localhost:3000`.

## Health check

`GET /health` returns a small JSON response so you can verify that the Node.js server is running.

## Notes

- The original HTML, CSS, and browser-side JavaScript are embedded in `server.js` as Base64 and decoded at runtime.
- No Express or third-party dependency is required.
- `PORT` is read from the environment, which makes the app compatible with GitHub Codespaces and most hosting platforms.
