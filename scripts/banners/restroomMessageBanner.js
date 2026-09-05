import { MessageBanner } from './messageBanner.js';

export class RestroomMessageBanner {
   static createRestroomMessageBanner() {
      return MessageBanner.createSingleMessageBanner(
         restroom => restroom?.closed_message || restroom?.alert_message
      );
   }
}
