import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsoleCheckboxGridFieldBuilder } from '../../templates/consoleCheckboxGridFieldBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class OffDisplayForSeasonView {
   static createOffDisplayForSeasonPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'offDisplayForSeasonPanel',
         title: Strings.panelTitles.offDisplayForSeason,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'offDisplayForSeasonExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'offDisplayForSeasonSpecies',
               resultsId: 'offDisplayForSeasonSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleCheckboxGridFieldBuilder.createCheckboxGridField({
               label: Strings.labels.viewingScope,
               gridId: 'offDisplayForSeasonViewingScope',
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'offDisplayForSeasonStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'offDisplayForSeasonEndDate',
               endHelpText: Strings.help.keepOffDisplayUntilOnDisplay,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.reason,
               inputId: 'offDisplayForSeasonMessage',
               placeholder: Strings.textareas.offDisplayForSeasonReason,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitOffDisplayForSeason',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'offDisplayForSeasonStatus',
            }),
         ],
      });
   }
}
