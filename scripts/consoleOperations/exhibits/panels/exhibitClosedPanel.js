import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class ExhibitClosedPanel {
   static createExhibitClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'exhibitClosedPanel',
         title: Strings.panelTitles.exhibitClosed,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'exhibitClosedExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'exhibitClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'exhibitClosedEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('exhibit'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'exhibitClosedMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            Fragments.createActions({
               submitId: 'submitExhibitClosed',
            }),
            Fragments.createStatus({
               statusId: 'exhibitClosedStatus',
            }),
         ],
      });
   }
}
