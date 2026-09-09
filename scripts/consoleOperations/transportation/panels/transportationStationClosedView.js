import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class TransportationStationClosedView {
   static createTransportationStationClosedPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'transportationStationClosedPanel',
         title: Strings.panelTitles.transportationStationClosed,
         entityLabel: Strings.entityLabels.transportationStation,
         emptyOptionLabel: Strings.placeholders.transportationStation,
         idPrefix: 'transportationStationClosed',
         entityFieldName: 'TransportationStation',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('transportation station'),
         messageLabel: Strings.labels.closureMessage,
         messagePlaceholder: Strings.textareas.closureMessage,
         submitId: 'submitTransportationStationClosed',
         statusId: 'transportationStationClosedStatus',
      });
   }
}
