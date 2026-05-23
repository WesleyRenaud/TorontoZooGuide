import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateField,
   createDateRangeFields,
   createPanelShell,
   createRadioGroupField,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

function createWeekdayTimeField(dayKey) {
   const dayLabel = APP_STRINGS.schedule.dayLabels[dayKey];

   return createDateField({
      label: `${dayLabel} time`,
      inputId: `guardiansTalkSchedule${dayLabel}Time`,
      placeholder: APP_STRINGS.placeholders.scheduledTime(`${dayLabel.toLowerCase()} talk`),
   });
}

function createTimeModeField() {
   return createRadioGroupField({
      label: APP_STRINGS.labels.scheduleMode,
      name: 'guardiansTalkScheduleMode',
      options: [
         {
            id: 'guardiansTalkScheduleSameTimeEveryDayMode',
            value: 'sameTimeEveryDay',
            label: APP_STRINGS.schedule.guardiansTalkTimeModeLabels.sameTimeEveryDay,
            checked: true,
         },
         {
            id: 'guardiansTalkScheduleWeekdayTimesMode',
            value: 'weekdayTimes',
            label: APP_STRINGS.schedule.guardiansTalkTimeModeLabels.weekdayTimes,
         },
      ],
   });
}

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
         createTimeModeField(),
         createDateField({
            label: APP_STRINGS.labels.talkTimeEveryDay,
            inputId: 'guardiansTalkScheduleDailyTime',
            placeholder: APP_STRINGS.placeholders.scheduledTime('a talk'),
         }),
         createWeekdayTimeField('monday'),
         createWeekdayTimeField('tuesday'),
         createWeekdayTimeField('wednesday'),
         createWeekdayTimeField('thursday'),
         createWeekdayTimeField('friday'),
         createWeekdayTimeField('saturday'),
         createWeekdayTimeField('sunday'),
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
