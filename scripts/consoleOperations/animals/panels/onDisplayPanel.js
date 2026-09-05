import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export class OnDisplayPanel {
   static createOnDisplayPanel() {
      return createPanelShell({
         panelId: 'onDisplayPanel',
         title: APP_STRINGS.panelTitles.onDisplay,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.exhibit,
               inputId: 'onDisplayExhibit',
               emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
            }),
            createAutocompleteField({
               label: APP_STRINGS.labels.species,
               inputId: 'onDisplaySpecies',
               resultsId: 'onDisplaySpeciesResults',
               placeholder: APP_STRINGS.placeholders.speciesSearch,
            }),
            createSelectField({
               label: APP_STRINGS.labels.viewingScope,
               inputId: 'onDisplayViewingScope',
               emptyOptionLabel: APP_STRINGS.placeholders.viewingScope,
               options: APP_STRINGS.viewingScopes,
            }),
            createActions({
               submitId: 'submitOnDisplay',
            }),
            createStatus({
               statusId: 'onDisplayStatus',
            }),
         ],
      });
   }
}
