import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RemoveViewingAlertPanel {
   static createRemoveViewingAlertPanel() {
      return Fragments.createPanelShell({
         panelId: 'removeViewingAlertPanel',
         title: Strings.panelTitles.removeViewingAlert,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'removeViewingAlertExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'removeViewingAlertSpecies',
               resultsId: 'removeViewingAlertSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            Fragments.createActions({
               submitId: 'submitRemoveViewingAlert',
               submitLabel: Strings.actions.removeAlert,
            }),
            Fragments.createStatus({
               statusId: 'removeViewingAlertStatus',
            }),
         ],
      });
   }
}
