import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createOnDisplayPanel() {
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
         createActions({
            submitId: 'submitOnDisplay',
         }),
         createStatus({
            statusId: 'onDisplayStatus',
         }),
      ],
   });
}
