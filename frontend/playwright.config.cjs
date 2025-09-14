// @ts-check
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['list'], ['html', { open: 'never' }]],

  // Use a global setup file for authentication
  globalSetup: require.resolve('./tests/global.setup.js'),

  use: {
    baseURL: 'http://localhost:5173', // The frontend server
    trace: 'on-first-retry',
    // Tell all tests to use the saved storage state
    storageState: 'storageState.json',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Run your local dev server before starting the tests
  webServer: [
    {
      // Backend server
      command: 'npm run test:backend',
      cwd: '..', // Run from the project root
      url: 'http://localhost:8000/api/doctors/',
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
    },
    {
      // Frontend server (serving the built files)
      command: 'npx serve -s dist -l 5173',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
    },
  ],
});
