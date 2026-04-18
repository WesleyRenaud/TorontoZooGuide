import {
   createActionsHtml,
   createAutocompleteFieldHtml,
   createDateRangeFieldsHtml,
   createDateFieldHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createVisibilitySchedulePanelHtml() {
   return createPanelShellHtml({
      panelId: 'visibilitySchedulePanel',
      title: 'Set animal visibility schedule',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'visibilityScheduleExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createAutocompleteFieldHtml({
   label: 'Species',
   inputId: 'visibilityScheduleSpecies',
   resultsId: 'visibilityScheduleSpeciesResults',
   placeholder: 'Search for a species',
})}
${createDateRangeFieldsHtml({
   startDateId: 'visibilityScheduleStartDate',
   startLabel: 'Schedule start date',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'visibilityScheduleEndDate',
   endLabel: 'Schedule end date',
   endHelpText: 'Leave blank to keep this visibility schedule in place until manually changed.',
})}
${createDateFieldHtml({
   label: 'Daily viewing start time',
   inputId: 'visibilityScheduleDailyStartTime',
   placeholder: 'Select a daily start time',
})}
${createDateFieldHtml({
   label: 'Daily viewing end time',
   inputId: 'visibilityScheduleDailyEndTime',
   placeholder: 'Select a daily end time',
})}
${createTextareaFieldHtml({
   label: 'Message',
   inputId: 'visibilityScheduleMessage',
   placeholder: 'Enter the viewing message shown to guests',
})}
${createActionsHtml({
   submitId: 'submitVisibilitySchedule',
})}
${createStatusHtml({
   statusId: 'visibilityScheduleStatus',
})}
      `,
   });
}
