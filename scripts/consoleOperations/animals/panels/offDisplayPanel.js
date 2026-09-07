import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class OffDisplayPanel {
   static createOffDisplayPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'offDisplayPanel',
         title: Strings.panelTitles.offDisplay,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'offDisplayExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'offDisplaySpecies',
               resultsId: 'offDisplaySpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.viewingScope,
               inputId: 'offDisplayViewingScope',
               emptyOptionLabel: Strings.placeholders.viewingScope,
               options: Strings.viewingScopes,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'offDisplayStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'offDisplayEndDate',
               endHelpText: Strings.help.keepOffDisplayUntilOnDisplay,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.reason,
               inputId: 'offDisplayMessage',
               placeholder: Strings.textareas.offDisplayReason,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitOffDisplay',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'offDisplayStatus',
            }),
         ],
      });
   }
}
