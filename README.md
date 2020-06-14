Install gcloud and init

Install miniconda on /opt/miniconda

`conda create --name work python=3.7`

`conda activate work`

`pip install -r requirements.txt`

Install NodeJS and Hubot following the official docs

`yo hubot --adapter=slack`

Copy systemd service files into /etc/systemd/system/

Create file /etc/iambot/env with content (no quotes involved):
```
HUBOT_SLACK_TOKEN=...
WEBHOOK_URL=...
```

Create 2 cron jobs via `crontab -e`
```
*/2 * * * * sudo su brian /opt/iambot/run_check_iams.sh
*/5 * * * * sudo su brian /opt/iambot/prepare_previous.sh
```

and it could run, I think. CMIIW.
# gcp-iam-check-hubot
# gcp-iam-check-hubot
