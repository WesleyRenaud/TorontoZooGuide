import { createSingleMessageBanner } from './messageBanner.js';

export function createRestroomMessageBanner() {
   return createSingleMessageBanner(
      restroom => restroom?.closed_message || restroom?.alert_message
   );
}
