import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class AttractionClosedPanel {
   static createAttractionClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'attractionClosedPanel',
         title: Strings.panelTitles.attractionClosed,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionClosedAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'attractionClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionClosedEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'attractionClosedMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            Fragments.createActions({
               submitId: 'submitAttractionClosed',
            }),
            Fragments.createStatus({
               statusId: 'attractionClosedStatus',
            }),
         ],
      });
   }
}
