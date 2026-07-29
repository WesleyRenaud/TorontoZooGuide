import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateField,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createAttractionHoursSchedulePanel() {
   return createPanelShell({
      panelId: 'attractionHoursSchedulePanel',
      title: APP_STRINGS.panelTitles.attractionHoursSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.attraction,
            inputId: 'attractionHoursScheduleAttraction',
            emptyOptionLabel: APP_STRINGS.placeholders.attraction,
         }),
         createDateRangeFields({
            startDateId: 'attractionHoursScheduleStartDate',
            startLabel: APP_STRINGS.labels.scheduleStartDate,
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'attractionHoursScheduleEndDate',
            endLabel: APP_STRINGS.labels.scheduleEndDate,
            endHelpText: APP_STRINGS.help.keepScheduleUntilChanged,
         }),
         createDateField({
            label: APP_STRINGS.labels.weekdayStartTime,
            inputId: 'attractionHoursScheduleWeekdayStartTime',
            placeholder: APP_STRINGS.placeholders.weekdayStartTime,
         }),
         createDateField({
            label: APP_STRINGS.labels.weekdayEndTime,
            inputId: 'attractionHoursScheduleWeekdayEndTime',
            placeholder: APP_STRINGS.placeholders.weekdayEndTime,
         }),
         createDateField({
            label: APP_STRINGS.labels.weekendHolidayStartTime,
            inputId: 'attractionHoursScheduleWeekendHolidayStartTime',
            placeholder: APP_STRINGS.placeholders.weekendHolidayStartTime,
         }),
         createDateField({
            label: APP_STRINGS.labels.weekendHolidayEndTime,
            inputId: 'attractionHoursScheduleWeekendHolidayEndTime',
            placeholder: APP_STRINGS.placeholders.weekendHolidayEndTime,
         }),
         createActions({
            submitId: 'submitAttractionHoursSchedule',
         }),
         createStatus({
            statusId: 'attractionHoursScheduleStatus',
         }),
      ],
   });
}
