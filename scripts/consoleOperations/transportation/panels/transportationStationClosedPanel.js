import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export class TransportationStationClosedPanel {
   static createTransportationStationClosedPanel() {
      return createPanelShell({
         panelId: 'transportationStationClosedPanel',
         title: APP_STRINGS.panelTitles.transportationStationClosed,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.transportationStation,
               inputId: 'transportationStationClosedTransportationStation',
               emptyOptionLabel: APP_STRINGS.placeholders.transportationStation,
            }),
            createDateRangeFields({
               startDateId: 'transportationStationClosedStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'transportationStationClosedEndDate',
               endHelpText: APP_STRINGS.help.keepClosedUntilManuallyReopened('transportation station'),
            }),
            createTextareaField({
               label: APP_STRINGS.labels.closureMessage,
               inputId: 'transportationStationClosedMessage',
               placeholder: APP_STRINGS.textareas.closureMessage,
            }),
            createActions({
               submitId: 'submitTransportationStationClosed',
            }),
            createStatus({
               statusId: 'transportationStationClosedStatus',
            }),
         ],
      });
   }
}
