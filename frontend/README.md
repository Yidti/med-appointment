# frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Running Tests

#### Unit Tests

To run unit tests with Vitest:

```sh
npm test
```

This will execute all `*.spec.js` files once and provide a report.

#### End-to-End (E2E) Tests

E2E tests are run using Playwright. We have two methods for running them:

**1. Quick Method (For Local Development)**

This command uses `npm-run-all` to start the backend and frontend servers concurrently and then runs the tests. It's convenient but can sometimes be less stable.

```sh
npm run test:e2e
```

**2. Robust Method (For CI/CD or Stable Testing)**

This is a more reliable, step-by-step process that ensures servers are fully ready before tests run. This is the recommended approach for automated environments.

```bash
# 1. Start the backend server in the background
(cd .. && . venv/bin/activate && python manage.py migrate && python manage.py runserver) &
BACKEND_PID=$!

# 2. Start the frontend server in the background
npm run dev &
FRONTEND_PID=$!

# 3. Wait for both servers to be ready
npx wait-on http://localhost:8000 http://localhost:5173

# 4. Run Playwright tests
npx playwright test

# 5. Clean up: stop the servers
kill $BACKEND_PID
kill $FRONTEND_PID
```
