import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createRestaurantClosedPanelHtml() {
   return createPanelShellHtml({
      panelId: 'restaurantClosedPanel',
      title: 'Set restaurant as closed',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Restaurant',
   inputId: 'restaurantClosedRestaurant',
   emptyOptionLabel: 'Select a restaurant',
})}
${createDateRangeFieldsHtml({
   startDateId: 'restaurantClosedStartDate',
   endDateId: 'restaurantClosedEndDate',
   endHelpText: 'Leave blank to continue until the restaurant is reopened.',
})}
${createTextareaFieldHtml({
   label: 'Closed message',
   inputId: 'restaurantClosedMessage',
   placeholder: 'Enter the message shown when the restaurant is closed',
})}
${createActionsHtml({
   submitId: 'submitRestaurantClosed',
})}
${createStatusHtml({
   statusId: 'restaurantClosedStatus',
})}
      `,
   });
}
