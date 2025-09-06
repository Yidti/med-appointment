import { test, expect } from '@playwright/test';

test.describe('Booking Flow', () => {
  const storageStatePath = 'storageState.json';

  // Before all tests, run a setup to authenticate and save the storage state.
  test.beforeAll(async ({ browser }) => {
    // Use a new, clean context for the setup, ignoring the storageState of the suite.
    const setupContext = await browser.newContext({ storageState: undefined });
    const page = await setupContext.newPage();

    const uniqueEmail = `testuser_booking_${Date.now()}@example.com`;
    const password = 'password123';

    // Register a new user
    await page.goto('/register');
    await page.fill('#name', 'Booking User');
    await page.fill('#email', uniqueEmail);
    await page.fill('#password', password);
    await page.fill('#phone', '1112223333');
    await page.fill('#birthday', '1991-01-01');
    await page.click('button[type="submit"]');
    // After registration, wait for the navigation to the login page to complete.
    // The component has a 2-second delay, so we wait for a login-specific element.
    await expect(page.locator('#login-email')).toBeVisible({ timeout: 5000 });

    // Log in
    await page.fill('#login-email', uniqueEmail);
    await page.fill('#login-password', password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*doctors/);

    // Save the authenticated state and close the setup context.
    await page.context().storageState({ path: storageStatePath });
    await setupContext.close();
  });

  // Use the saved authenticated state for all tests in this suite.
  test.use({ storageState: storageStatePath });

  test('user can view doctors, select one, and book an appointment', async ({ page }) => {
    // 1. Go to the doctors list page (already on it after login, but good to be explicit)
    await page.goto('/doctors');

    // 2. Verify the doctor list is visible.
    await expect(page.locator('h2:has-text("Find Your Doctor")')).toBeVisible();
    await expect(page.locator('.card').first()).toBeVisible({ timeout: 10000 });

    // 3. Click "View Schedule" for the E2E test doctor.
    await page.locator('.card', { hasText: 'E2E Test Doctor' }).getByText('View Schedule').click();

    // 4. Verify navigation to the doctor's detail page.
    await expect(page).toHaveURL(/.*doctors\/\d+/);
    await expect(page.locator('h4:has-text("Book an Appointment")')).toBeVisible();

    // 5. Select the first available time slot and book.
    const firstSlot = page.locator('.list-group .list-group-item-action').first();
    await expect(firstSlot).toBeVisible({ timeout: 10000 });
    await firstSlot.click();
    await expect(firstSlot).toHaveClass(/active/);

    // Add an aggressive listener to fail the test with a clear API error
    page.on('response', async response => {
      if (response.url().includes('/api/appointments/') && response.request().method() === 'POST') {
        expect(response.status(), `API call to ${response.url()} failed with status ${response.status()}`).toBe(201);
      }
    });

    const bookingButton = page.locator('button:has-text("Book Appointment")');
    // Click the booking button
    await bookingButton.click();

    // Verify the redirection to the confirmation page
    await expect(page).toHaveURL(/.*booking\/confirmation/);
    await expect(page.locator('h2:has-text("預約成功")')).toBeVisible();

    // Verify the content of the confirmation page
    await expect(page.locator('.appointment-details')).toBeVisible();
    await expect(page.locator('.appointment-details')).toContainText('醫師:');
  });
});
