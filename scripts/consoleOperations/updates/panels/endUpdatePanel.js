import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createEndUpdatePanel() {
   return createPanelShell({
      panelId: 'endUpdatePanel',
      title: APP_STRINGS.panelTitles.endUpdate,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.labels.update,
            inputId: 'endUpdateKey',
            emptyOptionLabel: APP_STRINGS.placeholders.update,
         }),
         createDateField({
            label: APP_STRINGS.labels.endDate,
            inputId: 'endUpdateEndDate',
            placeholder: APP_STRINGS.placeholders.endDate,
            helpText: APP_STRINGS.help.endUpdateToday,
         }),
         createActions({
            submitId: 'submitEndUpdate',
         }),
         createStatus({
            statusId: 'endUpdateStatus',
         }),
      ],
   });
}
