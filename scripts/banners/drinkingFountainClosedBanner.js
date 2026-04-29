import { createSingleMessageBanner } from './messageBanner.js';

export function createDrinkingFountainClosedBanner() {
   return createSingleMessageBanner(
      drinkingFountain => drinkingFountain?.closed_message
   );
}
