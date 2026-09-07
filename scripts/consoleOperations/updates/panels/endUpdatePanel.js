import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class EndUpdatePanel {
   static createEndUpdatePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'endUpdatePanel',
         title: Strings.panelTitles.endUpdate,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.update,
               inputId: 'endUpdateKey',
               emptyOptionLabel: Strings.placeholders.update,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.endDate,
               inputId: 'endUpdateEndDate',
               placeholder: Strings.placeholders.endDate,
               helpText: Strings.help.endUpdateToday,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitEndUpdate',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'endUpdateStatus',
            }),
         ],
      });
   }
}
