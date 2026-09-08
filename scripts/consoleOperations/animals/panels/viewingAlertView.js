import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../templates/consoleAutocompleteFieldBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class ViewingAlertView {
   static createViewingAlertPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'viewingAlertPanel',
         title: Strings.panelTitles.viewingAlert,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'viewingAlertExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleAutocompleteFieldBuilder.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'viewingAlertSpecies',
               resultsId: 'viewingAlertSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'viewingAlertStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'viewingAlertEndDate',
               endHelpText: Strings.help.keepAlertActiveUntilRemoved,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.alertMessage,
               inputId: 'viewingAlertMessage',
               placeholder: Strings.textareas.viewingAlert,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitViewingAlert',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'viewingAlertStatus',
            }),
         ],
      });
   }
}
