import { ItineraryClient } from '../api/itineraryClient.js';
import { DraftStore } from './draftStore.js';

export class ItineraryServiceHelper {
   static async fetchSavedItineraryVisitDate() {
      const { date } = await ItineraryClient.getItineraryDateRequest();

      if (date) {
         DraftStore.setStoredItineraryDate(date);
      }

      return date;
   }
}
