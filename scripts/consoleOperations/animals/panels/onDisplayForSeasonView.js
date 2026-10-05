import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsoleCheckboxGridFieldBuilder } from '../../templates/consoleCheckboxGridFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class OnDisplayForSeasonView {
   static createOnDisplayForSeasonPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'onDisplayForSeasonPanel',
         title: Strings.panelTitles.onDisplayForSeason,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'onDisplayForSeasonExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'onDisplayForSeasonSpecies',
               resultsId: 'onDisplayForSeasonSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleCheckboxGridFieldBuilder.createCheckboxGridField({
               label: Strings.labels.viewingScope,
               gridId: 'onDisplayForSeasonViewingScope',
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitOnDisplayForSeason',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'onDisplayForSeasonStatus',
            }),
         ],
      });
   }
}
