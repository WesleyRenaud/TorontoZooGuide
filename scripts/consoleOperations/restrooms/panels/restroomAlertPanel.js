import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export class RestroomAlertPanel {
   static createRestroomAlertPanel() {
      return createPanelShell({
         panelId: 'restroomAlertPanel',
         title: APP_STRINGS.panelTitles.restroomAlert,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.restroom,
               inputId: 'restroomAlertRestroom',
               emptyOptionLabel: APP_STRINGS.placeholders.restroom,
            }),
            createDateRangeFields({
               startDateId: 'restroomAlertStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'restroomAlertEndDate',
               endHelpText: APP_STRINGS.help.keepAlertActiveUntilRemoved,
            }),
            createTextareaField({
               label: APP_STRINGS.labels.alertMessage,
               inputId: 'restroomAlertMessage',
               placeholder: APP_STRINGS.placeholders.restroomAlertExample,
            }),
            createActions({
               submitId: 'submitRestroomAlert',
            }),
            createStatus({
               statusId: 'restroomAlertStatus',
            }),
         ],
      });
   }
}
