import {
   createActionsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../templates/fragments.js';

export function createCancelGuardiansTalkOccurrencePanelHtml() {
   return createPanelShellHtml({
      panelId: 'cancelGuardiansTalkOccurrencePanel',
      title: 'Cancel Meet the Guardians talk occurrence',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Location',
   inputId: 'cancelGuardiansTalkOccurrenceLocation',
   emptyOptionLabel: 'Select a location',
})}
${createSelectFieldHtml({
   label: 'Talk name',
   inputId: 'cancelGuardiansTalkOccurrenceTalkName',
   emptyOptionLabel: 'Select a talk',
})}
${createSelectFieldHtml({
   label: 'Date',
   inputId: 'cancelGuardiansTalkOccurrenceDate',
   emptyOptionLabel: 'Select a date',
})}
${createSelectFieldHtml({
   label: 'Time',
   inputId: 'cancelGuardiansTalkOccurrenceTime',
   emptyOptionLabel: 'Select a time',
})}
${createActionsHtml({
   submitId: 'submitCancelGuardiansTalkOccurrence',
})}
${createStatusHtml({
   statusId: 'cancelGuardiansTalkOccurrenceStatus',
})}
      `,
   });
}
