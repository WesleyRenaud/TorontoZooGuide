import { ItineraryClient } from '../api/itineraryClient.js';
import { ItineraryServiceTimeRunner } from './itineraryServiceTimeRunner.js';

export class ItineraryServiceFormatter {
   static async setItineraryArrivalTime(arrivalTime) {
      return ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(
         ItineraryClient.setItineraryArrivalTimeRequest,
         arrivalTime
      );
   }

   static async setItineraryDepartureTime(departureTime) {
      return ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(
         ItineraryClient.setItineraryDepartureTimeRequest,
         departureTime
      );
   }
}
