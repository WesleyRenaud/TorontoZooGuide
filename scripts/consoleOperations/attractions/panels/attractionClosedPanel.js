import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createAttractionClosedPanelHtml() {
   return createPanelShellHtml({
      panelId: 'attractionClosedPanel',
      title: 'Set attraction as closed',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Attraction',
   inputId: 'attractionClosedAttraction',
   emptyOptionLabel: 'Select an attraction',
})}
${createDateRangeFieldsHtml({
   startDateId: 'attractionClosedStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'attractionClosedEndDate',
   endHelpText: 'Leave blank to keep the attraction closed until it is manually reopened.',
})}
${createTextareaFieldHtml({
   label: 'Closure message',
   inputId: 'attractionClosedMessage',
   placeholder: 'Enter the closure message shown to guests',
})}
${createActionsHtml({
   submitId: 'submitAttractionClosed',
})}
${createStatusHtml({
   statusId: 'attractionClosedStatus',
})}
      `,
   });
}
