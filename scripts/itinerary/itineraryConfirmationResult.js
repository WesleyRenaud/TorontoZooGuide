export class ItineraryConfirmationResult {
   static createItineraryConfirmationCancelledResult(result = {}) {
      return {
         ...result,
         cancelled: true,
      };
   }

   static isItineraryConfirmationCancelled(result) {
      return Boolean(result?.cancelled);
   }
}
