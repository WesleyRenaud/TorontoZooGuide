import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class DrinkingFountainsClosedPanel {
   static createDrinkingFountainsClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'drinkingFountainsClosedPanel',
         title: Strings.panelTitles.drinkingFountainsClosed,
         bodyChildren: [
            Fragments.createDateRangeFields({
               startDateId: 'drinkingFountainsClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'drinkingFountainsClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened(
                  'drinking fountains'
               ),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'drinkingFountainsClosedMessage',
               placeholder: Strings.textareas.drinkingFountainsClosedMessage,
            }),
            Fragments.createActions({
               submitId: 'submitDrinkingFountainsClosed',
            }),
            Fragments.createStatus({
               statusId: 'drinkingFountainsClosedStatus',
            }),
         ],
      });
   }
}
