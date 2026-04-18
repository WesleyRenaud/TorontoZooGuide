import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSchedulePresetFieldHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
   createWeeklyScheduleCheckboxesHtml,
} from '../../templates/fragments.js';

export function createGiftShopOpenPanelHtml() {
   return createPanelShellHtml({
      panelId: 'giftShopOpenPanel',
      title: 'Set gift shop as open',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Gift shop',
   inputId: 'giftShopOpenGiftShop',
   emptyOptionLabel: 'Select a gift shop',
})}
${createSchedulePresetFieldHtml({
   inputId: 'giftShopOpenPreset',
})}
${createDateRangeFieldsHtml({
   startDateId: 'giftShopOpenStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'giftShopOpenEndDate',
   endHelpText: 'Leave blank to keep this schedule active until it is changed.',
})}
${createWeeklyScheduleCheckboxesHtml({
   dayIds: {
      monday: 'giftShopOpenMonday',
      tuesday: 'giftShopOpenTuesday',
      wednesday: 'giftShopOpenWednesday',
      thursday: 'giftShopOpenThursday',
      friday: 'giftShopOpenFriday',
      saturday: 'giftShopOpenSaturday',
      sunday: 'giftShopOpenSunday',
      holidays: 'giftShopOpenHolidaysOnly',
   },
})}
${createTextareaFieldHtml({
   label: 'Schedule message',
   inputId: 'giftShopOpenMessage',
   placeholder: 'Enter the message shown when the gift shop is closed outside this schedule',
})}
${createActionsHtml({
   submitId: 'submitGiftShopOpen',
})}
${createStatusHtml({
   statusId: 'giftShopOpenStatus',
})}
      `,
   });
}
