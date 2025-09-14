import { chromium, expect } from '@playwright/test';

const storageStatePath = 'storageState.json';

async function globalSetup(config) {
  const { baseURL } = config.projects[0].use;
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const uniqueEmail = `testuser_global_${Date.now()}@example.com`;
  const password = 'password123';

  // 1. Register a new user via UI (this part works)
  await page.goto(`${baseURL}/register`);
  await page.fill('#first_name', 'Global Setup User');
  await page.fill('#email', uniqueEmail);
  await page.fill('#password', password);
  await page.fill('#phone', '1112223333');
  await page.fill('#birthday', '1991-01-01');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/login');

  // 2. Log in via API call (more robust)
  const requestContext = page.context();
  const response = await requestContext.request.post(`http://localhost:8000/api/login/`, {
    data: {
      email: uniqueEmail,
      password: password,
    },
  });
  if (!response.ok()) {
    console.log(`Login API failed with status ${response.status()}:`, await response.text());
  }
  const { token } = await response.json();

  // 3. Set the token in localStorage
  await page.evaluate(t => {
    localStorage.setItem('token', t);
  }, token);

  // 4. Go to a protected page and verify login
  await page.goto(`${baseURL}/doctors`);
  await expect(page.locator('h2:has-text("Find Your Doctor")')).toBeVisible();

  // 5. Save the authenticated state
  await page.context().storageState({ path: storageStatePath });
  await browser.close();
}

export default globalSetup;
