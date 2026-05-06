import { APP_STRINGS } from '../../../strings.js';
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
      title: APP_STRINGS.panelTitles.giftShopOpen,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.giftShop,
            inputId: 'giftShopOpenGiftShop',
            emptyOptionLabel: APP_STRINGS.placeholders.giftShop,
         }),
         createSchedulePresetField({
            inputId: 'giftShopOpenPreset',
         }),
         createDateRangeFields({
            startDateId: 'giftShopOpenStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'giftShopOpenEndDate',
            endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
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
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'giftShopOpenMessage',
            placeholder: APP_STRINGS.textareas.scheduledClosedMessage('gift shop'),
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
