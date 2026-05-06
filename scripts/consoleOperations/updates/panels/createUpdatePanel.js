import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
   createTextInputField,
} from '../../templates/fragments.js';

export function createCreateUpdatePanel() {
   return createPanelShell({
      panelId: 'createUpdatePanel',
      title: APP_STRINGS.panelTitles.createUpdate,
      bodyChildren: [
         createTextInputField({
            label: APP_STRINGS.labels.title,
            inputId: 'createUpdateTitle',
            placeholder: APP_STRINGS.textareas.updateTitleExample,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.description,
            inputId: 'createUpdateDescription',
            placeholder: APP_STRINGS.textareas.updateDescription,
         }),
         createSelectField({
            label: APP_STRINGS.labels.type,
            inputId: 'createUpdateType',
            emptyOptionLabel: APP_STRINGS.placeholders.type,
            options: APP_STRINGS.updateTypes,
         }),
         createDateRangeFields({
            startDateId: 'createUpdateStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'createUpdateEndDate',
            endHelpText: APP_STRINGS.help.keepUpdateActiveWithoutEndDate,
         }),
         createActions({
            submitId: 'submitCreateUpdate',
         }),
         createStatus({
            statusId: 'createUpdateStatus',
         }),
      ],
   });
}
