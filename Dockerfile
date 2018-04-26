FROM quay.io/numigi/odoo-public:11.0
MAINTAINER numigi <contact@numigi.com>

COPY mail_recipient_unchecked /mnt/extra-addons/mail_recipient_unchecked

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
