import { test, expect } from '@playwright/test';

test.describe('Booking Flow', () => {
  // Authentication is handled by the global setup.

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
