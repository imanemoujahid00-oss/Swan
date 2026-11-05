# Deploy the agreed MVP

Deployed on 5 November 2026 in Paris. [Demo interface](https://swan-mvp-ui-1083386136867.europe-west9.run.app). See the [external MVP overview](mvp-overview.md). Operational release details are maintained separately in restricted team documents; independent team acceptance remains open.

## Release configuration prepared on 5 November

Region: `europe-west9` (Paris). Use the project's approved deployment settings. The current MVP services use request-based billing, minimum zero and maximum one instance per service. This reduces idle cost; it is not a spending cap. An active Streamlit WebSocket session can keep a UI instance active; close unused demo tabs.

Build both images with `cloudbuild.yaml`, supplying `_REGISTRY` (the Artifact Registry repository path) and `_TAG` (the exact Git commit). `.gcloudignore` excludes local data, credentials and development files from the uploaded source. The API image downloads only checksum-verified runtime artifacts.

Use separate UI and API service identities. Only the UI identity gets `roles/run.invoker` on the API. Set `SWAN_API_URL` to the API's Cloud Run URL and `SWAN_API_AUTH=cloudrun` in the UI. The server obtains a short-lived ID token from Cloud Run metadata and sends it to the private API; no service-account key file is needed. Local development remains unauthenticated loopback unless that flag is explicitly enabled.

The public link is the UI only. Test the API using an authorized identity and verify anonymous API requests are rejected. Public UI access exposes the demonstration to anyone with its URL; no questionnaire database is implemented. Do not log request bodies, credentials or profile answers.

References: [service-to-service authentication](https://docs.cloud.google.com/run/docs/authenticating/service-to-service), [Cloud Run pricing](https://cloud.google.com/run/pricing).

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
