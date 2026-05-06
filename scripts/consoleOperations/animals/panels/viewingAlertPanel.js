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

export function createViewingAlertPanel() {
   return createPanelShell({
      panelId: 'viewingAlertPanel',
      title: APP_STRINGS.panelTitles.viewingAlert,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.exhibit,
            inputId: 'viewingAlertExhibit',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createAutocompleteField({
            label: APP_STRINGS.labels.species,
            inputId: 'viewingAlertSpecies',
            resultsId: 'viewingAlertSpeciesResults',
            placeholder: APP_STRINGS.placeholders.speciesSearch,
         }),
         createDateRangeFields({
            startDateId: 'viewingAlertStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'viewingAlertEndDate',
            endHelpText: APP_STRINGS.help.keepAlertActiveUntilRemoved,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.alertMessage,
            inputId: 'viewingAlertMessage',
            placeholder: APP_STRINGS.textareas.viewingAlert,
         }),
         createActions({
            submitId: 'submitViewingAlert',
         }),
         createStatus({
            statusId: 'viewingAlertStatus',
         }),
      ],
   });
}
