import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createEditUpdatePanel() {
   return createPanelShell({
      panelId: 'editUpdatePanel',
      title: APP_STRINGS.panelTitles.editUpdate,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.update,
            inputId: 'editUpdateKey',
            emptyOptionLabel: APP_STRINGS.placeholders.update,
         }),
         createTextareaField({
            label: APP_STRINGS.labels.description,
            inputId: 'editUpdateDescription',
            placeholder: APP_STRINGS.textareas.currentDescription,
         }),
         createSelectField({
            label: APP_STRINGS.labels.type,
            inputId: 'editUpdateType',
            emptyOptionLabel: APP_STRINGS.placeholders.keepCurrentType,
            options: APP_STRINGS.updateTypes,
         }),
         createDateField({
            label: APP_STRINGS.labels.endDate,
            inputId: 'editUpdateEndDate',
            placeholder: APP_STRINGS.placeholders.newEndDate,
            helpText: APP_STRINGS.help.keepCurrentEndDate,
         }),
         createActions({
            submitId: 'submitEditUpdate',
         }),
         createStatus({
            statusId: 'editUpdateStatus',
         }),
      ],
   });
}
