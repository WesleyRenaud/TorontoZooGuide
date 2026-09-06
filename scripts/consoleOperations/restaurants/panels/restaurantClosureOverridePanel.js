import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class RestaurantClosureOverridePanel {
   static createRestaurantClosureOverridePanel() {
      return Fragments.createPanelShell({
         panelId: 'restaurantClosureOverridePanel',
         title: Strings.panelTitles.restaurantClosureOverride,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.restaurant,
               inputId: 'restaurantClosureOverrideRestaurant',
               emptyOptionLabel: Strings.placeholders.restaurant,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'restaurantClosureOverrideStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'restaurantClosureOverrideEndDate',
               endHelpText: Strings.help.continueUntilReopened('restaurant'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'restaurantClosureOverrideMessage',
               placeholder: Strings.textareas.closedMessage('restaurant'),
            }),
            Fragments.createActions({
               submitId: 'submitRestaurantClosureOverride',
            }),
            Fragments.createStatus({
               statusId: 'restaurantClosureOverrideStatus',
            }),
         ],
      });
   }
}
