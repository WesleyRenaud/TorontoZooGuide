import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createDrinkingFountainsClosedPanel() {
   return createPanelShell({
      panelId: 'drinkingFountainsClosedPanel',
      title: 'Close drinking fountains',
      bodyChildren: [
         createDateRangeFields({
            startDateId: 'drinkingFountainsClosedStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'drinkingFountainsClosedEndDate',
            endHelpText: 'Leave blank to continue until the drinking fountains are reopened.',
         }),
         createTextareaField({
            label: 'Closed message',
            inputId: 'drinkingFountainsClosedMessage',
            placeholder: 'Optional message shown while drinking fountains are closed',
         }),
         createActions({
            submitId: 'submitDrinkingFountainsClosed',
         }),
         createStatus({
            statusId: 'drinkingFountainsClosedStatus',
         }),
      ],
   });
}
