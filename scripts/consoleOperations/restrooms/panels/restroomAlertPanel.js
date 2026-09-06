import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RestroomAlertPanel {
   static createRestroomAlertPanel() {
      return Fragments.createPanelShell({
         panelId: 'restroomAlertPanel',
         title: Strings.panelTitles.restroomAlert,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'restroomAlertRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'restroomAlertStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restroomAlertEndDate',
               endHelpText: Strings.help.keepAlertActiveUntilRemoved,
            }),
            Fragments.createTextareaField({
               label: Strings.labels.alertMessage,
               inputId: 'restroomAlertMessage',
               placeholder: Strings.placeholders.restroomAlertExample,
            }),
            Fragments.createActions({
               submitId: 'submitRestroomAlert',
            }),
            Fragments.createStatus({
               statusId: 'restroomAlertStatus',
            }),
         ],
      });
   }
}
