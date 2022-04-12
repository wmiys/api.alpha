mod_wsgi-express start-server \
--user www-data  \
--group www-data  \
--server-name api.wmiys.com  \
--port 81   \
--access-log  \
--log-level info   \
--server-root /etc/api.wmiys.com \
--host 104.225.208.163 \
--log-to-terminal \
--document-root /var/www/wmiys/api.wmiys/src/api_wmiys/static \
/var/www/wmiys/api.wmiys/src/api_wmiys.wsgi
