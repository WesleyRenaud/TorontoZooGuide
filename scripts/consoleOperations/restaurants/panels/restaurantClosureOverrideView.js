import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class RestaurantClosureOverrideView {
   static createRestaurantClosureOverridePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'restaurantClosureOverridePanel',
         title: Strings.panelTitles.restaurantClosureOverride,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restaurant,
               inputId: 'restaurantClosureOverrideRestaurant',
               emptyOptionLabel: Strings.placeholders.restaurant,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'restaurantClosureOverrideStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restaurantClosureOverrideEndDate',
               endHelpText: Strings.help.continueUntilReopened('restaurant'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'restaurantClosureOverrideMessage',
               placeholder: Strings.textareas.closedMessage('restaurant'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRestaurantClosureOverride',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'restaurantClosureOverrideStatus',
            }),
         ],
      });
   }
}
