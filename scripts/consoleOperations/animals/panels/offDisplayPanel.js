import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class OffDisplayPanel {
   static createOffDisplayPanel() {
      return Fragments.createPanelShell({
         panelId: 'offDisplayPanel',
         title: Strings.panelTitles.offDisplay,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'offDisplayExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'offDisplaySpecies',
               resultsId: 'offDisplaySpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            Fragments.createSelectField({
               label: Strings.labels.viewingScope,
               inputId: 'offDisplayViewingScope',
               emptyOptionLabel: Strings.placeholders.viewingScope,
               options: Strings.viewingScopes,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'offDisplayStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'offDisplayEndDate',
               endHelpText: Strings.help.keepOffDisplayUntilOnDisplay,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.reason,
               inputId: 'offDisplayMessage',
               placeholder: Strings.textareas.offDisplayReason,
            }),
            Fragments.createActions({
               submitId: 'submitOffDisplay',
            }),
            Fragments.createStatus({
               statusId: 'offDisplayStatus',
            }),
         ],
      });
   }
}
