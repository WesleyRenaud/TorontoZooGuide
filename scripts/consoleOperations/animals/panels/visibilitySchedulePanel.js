import {
   createActions,
   createAutocompleteField,
   createDateRangeFields,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createVisibilitySchedulePanel() {
   return createPanelShell({
      panelId: 'visibilitySchedulePanel',
      title: 'Set animal visibility schedule',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'visibilityScheduleExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createAutocompleteField({
            label: 'Species',
            inputId: 'visibilityScheduleSpecies',
            resultsId: 'visibilityScheduleSpeciesResults',
            placeholder: 'Search for a species',
         }),
         createDateRangeFields({
            startDateId: 'visibilityScheduleStartDate',
            startLabel: 'Schedule start date',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'visibilityScheduleEndDate',
            endLabel: 'Schedule end date',
            endHelpText: 'Leave blank to keep this visibility schedule in place until manually changed.',
         }),
         createDateField({
            label: 'Daily viewing start time',
            inputId: 'visibilityScheduleDailyStartTime',
            placeholder: 'Select a daily start time',
         }),
         createDateField({
            label: 'Daily viewing end time',
            inputId: 'visibilityScheduleDailyEndTime',
            placeholder: 'Select a daily end time',
         }),
         createTextareaField({
            label: 'Message',
            inputId: 'visibilityScheduleMessage',
            placeholder: 'Enter the viewing message shown to guests',
         }),
         createActions({
            submitId: 'submitVisibilitySchedule',
         }),
         createStatus({
            statusId: 'visibilityScheduleStatus',
         }),
      ],
   });
}
