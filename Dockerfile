FROM odoo:17.0

USER root

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./custom_addons /mnt/custom_addons

USER odoo

ENTRYPOINT ["/entrypoint.sh"]