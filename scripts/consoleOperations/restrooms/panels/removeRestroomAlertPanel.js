import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createRemoveRestroomAlertPanel() {
   return createPanelShell({
      panelId: 'removeRestroomAlertPanel',
      title: 'Remove restroom alert',
      bodyChildren: [
         createSelectField({
            label: 'Restroom',
            inputId: 'removeRestroomAlertRestroom',
            emptyOptionLabel: 'Select a restroom',
         }),
         createActions({
            submitId: 'submitRemoveRestroomAlert',
            submitLabel: 'Remove alert',
         }),
         createStatus({
            statusId: 'removeRestroomAlertStatus',
         }),
      ],
   });
}
