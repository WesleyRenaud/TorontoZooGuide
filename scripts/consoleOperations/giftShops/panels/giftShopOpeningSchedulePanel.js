import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class GiftShopOpeningSchedulePanel {
   static createGiftShopOpeningSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'giftShopOpeningSchedulePanel',
         title: Strings.panelTitles.giftShopOpeningSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.giftShop,
               inputId: 'giftShopOpeningScheduleGiftShop',
               emptyOptionLabel: Strings.placeholders.giftShop,
            }),
            Fragments.createSchedulePresetField({
               inputId: 'giftShopOpeningSchedulePreset',
            }),
            Fragments.createDateRangeFields({
               startDateId: 'giftShopOpeningScheduleStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'giftShopOpeningScheduleEndDate',
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            Fragments.createWeeklyScheduleCheckboxes({
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
            Fragments.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'giftShopOpeningScheduleMessage',
               placeholder: Strings.textareas.scheduledClosedMessage('gift shop'),
            }),
            Fragments.createActions({
               submitId: 'submitGiftShopOpeningSchedule',
            }),
            Fragments.createStatus({
               statusId: 'giftShopOpeningScheduleStatus',
            }),
         ],
      });
   }
}
