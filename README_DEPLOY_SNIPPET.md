## Production deploy (recommended)

1. Create server (VPS) with Docker & Docker Compose installed.
2. Place repo at `/home/<user>/socialpipe` and copy `docker-compose.prod.yml` & `deploy/nginx/nginx.conf`.
3. Provide `/home/<user>/socialpipe/.env` with production secrets.
4. Option A (recommended): Use GitHub Actions + SSH deploy:
   - Add secrets: DEPLOY_SSH_HOST, DEPLOY_SSH_USER, DEPLOY_SSH_PORT, DEPLOY_SSH_KEY
   - Push to `main` and workflow will run.
5. Start stack:
   ```bash
   sudo systemctl enable --now socialpipe.service
