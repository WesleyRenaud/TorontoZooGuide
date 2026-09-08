import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class RemoveVisibilityScheduleView {
   static createRemoveVisibilitySchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'removeVisibilitySchedulePanel',
         title: Strings.panelTitles.removeVisibilitySchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'removeVisibilityScheduleExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'removeVisibilityScheduleSpecies',
               resultsId: 'removeVisibilityScheduleSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRemoveVisibilitySchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'removeVisibilityScheduleStatus',
            }),
         ],
      });
   }
}
