import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class OnDisplayPanel {
   static createOnDisplayPanel() {
      return Fragments.createPanelShell({
         panelId: 'onDisplayPanel',
         title: Strings.panelTitles.onDisplay,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'onDisplayExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'onDisplaySpecies',
               resultsId: 'onDisplaySpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            Fragments.createSelectField({
               label: Strings.labels.viewingScope,
               inputId: 'onDisplayViewingScope',
               emptyOptionLabel: Strings.placeholders.viewingScope,
               options: Strings.viewingScopes,
            }),
            Fragments.createActions({
               submitId: 'submitOnDisplay',
            }),
            Fragments.createStatus({
               statusId: 'onDisplayStatus',
            }),
         ],
      });
   }
}
