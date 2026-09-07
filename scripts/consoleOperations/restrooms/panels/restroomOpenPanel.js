import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class RestroomOpenPanel {
   static createRestroomOpenPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'restroomOpenPanel',
         title: Strings.panelTitles.restroomOpen,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restroom,
               inputId: 'restroomOpenRestroom',
               emptyOptionLabel: Strings.placeholders.restroom,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'restroomOpenStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restroomOpenEndDate',
               endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('restroom'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRestroomOpen',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'restroomOpenStatus',
            }),
         ],
      });
   }
}
