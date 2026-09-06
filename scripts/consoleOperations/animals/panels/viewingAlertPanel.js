import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class ViewingAlertPanel {
   static createViewingAlertPanel() {
      return Fragments.createPanelShell({
         panelId: 'viewingAlertPanel',
         title: Strings.panelTitles.viewingAlert,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'viewingAlertExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'viewingAlertSpecies',
               resultsId: 'viewingAlertSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'viewingAlertStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'viewingAlertEndDate',
               endHelpText: Strings.help.keepAlertActiveUntilRemoved,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.alertMessage,
               inputId: 'viewingAlertMessage',
               placeholder: Strings.textareas.viewingAlert,
            }),
            Fragments.createActions({
               submitId: 'submitViewingAlert',
            }),
            Fragments.createStatus({
               statusId: 'viewingAlertStatus',
            }),
         ],
      });
   }
}
