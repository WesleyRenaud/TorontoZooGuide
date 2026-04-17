import { createMessageBanner } from './messageBanner.js';

export function createGiftShopClosedBanner() {
   return createMessageBanner({
      getMessages: giftShop => giftShop?.closed_message ? [giftShop.closed_message] : [],
   });
}
