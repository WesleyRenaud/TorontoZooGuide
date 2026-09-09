import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class TransportationStationOpenView {
   static createTransportationStationOpenPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'transportationStationOpenPanel',
         title: Strings.panelTitles.transportationStationOpen,
         entityLabel: Strings.entityLabels.transportationStation,
         emptyOptionLabel: Strings.placeholders.transportationStation,
         idPrefix: 'transportationStationOpen',
         entityFieldName: 'TransportationStation',
         includeDateRange: false,
         submitId: 'submitTransportationStationOpen',
         statusId: 'transportationStationOpenStatus',
      });
   }
}
