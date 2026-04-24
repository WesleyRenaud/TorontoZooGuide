import { createSingleMessageBanner } from './messageBanner.js';

export function createRestaurantClosedBanner() {
   return createSingleMessageBanner(
      restaurant => restaurant?.closed_message
   );
}
