import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSchedulePresetFieldBuilder } from '../../templates/consoleSchedulePresetFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleWeeklyScheduleCheckboxesBuilder } from '../../templates/consoleWeeklyScheduleCheckboxesBuilder.js';

export class GiftShopOpeningSchedulePanel {
   static createGiftShopOpeningSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'giftShopOpeningSchedulePanel',
         title: Strings.panelTitles.giftShopOpeningSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.giftShop,
               inputId: 'giftShopOpeningScheduleGiftShop',
               emptyOptionLabel: Strings.placeholders.giftShop,
            }),
            ConsoleSchedulePresetFieldBuilder.createSchedulePresetField({
               inputId: 'giftShopOpeningSchedulePreset',
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'giftShopOpeningScheduleStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'giftShopOpeningScheduleEndDate',
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes({
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
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'giftShopOpeningScheduleMessage',
               placeholder: Strings.textareas.scheduledClosedMessage('gift shop'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitGiftShopOpeningSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'giftShopOpeningScheduleStatus',
            }),
         ],
      });
   }
}
