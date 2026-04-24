import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createGiftShopClosedPanel() {
   return createPanelShell({
      panelId: 'giftShopClosedPanel',
      title: 'Set gift shop as closed',
      bodyChildren: [
         createSelectField({
            label: 'Gift shop',
            inputId: 'giftShopClosedGiftShop',
            emptyOptionLabel: 'Select a gift shop',
         }),
         createDateRangeFields({
            startDateId: 'giftShopClosedStartDate',
            endDateId: 'giftShopClosedEndDate',
            endHelpText: 'Leave blank to continue until the gift shop is reopened.',
         }),
         createTextareaField({
            label: 'Closed message',
            inputId: 'giftShopClosedMessage',
            placeholder: 'Enter the message shown when the gift shop is closed',
         }),
         createActions({
            submitId: 'submitGiftShopClosed',
         }),
         createStatus({
            statusId: 'giftShopClosedStatus',
         }),
      ],
   });
}
