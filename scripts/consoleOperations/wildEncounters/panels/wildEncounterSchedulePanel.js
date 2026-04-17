import {
   createActionsHtml,
   createCheckboxGridFieldHtml,
   createDateFieldHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createWildEncounterSchedulePanelHtml() {
   return createPanelShellHtml({
      panelId: 'wildEncounterSchedulePanel',
      title: 'Set Wild Encounter schedule',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Wild Encounter',
   inputId: 'wildEncounterScheduleName',
   emptyOptionLabel: 'Select a Wild Encounter',
})}
${createDateRangeFieldsHtml({
   startDateId: 'wildEncounterScheduleStartDate',
   endDateId: 'wildEncounterScheduleEndDate',
   endHelpText: 'Leave blank to continue until the schedule is ended.',
})}
${createCheckboxGridFieldHtml({
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
})}
${createDateFieldHtml({
   label: 'Encounter time',
   inputId: 'wildEncounterScheduleTime',
   placeholder: 'Select an encounter time',
})}
${createTextareaFieldHtml({
   label: 'Schedule message',
   inputId: 'wildEncounterScheduleMessage',
   placeholder: 'Enter an optional message for this Wild Encounter schedule',
})}
${createActionsHtml({
   submitId: 'submitWildEncounterSchedule',
})}
${createStatusHtml({
   statusId: 'wildEncounterScheduleStatus',
})}
      `,
   });
}
