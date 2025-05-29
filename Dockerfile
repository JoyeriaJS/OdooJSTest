FROM odoo:17.0

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    netcat-openbsd \
    && pip3 install --no-cache-dir pandas openpyxl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chmod=755 entrypoint.sh ./
COPY ./custom_addons /mnt/custom_addons

USER odoo

ENTRYPOINT ["/bin/sh"]
CMD ["entrypoint.sh"]
