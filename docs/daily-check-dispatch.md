# Daily check morning dispatch

The [Daily check](../.github/workflows/daily-check.yml) workflow runs only on `workflow_dispatch`. An external cron must start it each morning so GitHub’s own `schedule` timer is never involved.

## Remove cron.surf

1. Open [Installed GitHub Apps](https://github.com/settings/installations).
2. Open **cron.surf** → **Configure** (or **Uninstall**).
3. Uninstall it from this account, or remove **TorontoZooGuide** from its repository access.

cron.surf is not used anymore; leaving it installed only creates empty queued checks on push.

## Token

Create a fine-grained personal access token with access to **WesleyRenaud/TorontoZooGuide** only, and **Actions: Read and write**. Store the token in the cron service, not in this repository.

## cron-job.org

1. Create a job at [cron-job.org](https://cron.job.org/).
2. Schedule: `0 6 * * *`, timezone **America/Toronto**.
3. Request:
   - Method: `POST`
   - URL: `https://api.github.com/repos/WesleyRenaud/TorontoZooGuide/actions/workflows/daily-check.yml/dispatches`
   - Headers:
     - `Authorization: Bearer <token>`
     - `Accept: application/vnd.github+json`
     - `X-GitHub-Api-Version: 2022-11-28`
     - `Content-Type: application/json`
   - Body: `{"ref":"main"}`
4. Turn on failure notifications for the job.
5. Use “Test run” once. GitHub should respond **204**, and Actions should show a new Daily check run with event `workflow_dispatch`.

## Manual test

```bash
gh workflow run daily-check.yml --ref main
```

Or with curl (token in `GITHUB_TOKEN`):

```bash
curl -sS -o /dev/null -w "%{http_code}\n" -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{"ref":"main"}' \
  https://api.github.com/repos/WesleyRenaud/TorontoZooGuide/actions/workflows/daily-check.yml/dispatches
```
