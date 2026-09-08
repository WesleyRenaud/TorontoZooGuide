import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSchedulePresetFieldBuilder } from '../../templates/consoleSchedulePresetFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleWeeklyScheduleCheckboxesBuilder } from '../../templates/consoleWeeklyScheduleCheckboxesBuilder.js';

export class AttractionOpeningScheduleView {
   static createAttractionOpeningSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'attractionOpeningSchedulePanel',
         title: Strings.panelTitles.attractionOpeningSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionOpeningScheduleAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            ConsoleSchedulePresetFieldBuilder.createSchedulePresetField({
               inputId: 'attractionOpeningSchedulePreset',
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'attractionOpeningScheduleStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionOpeningScheduleEndDate',
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes({
               dayIds: {
                  monday: 'attractionOpeningScheduleMonday',
                  tuesday: 'attractionOpeningScheduleTuesday',
                  wednesday: 'attractionOpeningScheduleWednesday',
                  thursday: 'attractionOpeningScheduleThursday',
                  friday: 'attractionOpeningScheduleFriday',
                  saturday: 'attractionOpeningScheduleSaturday',
                  sunday: 'attractionOpeningScheduleSunday',
                  holidays: 'attractionOpeningScheduleHolidaysOnly',
               },
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'attractionOpeningScheduleMessage',
               placeholder: Strings.textareas.scheduledClosedMessage('attraction'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitAttractionOpeningSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'attractionOpeningScheduleStatus',
            }),
         ],
      });
   }
}
