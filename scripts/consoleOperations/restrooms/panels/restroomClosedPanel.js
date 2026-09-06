import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RestroomClosedPanel {
   static createRestroomClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'restroomClosedPanel',
         title: Strings.panelTitles.restroomClosed,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'restroomClosedRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'restroomClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restroomClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened('restroom'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'restroomClosedMessage',
               placeholder: Strings.textareas.closedMessage('restroom'),
            }),
            Fragments.createActions({
               submitId: 'submitRestroomClosed',
            }),
            Fragments.createStatus({
               statusId: 'restroomClosedStatus',
            }),
         ],
      });
   }
}
