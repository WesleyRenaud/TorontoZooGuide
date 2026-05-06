import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createCheckboxGridField,
   createDateField,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createGuardiansTalkSchedulePanel() {
   return createPanelShell({
      panelId: 'guardiansTalkSchedulePanel',
      title: APP_STRINGS.panelTitles.guardiansTalkSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.location,
            inputId: 'guardiansTalkScheduleLocation',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createSelectField({
            label: APP_STRINGS.labels.talkName,
            inputId: 'guardiansTalkScheduleTalkName',
            emptyOptionLabel: APP_STRINGS.placeholders.talk,
         }),
         createDateRangeFields({
            startDateId: 'guardiansTalkScheduleStartDate',
            endDateId: 'guardiansTalkScheduleEndDate',
            endHelpText: APP_STRINGS.help.continueUntilScheduleEnded,
         }),
         createCheckboxGridField({
            label: APP_STRINGS.labels.occursOnTheseDays,
            options: [
               { id: 'guardiansTalkScheduleMonday', label: APP_STRINGS.schedule.dayLabels.monday },
               { id: 'guardiansTalkScheduleTuesday', label: APP_STRINGS.schedule.dayLabels.tuesday },
               { id: 'guardiansTalkScheduleWednesday', label: APP_STRINGS.schedule.dayLabels.wednesday },
               { id: 'guardiansTalkScheduleThursday', label: APP_STRINGS.schedule.dayLabels.thursday },
               { id: 'guardiansTalkScheduleFriday', label: APP_STRINGS.schedule.dayLabels.friday },
               { id: 'guardiansTalkScheduleSaturday', label: APP_STRINGS.schedule.dayLabels.saturday },
               { id: 'guardiansTalkScheduleSunday', label: APP_STRINGS.schedule.dayLabels.sunday },
            ],
         }),
         createDateField({
            label: APP_STRINGS.labels.talkTime,
            inputId: 'guardiansTalkScheduleTime',
            placeholder: APP_STRINGS.placeholders.scheduledTime('a talk'),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.scheduleMessage,
            inputId: 'guardiansTalkScheduleMessage',
            placeholder: APP_STRINGS.textareas.optionalScheduleMessage('talk'),
         }),
         createActions({
            submitId: 'submitGuardiansTalkSchedule',
         }),
         createStatus({
            statusId: 'guardiansTalkScheduleStatus',
         }),
      ],
   });
}
