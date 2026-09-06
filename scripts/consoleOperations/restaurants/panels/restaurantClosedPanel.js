import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RestaurantClosedPanel {
   static createRestaurantClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'restaurantClosedPanel',
         title: Strings.panelTitles.restaurantClosed,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restaurant,
               inputId: 'restaurantClosedRestaurant',
               emptyOptionLabel: Strings.placeholders.restaurant,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'restaurantClosedStartDate',
               endDateId: 'restaurantClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened('restaurant'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'restaurantClosedMessage',
               placeholder: Strings.textareas.closedMessage('restaurant'),
            }),
            Fragments.createActions({
               submitId: 'submitRestaurantClosed',
            }),
            Fragments.createStatus({
               statusId: 'restaurantClosedStatus',
            }),
         ],
      });
   }
}
