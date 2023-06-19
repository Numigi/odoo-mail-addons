FROM quay.io/numigi/odoo-public:14.latest
MAINTAINER numigi <contact@numigi.com>

USER root

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"

USER odoo

COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted
COPY fetchmail_outlook_by_company /mnt/extra-addons/fetchmail_outlook_by_company

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
