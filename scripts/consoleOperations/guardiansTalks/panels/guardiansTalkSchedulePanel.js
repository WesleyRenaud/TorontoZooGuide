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
      title: 'Set Meet the Guardians talk schedule',
      bodyChildren: [
         createSelectField({
            label: 'Location',
            inputId: 'guardiansTalkScheduleLocation',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createSelectField({
            label: 'Talk name',
            inputId: 'guardiansTalkScheduleTalkName',
            emptyOptionLabel: 'Select a talk',
         }),
         createDateRangeFields({
            startDateId: 'guardiansTalkScheduleStartDate',
            endDateId: 'guardiansTalkScheduleEndDate',
            endHelpText: 'Leave blank to continue until the schedule is ended.',
         }),
         createCheckboxGridField({
            label: 'Occurs on these days',
            options: [
               { id: 'guardiansTalkScheduleMonday', label: 'Monday' },
               { id: 'guardiansTalkScheduleTuesday', label: 'Tuesday' },
               { id: 'guardiansTalkScheduleWednesday', label: 'Wednesday' },
               { id: 'guardiansTalkScheduleThursday', label: 'Thursday' },
               { id: 'guardiansTalkScheduleFriday', label: 'Friday' },
               { id: 'guardiansTalkScheduleSaturday', label: 'Saturday' },
               { id: 'guardiansTalkScheduleSunday', label: 'Sunday' },
            ],
         }),
         createDateField({
            label: 'Talk time',
            inputId: 'guardiansTalkScheduleTime',
            placeholder: 'Select a talk time',
         }),
         createTextareaField({
            label: 'Schedule message',
            inputId: 'guardiansTalkScheduleMessage',
            placeholder: 'Enter an optional message for this talk schedule',
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
