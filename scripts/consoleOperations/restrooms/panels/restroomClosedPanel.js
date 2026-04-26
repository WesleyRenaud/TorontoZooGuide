import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createRestroomClosedPanel() {
   return createPanelShell({
      panelId: 'restroomClosedPanel',
      title: 'Set restroom as closed',
      bodyChildren: [
         createSelectField({
            label: 'Restroom',
            inputId: 'restroomClosedRestroom',
            emptyOptionLabel: 'Select a restroom',
         }),
         createDateRangeFields({
            startDateId: 'restroomClosedStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'restroomClosedEndDate',
            endHelpText: 'Leave blank to continue until the restroom is reopened.',
         }),
         createTextareaField({
            label: 'Closed message',
            inputId: 'restroomClosedMessage',
            placeholder: 'Enter the message shown when the restroom is closed',
         }),
         createActions({
            submitId: 'submitRestroomClosed',
         }),
         createStatus({
            statusId: 'restroomClosedStatus',
         }),
      ],
   });
}
