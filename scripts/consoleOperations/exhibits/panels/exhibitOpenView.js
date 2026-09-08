import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class ExhibitOpenView {
   static createExhibitOpenPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'exhibitOpenPanel',
         title: Strings.panelTitles.exhibitOpen,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.exhibit,
               inputId: 'exhibitOpenExhibit',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'exhibitOpenStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'exhibitOpenEndDate',
               endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('exhibit'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitExhibitOpen',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'exhibitOpenStatus',
            }),
         ],
      });
   }
}
