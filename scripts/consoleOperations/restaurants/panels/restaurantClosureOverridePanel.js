import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export class RestaurantClosureOverridePanel {
   static createRestaurantClosureOverridePanel() {
      return createPanelShell({
         panelId: 'restaurantClosureOverridePanel',
         title: APP_STRINGS.panelTitles.restaurantClosureOverride,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.restaurant,
               inputId: 'restaurantClosureOverrideRestaurant',
               emptyOptionLabel: APP_STRINGS.placeholders.restaurant,
            }),
            createDateRangeFields({
               startDateId: 'restaurantClosureOverrideStartDate',
               startHelpText: APP_STRINGS.help.startImmediately,
               endDateId: 'restaurantClosureOverrideEndDate',
               endHelpText: APP_STRINGS.help.continueUntilReopened('restaurant'),
            }),
            createTextareaField({
               label: APP_STRINGS.labels.closedMessage,
               inputId: 'restaurantClosureOverrideMessage',
               placeholder: APP_STRINGS.textareas.closedMessage('restaurant'),
            }),
            createActions({
               submitId: 'submitRestaurantClosureOverride',
            }),
            createStatus({
               statusId: 'restaurantClosureOverrideStatus',
            }),
         ],
      });
   }
}
