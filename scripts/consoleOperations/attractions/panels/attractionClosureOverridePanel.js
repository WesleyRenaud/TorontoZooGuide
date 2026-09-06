import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class AttractionClosureOverridePanel {
   static createAttractionClosureOverridePanel() {
      return Fragments.createPanelShell({
         panelId: 'attractionClosureOverridePanel',
         title: Strings.panelTitles.attractionClosureOverride,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionClosureOverrideAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'attractionClosureOverrideStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionClosureOverrideEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'attractionClosureOverrideMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            Fragments.createActions({
               submitId: 'submitAttractionClosureOverride',
            }),
            Fragments.createStatus({
               statusId: 'attractionClosureOverrideStatus',
            }),
         ],
      });
   }
}
