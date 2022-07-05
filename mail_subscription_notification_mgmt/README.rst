Mail Subscription Notification Management
=========================================

.. contents:: Table of Contents

Overview
--------

The module allows to manage enabling or disabling subscription notification for a model.

Settings
--------
As a user belonging to the `Administration / Configuration group`,
activate the developer mode and go to the form view of a model `(Settings > Technical > database Structure > models)`.

A new `Disable Subscription Notifications` checkbox is present.

The default value of the box is unchecked.

Usage
-----
As a sales user, create a lead or opportunity or go to an existing lead/opportunity.

Fill a user (other than myself) in the Salesperson field and save.

    .. image:: static/description/assign_salesperson_to_lead.png

By default the Salesperson will receive an email notification.

    .. image:: static/description/subscription_notification.png

Now if you want to disable the subscription notification for the crm.lead model, go to the form view of this model, uncheck the box **Disable Subscription Notifications** and save.

    .. image:: static/description/disable_subscription_notification.png


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
