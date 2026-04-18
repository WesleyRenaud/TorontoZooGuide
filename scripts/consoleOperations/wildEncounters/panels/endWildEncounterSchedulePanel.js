import {
   createActionsHtml,
   createDateFieldHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../templates/fragments.js';

export function createEndWildEncounterSchedulePanelHtml() {
   return createPanelShellHtml({
      panelId: 'endWildEncounterSchedulePanel',
      title: 'End Wild Encounter schedule',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Wild Encounter',
   inputId: 'endWildEncounterScheduleName',
   emptyOptionLabel: 'Select a Wild Encounter',
})}
${createDateFieldHtml({
   label: 'End date',
   inputId: 'endWildEncounterScheduleDate',
   placeholder: 'Select the date the schedule should end',
   helpText: 'Leave blank to end the schedule today.',
})}
${createActionsHtml({
   submitId: 'submitEndWildEncounterSchedule',
})}
${createStatusHtml({
   statusId: 'endWildEncounterScheduleStatus',
})}
      `,
   });
}
