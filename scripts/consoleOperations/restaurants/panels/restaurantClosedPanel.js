import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class RestaurantClosedPanel {
   static createRestaurantClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'restaurantClosedPanel',
         title: Strings.panelTitles.restaurantClosed,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.restaurant,
               inputId: 'restaurantClosedRestaurant',
               emptyOptionLabel: Strings.placeholders.restaurant,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'restaurantClosedStartDate',
               endDateId: 'restaurantClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened('restaurant'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'restaurantClosedMessage',
               placeholder: Strings.textareas.closedMessage('restaurant'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitRestaurantClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'restaurantClosedStatus',
            }),
         ],
      });
   }
}
