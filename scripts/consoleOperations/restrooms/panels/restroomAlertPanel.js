import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createRestroomAlertPanel() {
   return createPanelShell({
      panelId: 'restroomAlertPanel',
      title: 'Set restroom alert',
      bodyChildren: [
         createSelectField({
            label: 'Restroom',
            inputId: 'restroomAlertRestroom',
            emptyOptionLabel: 'Select a restroom',
         }),
         createDateRangeFields({
            startDateId: 'restroomAlertStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'restroomAlertEndDate',
            endHelpText: 'Leave blank to keep the alert active until manually removed.',
         }),
         createTextareaField({
            label: 'Alert message',
            inputId: 'restroomAlertMessage',
            placeholder: 'Example: Women\'s restroom is temporarily unavailable',
         }),
         createActions({
            submitId: 'submitRestroomAlert',
         }),
         createStatus({
            statusId: 'restroomAlertStatus',
         }),
      ],
   });
}
