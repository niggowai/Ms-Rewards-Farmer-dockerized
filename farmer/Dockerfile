FROM python:3-alpine

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../ms_rewards_farmer.py .

RUN echo '18       7        *       *       *       /ms_rewards_farmer.py' >> /etc/crontabs/root

ENTRYPOINT [ "sleep", "infinity"]