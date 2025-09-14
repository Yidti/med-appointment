#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Seeding test data ---"
./venv/bin/python manage.py seed_test_doctor

echo "--- Starting backend server in background ---"
(./venv/bin/python manage.py migrate --no-input && ./venv/bin/python manage.py runserver) &
BACKEND_PID=$!
echo "Backend PIDs: $BACKEND_PID"

echo "--- Starting frontend server in background ---"
(cd frontend && npm run dev) &
FRONTEND_PID=$!
echo "Frontend PIDs: $FRONTEND_PID"

echo "--- Waiting for services to be ready ---"
npx wait-on http://localhost:5173 http://localhost:8000/api/doctors/

echo "--- Running Playwright E2E tests ---"
cd frontend && npx playwright test

echo "--- Cleaning up test data ---"
cd .. # Go back to root if playwright test changed directory
./venv/bin/python manage.py cleanup_test_data

echo "--- Stopping background servers ---"
kill $BACKEND_PID $FRONTEND_PID || true # Use || true to prevent script from exiting if a PID is already dead

echo "--- E2E tests completed successfully ---"
