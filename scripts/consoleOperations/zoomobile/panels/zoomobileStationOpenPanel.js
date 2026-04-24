import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createZoomobileStationOpenPanel() {
   return createPanelShell({
      panelId: 'zoomobileStationOpenPanel',
      title: 'Set zoomobile station as open',
      bodyChildren: [
         createSelectField({
            label: 'Zoomobile Station',
            inputId: 'zoomobileStationOpenZoomobileStation',
            emptyOptionLabel: 'Select a zoomobile station',
         }),
         createActions({
            submitId: 'submitZoomobileStationOpen',
         }),
         createStatus({
            statusId: 'zoomobileStationOpenStatus',
         }),
      ],
   });
}
