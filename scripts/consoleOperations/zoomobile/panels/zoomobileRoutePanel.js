import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createRadioGroupFieldHtml,
   createStatusHtml,
} from '../../templates/fragments.js';

export function createZoomobileRoutePanelHtml() {
   return createPanelShellHtml({
      panelId: 'zoomobileRoutePanel',
      title: 'Set current Zoomobile route',
      bodyHtml: `
${createRadioGroupFieldHtml({
   label: 'Route',
   name: 'zoomobileRoute',
   options: [
      { id: 'zoomobileRouteSummer', value: 'summer', label: 'Summer' },
      { id: 'zoomobileRouteWinter', value: 'winter', label: 'Winter' },
   ],
})}
${createDateRangeFieldsHtml({
   startDateId: 'zoomobileRouteStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'zoomobileRouteEndDate',
   endHelpText: 'Leave blank to keep this route until it is changed again.',
})}
${createActionsHtml({
   submitId: 'submitZoomobileRoute',
})}
${createStatusHtml({
   statusId: 'zoomobileRouteStatus',
})}
      `,
   });
}
