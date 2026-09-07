import { DayPlannerPlanActionsHelpers } from './dayPlannerPlanActionsHelpers.js';
export class DayPlannerPlanActions {
   static hasScheduledItineraryItems(itinerary = {}) {
      return DayPlannerPlanActionsHelpers.collectionHasScheduledItems(itinerary.animals)
         || DayPlannerPlanActionsHelpers.collectionHasScheduledItems(itinerary.attractions)
         || DayPlannerPlanActionsHelpers.collectionHasScheduledItems(itinerary.guardiansTalks)
         || DayPlannerPlanActionsHelpers.collectionHasScheduledItems(itinerary.wildEncounters)
         || DayPlannerPlanActionsHelpers.collectionHasScheduledItems(itinerary.transportations)
         || DayPlannerPlanActionsHelpers.collectionHasScheduledItems(itinerary.events);
   }
}
