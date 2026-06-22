export function createItineraryConfirmationCancelledResult(result = {}) {
   return {
      ...result,
      cancelled: true,
   };
}

export function isItineraryConfirmationCancelled(result) {
   return Boolean(result?.cancelled);
}
