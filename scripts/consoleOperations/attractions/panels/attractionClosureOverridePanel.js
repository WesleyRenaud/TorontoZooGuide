import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export class AttractionClosureOverridePanel {
   static createAttractionClosureOverridePanel() {
      return createPanelShell({
         panelId: 'attractionClosureOverridePanel',
         title: APP_STRINGS.panelTitles.attractionClosureOverride,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.attraction,
               inputId: 'attractionClosureOverrideAttraction',
               emptyOptionLabel: APP_STRINGS.placeholders.attraction,
            }),
            createDateRangeFields({
               startDateId: 'attractionClosureOverrideStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'attractionClosureOverrideEndDate',
               endHelpText: APP_STRINGS.help.keepClosedUntilManuallyReopened('attraction'),
            }),
            createTextareaField({
               label: APP_STRINGS.labels.closureMessage,
               inputId: 'attractionClosureOverrideMessage',
               placeholder: APP_STRINGS.textareas.closureMessage,
            }),
            createActions({
               submitId: 'submitAttractionClosureOverride',
            }),
            createStatus({
               statusId: 'attractionClosureOverrideStatus',
            }),
         ],
      });
   }
}
