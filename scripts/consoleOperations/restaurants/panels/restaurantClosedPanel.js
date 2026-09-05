import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export class RestaurantClosedPanel {
   static createRestaurantClosedPanel() {
      return createPanelShell({
         panelId: 'restaurantClosedPanel',
         title: APP_STRINGS.panelTitles.restaurantClosed,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.restaurant,
               inputId: 'restaurantClosedRestaurant',
               emptyOptionLabel: APP_STRINGS.placeholders.restaurant,
            }),
            createDateRangeFields({
               startDateId: 'restaurantClosedStartDate',
               endDateId: 'restaurantClosedEndDate',
               endHelpText: APP_STRINGS.help.continueUntilReopened('restaurant'),
            }),
            createTextareaField({
               label: APP_STRINGS.labels.closedMessage,
               inputId: 'restaurantClosedMessage',
               placeholder: APP_STRINGS.textareas.closedMessage('restaurant'),
            }),
            createActions({
               submitId: 'submitRestaurantClosed',
            }),
            createStatus({
               statusId: 'restaurantClosedStatus',
            }),
         ],
      });
   }
}
