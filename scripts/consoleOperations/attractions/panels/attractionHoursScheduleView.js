import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class AttractionHoursScheduleView {
   static createAttractionHoursSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'attractionHoursSchedulePanel',
         title: Strings.panelTitles.attractionHoursSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionHoursScheduleAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'attractionHoursScheduleStartDate',
               startLabel: Strings.labels.scheduleStartDate,
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionHoursScheduleEndDate',
               endLabel: Strings.labels.scheduleEndDate,
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.weekdayStartTime,
               inputId: 'attractionHoursScheduleWeekdayStartTime',
               placeholder: Strings.placeholders.weekdayStartTime,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.weekdayEndTime,
               inputId: 'attractionHoursScheduleWeekdayEndTime',
               placeholder: Strings.placeholders.weekdayEndTime,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.weekendHolidayStartTime,
               inputId: 'attractionHoursScheduleWeekendHolidayStartTime',
               placeholder: Strings.placeholders.weekendHolidayStartTime,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.weekendHolidayEndTime,
               inputId: 'attractionHoursScheduleWeekendHolidayEndTime',
               placeholder: Strings.placeholders.weekendHolidayEndTime,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitAttractionHoursSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'attractionHoursScheduleStatus',
            }),
         ],
      });
   }
}
