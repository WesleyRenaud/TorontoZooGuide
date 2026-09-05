import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export class RemoveVisibilitySchedulePanel {
   static createRemoveVisibilitySchedulePanel() {
      return createPanelShell({
         panelId: 'removeVisibilitySchedulePanel',
         title: APP_STRINGS.panelTitles.removeVisibilitySchedule,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.exhibit,
               inputId: 'removeVisibilityScheduleExhibit',
               emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
            }),
            createAutocompleteField({
               label: APP_STRINGS.labels.species,
               inputId: 'removeVisibilityScheduleSpecies',
               resultsId: 'removeVisibilityScheduleSpeciesResults',
               placeholder: APP_STRINGS.placeholders.speciesSearch,
            }),
            createActions({
               submitId: 'submitRemoveVisibilitySchedule',
            }),
            createStatus({
               statusId: 'removeVisibilityScheduleStatus',
            }),
         ],
      });
   }
}
