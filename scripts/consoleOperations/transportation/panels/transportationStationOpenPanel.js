import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class TransportationStationOpenPanel {
   static createTransportationStationOpenPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'transportationStationOpenPanel',
         title: Strings.panelTitles.transportationStationOpen,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.transportationStation,
               inputId: 'transportationStationOpenTransportationStation',
               emptyOptionLabel: Strings.placeholders.transportationStation,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitTransportationStationOpen',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'transportationStationOpenStatus',
            }),
         ],
      });
   }
}
