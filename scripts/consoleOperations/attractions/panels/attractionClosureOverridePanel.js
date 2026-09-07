import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class AttractionClosureOverridePanel {
   static createAttractionClosureOverridePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'attractionClosureOverridePanel',
         title: Strings.panelTitles.attractionClosureOverride,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.attraction,
               inputId: 'attractionClosureOverrideAttraction',
               emptyOptionLabel: Strings.placeholders.attraction,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'attractionClosureOverrideStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'attractionClosureOverrideEndDate',
               endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closureMessage,
               inputId: 'attractionClosureOverrideMessage',
               placeholder: Strings.textareas.closureMessage,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitAttractionClosureOverride',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'attractionClosureOverrideStatus',
            }),
         ],
      });
   }
}
