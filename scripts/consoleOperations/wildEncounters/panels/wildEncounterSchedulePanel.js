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

export function createWildEncounterSchedulePanel() {
   return createPanelShell({
      panelId: 'wildEncounterSchedulePanel',
      title: 'Set Wild Encounter schedule',
      bodyChildren: [
         createSelectField({
            label: 'Wild Encounter',
            inputId: 'wildEncounterScheduleName',
            emptyOptionLabel: 'Select a Wild Encounter',
         }),
         createDateRangeFields({
            startDateId: 'wildEncounterScheduleStartDate',
            endDateId: 'wildEncounterScheduleEndDate',
            endHelpText: 'Leave blank to continue until the schedule is ended.',
         }),
         createCheckboxGridField({
            label: 'Occurs on these days',
            options: [
               { id: 'wildEncounterScheduleMonday', label: 'Monday' },
               { id: 'wildEncounterScheduleTuesday', label: 'Tuesday' },
               { id: 'wildEncounterScheduleWednesday', label: 'Wednesday' },
               { id: 'wildEncounterScheduleThursday', label: 'Thursday' },
               { id: 'wildEncounterScheduleFriday', label: 'Friday' },
               { id: 'wildEncounterScheduleSaturday', label: 'Saturday' },
               { id: 'wildEncounterScheduleSunday', label: 'Sunday' },
            ],
         }),
         createDateField({
            label: 'Encounter time',
            inputId: 'wildEncounterScheduleTime',
            placeholder: 'Select an encounter time',
         }),
         createTextareaField({
            label: 'Schedule message',
            inputId: 'wildEncounterScheduleMessage',
            placeholder: 'Enter an optional message for this Wild Encounter schedule',
         }),
         createActions({
            submitId: 'submitWildEncounterSchedule',
         }),
         createStatus({
            statusId: 'wildEncounterScheduleStatus',
         }),
      ],
   });
}
