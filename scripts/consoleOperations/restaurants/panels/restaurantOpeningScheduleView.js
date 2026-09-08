import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSchedulePresetFieldBuilder } from '../../templates/consoleSchedulePresetFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleWeeklyScheduleCheckboxesBuilder } from '../../templates/consoleWeeklyScheduleCheckboxesBuilder.js';

export class RestaurantOpeningScheduleView {
   static createRestaurantOpeningSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'restaurantOpeningSchedulePanel',
         title: Strings.panelTitles.restaurantOpeningSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restaurant,
               inputId: 'restaurantOpeningScheduleRestaurant',
               emptyOptionLabel: Strings.placeholders.restaurant,
            }),
            ConsoleSchedulePresetFieldBuilder.createSchedulePresetField({
               inputId: 'restaurantOpeningSchedulePreset',
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'restaurantOpeningScheduleStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restaurantOpeningScheduleEndDate',
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes({
               dayIds: {
                  monday: 'restaurantOpeningScheduleMonday',
                  tuesday: 'restaurantOpeningScheduleTuesday',
                  wednesday: 'restaurantOpeningScheduleWednesday',
                  thursday: 'restaurantOpeningScheduleThursday',
                  friday: 'restaurantOpeningScheduleFriday',
                  saturday: 'restaurantOpeningScheduleSaturday',
                  sunday: 'restaurantOpeningScheduleSunday',
                  holidays: 'restaurantOpeningScheduleHolidaysOnly',
               },
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'restaurantOpeningScheduleMessage',
               placeholder: Strings.textareas.scheduledClosedMessage('restaurant'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRestaurantOpeningSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'restaurantOpeningScheduleStatus',
            }),
         ],
      });
   }
}
