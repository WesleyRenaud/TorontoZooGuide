import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class RemoveViewingAlertView {
   static createRemoveViewingAlertPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'removeViewingAlertPanel',
         title: Strings.panelTitles.removeViewingAlert,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'removeViewingAlertExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'removeViewingAlertSpecies',
               resultsId: 'removeViewingAlertSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRemoveViewingAlert',
               submitLabel: Strings.actions.removeAlert,
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'removeViewingAlertStatus',
            }),
         ],
      });
   }
}
