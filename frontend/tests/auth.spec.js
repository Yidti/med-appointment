
import { test, expect } from '@playwright/test';

test('user can register successfully', async ({ page }) => {
  // Use a unique email for each test run to ensure independence
  const uniqueEmail = `testuser_${Date.now()}@example.com`;
  const password = 'aVeryStrongP@ssw0rd!';

  // 1. Navigate to the registration page
  await page.goto('/register');

  // 2. Wait for the form to be visible and fill it out
  await expect(page.locator('h3:has-text("Create Account")')).toBeVisible();

  await page.locator('#name').fill('Test User');
  await page.locator('#email').fill(uniqueEmail);
  await page.locator('#password').fill(password);
  await page.locator('#phone').fill('1234567890');
  await page.locator('#birthday').fill('1990-01-01');

  // 3. Click the submit button
  await page.click('button[type="submit"]');

  // 4. Assert that the page redirects to the login page
  await page.waitForURL('**/login');
  await expect(page).toHaveURL(/.*login/);
});

