import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class TransportationStationClosedPanel {
   static createTransportationStationClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'transportationStationClosedPanel',
         title: Strings.panelTitles.transportationStationClosed,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.transportationStation,
               inputId: 'transportationStationClosedTransportationStation',
               emptyOptionLabel: Strings.placeholders.transportationStation,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'transportationStationClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'transportationStationClosedEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('transportation station'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'transportationStationClosedMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            Fragments.createActions({
               submitId: 'submitTransportationStationClosed',
            }),
            Fragments.createStatus({
               statusId: 'transportationStationClosedStatus',
            }),
         ],
      });
   }
}
