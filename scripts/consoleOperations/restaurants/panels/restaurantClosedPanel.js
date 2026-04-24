import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createRestaurantClosedPanel() {
   return createPanelShell({
      panelId: 'restaurantClosedPanel',
      title: 'Set restaurant as closed',
      bodyChildren: [
         createSelectField({
            label: 'Restaurant',
            inputId: 'restaurantClosedRestaurant',
            emptyOptionLabel: 'Select a restaurant',
         }),
         createDateRangeFields({
            startDateId: 'restaurantClosedStartDate',
            endDateId: 'restaurantClosedEndDate',
            endHelpText: 'Leave blank to continue until the restaurant is reopened.',
         }),
         createTextareaField({
            label: 'Closed message',
            inputId: 'restaurantClosedMessage',
            placeholder: 'Enter the message shown when the restaurant is closed',
         }),
         createActions({
            submitId: 'submitRestaurantClosed',
         }),
         createStatus({
            statusId: 'restaurantClosedStatus',
         }),
      ],
   });
}
