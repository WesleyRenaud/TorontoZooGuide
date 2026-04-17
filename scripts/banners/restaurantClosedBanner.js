import { createMessageBanner } from './messageBanner.js';

export function createRestaurantClosedBanner() {
   return createMessageBanner({
      getMessages: restaurant => restaurant?.closed_message ? [restaurant.closed_message] : [],
   });
}
