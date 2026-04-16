import {
   createActionsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../shared/panelFragments.js';

export function createCancelWildEncounterOccurrencePanelHtml() {
   return createPanelShellHtml({
      panelId: 'cancelWildEncounterOccurrencePanel',
      title: 'Cancel Wild Encounter occurrence',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Wild Encounter',
   inputId: 'cancelWildEncounterOccurrenceName',
   emptyOptionLabel: 'Select a Wild Encounter',
})}
${createSelectFieldHtml({
   label: 'Date',
   inputId: 'cancelWildEncounterOccurrenceDate',
   emptyOptionLabel: 'Select a date',
})}
${createSelectFieldHtml({
   label: 'Time',
   inputId: 'cancelWildEncounterOccurrenceTime',
   emptyOptionLabel: 'Select a time',
})}
${createActionsHtml({
   submitId: 'submitCancelWildEncounterOccurrence',
})}
${createStatusHtml({
   statusId: 'cancelWildEncounterOccurrenceStatus',
})}
      `,
   });
}
