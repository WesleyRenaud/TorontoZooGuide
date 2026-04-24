import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSchedulePresetField,
   createSelectField,
   createStatus,
   createTextareaField,
   createWeeklyScheduleCheckboxes,
} from '../../templates/fragments.js';

export function createGiftShopOpenPanel() {
   return createPanelShell({
      panelId: 'giftShopOpenPanel',
      title: 'Set gift shop as open',
      bodyChildren: [
         createSelectField({
            label: 'Gift shop',
            inputId: 'giftShopOpenGiftShop',
            emptyOptionLabel: 'Select a gift shop',
         }),
         createSchedulePresetField({
            inputId: 'giftShopOpenPreset',
         }),
         createDateRangeFields({
            startDateId: 'giftShopOpenStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'giftShopOpenEndDate',
            endHelpText: 'Leave blank to keep this schedule active until it is changed.',
         }),
         createWeeklyScheduleCheckboxes({
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
         }),
         createTextareaField({
            label: 'Schedule message',
            inputId: 'giftShopOpenMessage',
            placeholder: 'Enter the message shown when the gift shop is closed outside this schedule',
         }),
         createActions({
            submitId: 'submitGiftShopOpen',
         }),
         createStatus({
            statusId: 'giftShopOpenStatus',
         }),
      ],
   });
}
