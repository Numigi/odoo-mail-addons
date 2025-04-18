FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"

USER odoo

COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted
COPY mail_autosubscribe /mnt/extra-addons/mail_autosubscribe

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
