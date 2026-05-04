import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createStatus,
} from '../../templates/fragments.js';

export function createDrinkingFountainsOpenPanel() {
   return createPanelShell({
      panelId: 'drinkingFountainsOpenPanel',
      title: 'Open drinking fountains',
      bodyChildren: [
         createDateRangeFields({
            startDateId: 'drinkingFountainsOpenStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'drinkingFountainsOpenEndDate',
            endHelpText: 'Leave blank to keep the drinking fountains explicitly open until they are changed.',
         }),
         createActions({
            submitId: 'submitDrinkingFountainsOpen',
         }),
         createStatus({
            statusId: 'drinkingFountainsOpenStatus',
         }),
      ],
   });
}
