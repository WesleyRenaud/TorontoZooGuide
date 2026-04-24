import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createZoomobileStationClosedPanel() {
   return createPanelShell({
      panelId: 'zoomobileStationClosedPanel',
      title: 'Set zoomobile station as closed',
      bodyChildren: [
         createSelectField({
            label: 'Zoomobile Station',
            inputId: 'zoomobileStationClosedZoomobileStation',
            emptyOptionLabel: 'Select a zoomobile station',
         }),
         createDateRangeFields({
            startDateId: 'zoomobileStationClosedStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'zoomobileStationClosedEndDate',
            endHelpText: 'Leave blank to keep the zoomobile station closed until it is manually reopened.',
         }),
         createTextareaField({
            label: 'Closure message',
            inputId: 'zoomobileStationClosedMessage',
            placeholder: 'Enter the closure message shown to guests',
         }),
         createActions({
            submitId: 'submitZoomobileStationClosed',
         }),
         createStatus({
            statusId: 'zoomobileStationClosedStatus',
         }),
      ],
   });
}
