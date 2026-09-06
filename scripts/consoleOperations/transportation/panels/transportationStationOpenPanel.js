import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class TransportationStationOpenPanel {
   static createTransportationStationOpenPanel() {
      return Fragments.createPanelShell({
         panelId: 'transportationStationOpenPanel',
         title: Strings.panelTitles.transportationStationOpen,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.transportationStation,
               inputId: 'transportationStationOpenTransportationStation',
               emptyOptionLabel: Strings.placeholders.transportationStation,
            }),
            Fragments.createActions({
               submitId: 'submitTransportationStationOpen',
            }),
            Fragments.createStatus({
               statusId: 'transportationStationOpenStatus',
            }),
         ],
      });
   }
}
