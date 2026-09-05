import { MessageBanner } from './messageBanner.js';

export class DrinkingFountainClosedBanner {
   static createDrinkingFountainClosedBanner() {
      return MessageBanner.createSingleMessageBanner(
         drinkingFountain => drinkingFountain?.closed_message
      );
   }
}
