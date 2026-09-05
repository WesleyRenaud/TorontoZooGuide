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

export class GiftShopOpeningSchedulePanel {
   static createGiftShopOpeningSchedulePanel() {
      return createPanelShell({
         panelId: 'giftShopOpeningSchedulePanel',
         title: APP_STRINGS.panelTitles.giftShopOpeningSchedule,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.giftShop,
               inputId: 'giftShopOpeningScheduleGiftShop',
               emptyOptionLabel: APP_STRINGS.placeholders.giftShop,
            }),
            createSchedulePresetField({
               inputId: 'giftShopOpeningSchedulePreset',
            }),
            createDateRangeFields({
               startDateId: 'giftShopOpeningScheduleStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'giftShopOpeningScheduleEndDate',
               endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
            }),
            createWeeklyScheduleCheckboxes({
               dayIds: {
                  monday: 'giftShopOpeningScheduleMonday',
                  tuesday: 'giftShopOpeningScheduleTuesday',
                  wednesday: 'giftShopOpeningScheduleWednesday',
                  thursday: 'giftShopOpeningScheduleThursday',
                  friday: 'giftShopOpeningScheduleFriday',
                  saturday: 'giftShopOpeningScheduleSaturday',
                  sunday: 'giftShopOpeningScheduleSunday',
                  holidays: 'giftShopOpeningScheduleHolidaysOnly',
               },
            }),
            createTextareaField({
               label: APP_STRINGS.labels.scheduleMessage,
               inputId: 'giftShopOpeningScheduleMessage',
               placeholder: APP_STRINGS.textareas.scheduledClosedMessage('gift shop'),
            }),
            createActions({
               submitId: 'submitGiftShopOpeningSchedule',
            }),
            createStatus({
               statusId: 'giftShopOpeningScheduleStatus',
            }),
         ],
      });
   }
}
