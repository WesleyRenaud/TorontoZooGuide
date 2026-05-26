import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createAutocompleteField,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createOffDisplayPanel() {
   return createPanelShell({
      panelId: 'offDisplayPanel',
      title: APP_STRINGS.panelTitles.offDisplay,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.exhibit,
            inputId: 'offDisplayExhibit',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createAutocompleteField({
            label: APP_STRINGS.labels.species,
            inputId: 'offDisplaySpecies',
            resultsId: 'offDisplaySpeciesResults',
            placeholder: APP_STRINGS.placeholders.speciesSearch,
         }),
         createSelectField({
            label: APP_STRINGS.labels.viewingScope,
            inputId: 'offDisplayViewingScope',
            emptyOptionLabel: APP_STRINGS.placeholders.viewingScope,
            options: APP_STRINGS.viewingScopes,
         }),
         createDateRangeFields({
            startDateId: 'offDisplayStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'offDisplayEndDate',
            endHelpText: APP_STRINGS.help.keepOffDisplayUntilOnDisplay,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.reason,
            inputId: 'offDisplayMessage',
            placeholder: APP_STRINGS.textareas.offDisplayReason,
         }),
         createActions({
            submitId: 'submitOffDisplay',
         }),
         createStatus({
            statusId: 'offDisplayStatus',
         }),
      ],
   });
}
