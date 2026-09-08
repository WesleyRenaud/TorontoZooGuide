export class ItineraryPanelViewUrlHelper {
   static getDefaultLocation() {
      return globalThis.location ?? null;
   }

   static getDefaultHistory() {
      return globalThis.history ?? null;
   }
}
