import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class OnDisplayPanel {
   static createOnDisplayPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'onDisplayPanel',
         title: Strings.panelTitles.onDisplay,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'onDisplayExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'onDisplaySpecies',
               resultsId: 'onDisplaySpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.viewingScope,
               inputId: 'onDisplayViewingScope',
               emptyOptionLabel: Strings.placeholders.viewingScope,
               options: Strings.viewingScopes,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitOnDisplay',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'onDisplayStatus',
            }),
         ],
      });
   }
}
