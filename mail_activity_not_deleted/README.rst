Mail Activity Not Deleted
=========================
Since version 11.0, Odoo adds the concept of activities.
One issue with this feature is that when an activity is completed, the activity record is deleted from the database.

This module deactivates terminated activities instead of deleting them from the mail_activity table.

To see deactivated activities : 

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/16.0/mail_activity_not_deleted/static/description/view_activities.png

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/16.0/mail_activity_not_deleted/static/description/filter_active_is_no.png

.. image:: https://raw.githubusercontent.com/Numigi/odoo-mail-addons/16.0/mail_activity_not_deleted/static/description/deactivated_activities.png    
    
New State
---------
The state Done is added to activities. Any completed activity is automatically set to Done.

New Field
---------
The field Date Done is added to activities. When completing the activity, this field is filled with the current time.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
