import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createZoomobileStationClosedPanelHtml() {
   return createPanelShellHtml({
      panelId: 'zoomobileStationClosedPanel',
      title: 'Set zoomobile station as closed',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Zoomobile Station',
   inputId: 'zoomobileStationClosedZoomobileStation',
   emptyOptionLabel: 'Select a zoomobile station',
})}
${createDateRangeFieldsHtml({
   startDateId: 'zoomobileStationClosedStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'zoomobileStationClosedEndDate',
   endHelpText: 'Leave blank to keep the zoomobile station closed until it is manually reopened.',
})}
${createTextareaFieldHtml({
   label: 'Closure message',
   inputId: 'zoomobileStationClosedMessage',
   placeholder: 'Enter the closure message shown to guests',
})}
${createActionsHtml({
   submitId: 'submitZoomobileStationClosed',
})}
${createStatusHtml({
   statusId: 'zoomobileStationClosedStatus',
})}
      `,
   });
}
