==================
Mail Autosubscribe
==================

This module allows you to configure partners that will be automatically in copy
of their company's business documents.

For example, you can configure an accountant to be in copy of all invoices
sent for a given commercial partner, regardless of the invoicing address.

Configuration
=============

Go to `Configuration > Technical > Automation > Autosubscribe Models` and configure
the models for which you want the feature to work.

Then, on each partner, you can check the company documents subscriptions in the
field `In copy of`.

This feature can be disabled on specific templates, if required, by disabling the
Autosubscribe followers field.

Example of use
==============
Let's say you have a sale order for a customer, and you want to make sure that
the contact person of the customer is in copy of the order when the sale order
is confirmed.

To do this, you need to:
- Go to `Configuration > Technical > Automation > Autosubscribe Models` and
  configure the `sale.order` model.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/12.0/mail_autosubscribe/static/description/model_option_list.png

- Go to the partner form view and check the `In copy of` field for the contact
  person of the customer.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/12.0/mail_autosubscribe/static/description/partner_configuration.png

- When you confirm the sale order, the contact person of the customer will be
  subscribed to the sale order.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/12.0/mail_autosubscribe/static/description/sale_order_to_confirm.png

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/12.0/mail_autosubscribe/static/description/sale_order_confirmed.png

- When sending document in email composer, the contact person of the customer
  will be in copy of the email.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/12.0/mail_autosubscribe/static/description/sale_document_default_recipient.png

Credits
=======

Authors
~~~~~~~

* Camptocamp

Contributors
~~~~~~~~~~~~
* `Camptocamp <https://www.camptocamp.com>`_

     * Iván Todorovich <ivan.todorovich@gmail.com>

* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

* Odoo Community Association <https://odoo-community.org>

Maintainers
~~~~~~~~~~~

This module is maintained by Numigi.

More information
----------------
* Meet us at https://bit.ly/numigi-com