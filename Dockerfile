FROM quay.io/numigi/odoo-public:12.0
MAINTAINER numigi <contact@numigi.com>

COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
