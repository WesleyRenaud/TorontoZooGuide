import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class RemoveRestroomAlertPanel {
   static createRemoveRestroomAlertPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'removeRestroomAlertPanel',
         title: Strings.panelTitles.removeRestroomAlert,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'removeRestroomAlertRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRemoveRestroomAlert',
               submitLabel: Strings.actions.removeAlert,
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'removeRestroomAlertStatus',
            }),
         ],
      });
   }
}
