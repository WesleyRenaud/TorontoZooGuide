import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRemoveViewingAlertPanel() {
   return createPanelShell({
      panelId: 'removeViewingAlertPanel',
      title: APP_STRINGS.panelTitles.removeViewingAlert,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.exhibit,
            inputId: 'removeViewingAlertExhibit',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createAutocompleteField({
            label: APP_STRINGS.labels.species,
            inputId: 'removeViewingAlertSpecies',
            resultsId: 'removeViewingAlertSpeciesResults',
            placeholder: APP_STRINGS.placeholders.speciesSearch,
         }),
         createActions({
            submitId: 'submitRemoveViewingAlert',
            submitLabel: APP_STRINGS.actions.removeAlert,
         }),
         createStatus({
            statusId: 'removeViewingAlertStatus',
         }),
      ],
   });
}
