import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RemoveVisibilitySchedulePanel {
   static createRemoveVisibilitySchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'removeVisibilitySchedulePanel',
         title: Strings.panelTitles.removeVisibilitySchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'removeVisibilityScheduleExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createAutocompleteField({
               label: Strings.labels.species,
               inputId: 'removeVisibilityScheduleSpecies',
               resultsId: 'removeVisibilityScheduleSpeciesResults',
               placeholder: Strings.placeholders.speciesSearch,
            }),
            Fragments.createActions({
               submitId: 'submitRemoveVisibilitySchedule',
            }),
            Fragments.createStatus({
               statusId: 'removeVisibilityScheduleStatus',
            }),
         ],
      });
   }
}
