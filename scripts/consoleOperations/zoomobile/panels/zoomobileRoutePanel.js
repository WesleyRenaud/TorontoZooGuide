import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createRadioGroupField,
   createStatus,
} from '../../templates/fragments.js';

export function createZoomobileRoutePanel() {
   return createPanelShell({
      panelId: 'zoomobileRoutePanel',
      title: 'Set current Zoomobile route',
      bodyChildren: [
         createRadioGroupField({
            label: 'Route',
            name: 'zoomobileRoute',
            options: [
               { id: 'zoomobileRouteSummer', value: 'summer', label: 'Summer' },
               { id: 'zoomobileRouteWinter', value: 'winter', label: 'Winter' },
            ],
         }),
         createDateRangeFields({
            startDateId: 'zoomobileRouteStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'zoomobileRouteEndDate',
            endHelpText: 'Leave blank to keep this route until it is changed again.',
         }),
         createActions({
            submitId: 'submitZoomobileRoute',
         }),
         createStatus({
            statusId: 'zoomobileRouteStatus',
         }),
      ],
   });
}
