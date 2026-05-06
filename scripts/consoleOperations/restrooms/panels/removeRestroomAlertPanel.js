import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createRemoveRestroomAlertPanel() {
   return createPanelShell({
      panelId: 'removeRestroomAlertPanel',
      title: APP_STRINGS.panelTitles.removeRestroomAlert,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.restroom,
            inputId: 'removeRestroomAlertRestroom',
            emptyOptionLabel: APP_STRINGS.placeholders.restroom,
         }),
         createActions({
            submitId: 'submitRemoveRestroomAlert',
            submitLabel: APP_STRINGS.actions.removeAlert,
         }),
         createStatus({
            statusId: 'removeRestroomAlertStatus',
         }),
      ],
   });
}
