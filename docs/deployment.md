# Deploy the agreed MVP

Deployment has not yet been executed. Confirm the project, billing/access and region first. An existing configured project is not, by itself, a confirmed project choice.

## API

From the repository root with the standard Dockerfile:

```sh
gcloud run deploy swan-mvp-api --source . --project PROJECT_ID --region REGION
```

Confirm the service URL, intended audience/access settings and `/health` plus `/ready`. Do not mark ready if product artifacts failed to load. Verify access-log and retention configuration; do not enable request-body logging.

## Interface

Build the UI image from `Dockerfile.ui` using your agreed registry/build process, then deploy it with `SWAN_API_URL` set to the confirmed API URL. The interface does not need local product data. The backend must be reachable from the UI server; a private API needs explicit service authentication rather than a public URL alone.

## Release check

- API readiness returns 50 products and the expected content version.
- The public/interface URL opens independently and does not depend on a developer laptop.
- Eligible numeric-level profile returns real product IDs and reasons.
- `aroma` product cannot pass fragrance avoidance.
- Levels 4/5, referral flags and unsupported concerns return no products.
- Invalid answers, empty/insufficient results and API failure produce clear messages.
- No fictional fallback products, request-body logs or stored questionnaire database.
- Record API URL, interface URL, Git commit, artifact manifest/version and test results in the tracker.
