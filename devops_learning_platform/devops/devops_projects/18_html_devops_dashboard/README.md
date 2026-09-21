# HTML DevOps Dashboard

A hands-on frontend project for building an operational dashboard with semantic HTML, responsive CSS, and vanilla JavaScript.

## Open locally

Open `index.html` directly in a browser. No server or package installation is required.

## Features

- KPI cards for availability, latency, deployments, and open incidents
- Service health table with status filters
- Deployment timeline
- Incident list with severity filters
- Theme toggle
- Refresh timestamp
- Responsive layout for desktop and mobile

## Learning path

1. Read the HTML structure and landmark elements.
2. Inspect CSS variables, Grid, Flexbox, focus states, and responsive rules.
3. Trace the JavaScript data model and render functions.
4. Add a new service to `services` in `app.js`.
5. Add a filter or dashboard card.
6. Replace mock data with an authenticated API only after defining access, error, and loading states.

## Production extensions

- fetch metrics from a protected backend API
- add authentication and authorization
- use real Prometheus or cloud metric adapters
- add loading, empty, stale-data, and error states
- avoid exposing infrastructure secrets in browser JavaScript
- test keyboard navigation and responsive views
