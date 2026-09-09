import { GlobalAmenityStatusPanelBuilder } from '../../forms/globalAmenityStatusPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsClosedView {
   static createDrinkingFountainsClosedPanel() {
      return GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsClosedPanel',
         title: Strings.panelTitles.drinkingFountainsClosed,
         idPrefix: 'drinkingFountainsClosed',
         endHelpText: Strings.help.continueUntilReopened('drinking fountains'),
         includeMessage: true,
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.drinkingFountainsClosedMessage,
         submitId: 'submitDrinkingFountainsClosed',
         statusId: 'drinkingFountainsClosedStatus',
      });
   }
}
