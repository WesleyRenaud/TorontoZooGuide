import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createGiftShopClosedPanelHtml() {
   return createPanelShellHtml({
      panelId: 'giftShopClosedPanel',
      title: 'Set gift shop as closed',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Gift shop',
   inputId: 'giftShopClosedGiftShop',
   emptyOptionLabel: 'Select a gift shop',
})}
${createDateRangeFieldsHtml({
   startDateId: 'giftShopClosedStartDate',
   endDateId: 'giftShopClosedEndDate',
   endHelpText: 'Leave blank to continue until the gift shop is reopened.',
})}
${createTextareaFieldHtml({
   label: 'Closed message',
   inputId: 'giftShopClosedMessage',
   placeholder: 'Enter the message shown when the gift shop is closed',
})}
${createActionsHtml({
   submitId: 'submitGiftShopClosed',
})}
${createStatusHtml({
   statusId: 'giftShopClosedStatus',
})}
      `,
   });
}
