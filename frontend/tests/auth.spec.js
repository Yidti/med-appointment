
import { test, expect } from '@playwright/test';

test('user can register and log in', async ({ page }) => {
  // Use a unique email for each test run
  const uniqueEmail = `testuser_${Date.now()}@example.com`;
  const password = 'password123';

  // Navigate to the app's root
  await page.goto('/');

  // --- Registration ---
  await page.locator('h2:has-text("Register")').waitFor();

  // Fill out the registration form
  await page.locator('#name').fill('Test User');
  await page.locator('#email').fill(uniqueEmail);
  await page.locator('#password').fill(password);
  await page.locator('#phone').fill('1234567890');
  await page.locator('#birthday').fill('1990-01-01');

  // It's best practice to wait for the event *before* triggering the action.
  const dialogPromise = page.waitForEvent('dialog');

  // Submit the registration form
  await page.locator('form:has-text("Register") button[type="submit"]').click();

  // Wait for the dialog to appear and validate it
  const dialog = await dialogPromise;
  expect(dialog.message()).toBe('Registration successful! Please log in.');
  await dialog.accept();

  // --- Login ---
  await page.locator('h2:has-text("Login")').waitFor();

  // Fill out the login form
  await page.locator('#login-email').fill(uniqueEmail);
  await page.locator('#login-password').fill(password);

  // Submit the login form
  await page.locator('form:has-text("Login") button[type="submit"]').click();

  // --- Verification ---
  // After login, the register/login forms should disappear
  await expect(page.locator('h2:has-text("Register")')).not.toBeVisible();
  await expect(page.locator('h2:has-text("Login")')).not.toBeVisible();

  // A logout button should be visible
  await expect(page.locator('button:has-text("Logout")')).toBeVisible();

  // The doctor list should be visible
  await expect(page.locator('h2:has-text("Doctors")')).toBeVisible();
});
