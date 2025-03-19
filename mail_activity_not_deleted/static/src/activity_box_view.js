/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';

registerPatch({
    name: 'ActivityBoxView',
    fields: {
        activityViews: {
            /**
            * @override
            */
            compute() {
                return this.chatter.thread.activities
                    .filter(activity => activity.state !== 'done')
                    .map(activity => ({ activity }));
            },
        },
    },
});