mod_wsgi-express setup-server /var/www/wmiys/api/api_wmiys.wsgi \
--user www-data  \
--group www-data  \
--server-name api.wmiys.com  \
--port 80   \
--access-log  \
--log-level info   \
--compress-responses \
--processes 3 \
--startup-timeout 30   \
--server-root /etc/api.wmiys.com \
--host 104.225.208.116 \
--document-root /var/www/wmiys/api/api_wmiys/static \
--https-port 443 \
--https-only \
--ssl-certificate-file /etc/letsencrypt/live/api.wmiys.com/fullchain.pem \
--ssl-certificate-key-file /etc/letsencrypt/live/api.wmiys.com/privkey.pem \
--setup-only

