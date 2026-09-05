import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export class TransportationStationOpenPanel {
   static createTransportationStationOpenPanel() {
      return createPanelShell({
         panelId: 'transportationStationOpenPanel',
         title: APP_STRINGS.panelTitles.transportationStationOpen,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.transportationStation,
               inputId: 'transportationStationOpenTransportationStation',
               emptyOptionLabel: APP_STRINGS.placeholders.transportationStation,
            }),
            createActions({
               submitId: 'submitTransportationStationOpen',
            }),
            createStatus({
               statusId: 'transportationStationOpenStatus',
            }),
         ],
      });
   }
}
