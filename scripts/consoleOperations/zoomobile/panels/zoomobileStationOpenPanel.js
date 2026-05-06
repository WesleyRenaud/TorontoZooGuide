import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createZoomobileStationOpenPanel() {
   return createPanelShell({
      panelId: 'zoomobileStationOpenPanel',
      title: APP_STRINGS.panelTitles.zoomobileStationOpen,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.zoomobileStation,
            inputId: 'zoomobileStationOpenZoomobileStation',
            emptyOptionLabel: APP_STRINGS.placeholders.zoomobileStation,
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
