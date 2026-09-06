import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class AttractionHoursSchedulePanel {
   static createAttractionHoursSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'attractionHoursSchedulePanel',
         title: Strings.panelTitles.attractionHoursSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionHoursScheduleAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'attractionHoursScheduleStartDate',
               startLabel: Strings.labels.scheduleStartDate,
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionHoursScheduleEndDate',
               endLabel: Strings.labels.scheduleEndDate,
               endHelpText: Strings.help.keepScheduleUntilChanged,
            }),
            Fragments.createDateField({
               label: Strings.labels.weekdayStartTime,
               inputId: 'attractionHoursScheduleWeekdayStartTime',
               placeholder: Strings.placeholders.weekdayStartTime,
            }),
            Fragments.createDateField({
               label: Strings.labels.weekdayEndTime,
               inputId: 'attractionHoursScheduleWeekdayEndTime',
               placeholder: Strings.placeholders.weekdayEndTime,
            }),
            Fragments.createDateField({
               label: Strings.labels.weekendHolidayStartTime,
               inputId: 'attractionHoursScheduleWeekendHolidayStartTime',
               placeholder: Strings.placeholders.weekendHolidayStartTime,
            }),
            Fragments.createDateField({
               label: Strings.labels.weekendHolidayEndTime,
               inputId: 'attractionHoursScheduleWeekendHolidayEndTime',
               placeholder: Strings.placeholders.weekendHolidayEndTime,
            }),
            Fragments.createActions({
               submitId: 'submitAttractionHoursSchedule',
            }),
            Fragments.createStatus({
               statusId: 'attractionHoursScheduleStatus',
            }),
         ],
      });
   }
}
