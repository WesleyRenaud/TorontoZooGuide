import { OffDisplayView } from '../animals/panels/offDisplayView.js';
import { OnDisplayView } from '../animals/panels/onDisplayView.js';
import { RemoveViewingAlertView } from '../animals/panels/removeViewingAlertView.js';
import { RemoveVisibilityScheduleView } from '../animals/panels/removeVisibilityScheduleView.js';
import { ViewingAlertView } from '../animals/panels/viewingAlertView.js';
import { VisibilityScheduleView } from '../animals/panels/visibilityScheduleView.js';
import { AttractionClosedView } from '../attractions/panels/attractionClosedView.js';
import { AttractionClosureOverrideView } from '../attractions/panels/attractionClosureOverrideView.js';
import { AttractionHoursScheduleView } from '../attractions/panels/attractionHoursScheduleView.js';
import { AttractionOpeningScheduleView } from '../attractions/panels/attractionOpeningScheduleView.js';
import { DrinkingFountainsClosedView } from '../drinkingFountains/panels/drinkingFountainsClosedView.js';
import { DrinkingFountainsOpenView } from '../drinkingFountains/panels/drinkingFountainsOpenView.js';
import { CreateEventView } from '../events/panels/createEventView.js';
import { ExhibitClosedView } from '../exhibits/panels/exhibitClosedView.js';
import { ExhibitOpenView } from '../exhibits/panels/exhibitOpenView.js';
import { GiftShopClosedView } from '../giftShops/panels/giftShopClosedView.js';
import { GiftShopClosureOverrideView } from '../giftShops/panels/giftShopClosureOverrideView.js';
import { GiftShopOpeningScheduleView } from '../giftShops/panels/giftShopOpeningScheduleView.js';
import { AddGuardiansTalkOccurrenceView } from '../guardiansTalks/panels/addGuardiansTalkOccurrenceView.js';
import { CancelGuardiansTalkOccurrenceView } from '../guardiansTalks/panels/cancelGuardiansTalkOccurrenceView.js';
import { EndGuardiansTalkScheduleView } from '../guardiansTalks/panels/endGuardiansTalkScheduleView.js';
import { GuardiansTalkScheduleView } from '../guardiansTalks/panels/guardiansTalkScheduleView.js';
import { RestaurantClosedView } from '../restaurants/panels/restaurantClosedView.js';
import { RestaurantClosureOverrideView } from '../restaurants/panels/restaurantClosureOverrideView.js';
import { RestaurantOpeningScheduleView } from '../restaurants/panels/restaurantOpeningScheduleView.js';
import { RemoveRestroomAlertView } from '../restrooms/panels/removeRestroomAlertView.js';
import { RestroomAlertView } from '../restrooms/panels/restroomAlertView.js';
import { RestroomClosedView } from '../restrooms/panels/restroomClosedView.js';
import { RestroomOpenView } from '../restrooms/panels/restroomOpenView.js';
import { TransportationRouteView } from '../transportation/panels/transportationRouteView.js';
import { TransportationStationClosedView } from '../transportation/panels/transportationStationClosedView.js';
import { TransportationStationOpenView } from '../transportation/panels/transportationStationOpenView.js';
import { CreateUpdateView } from '../updates/panels/createUpdateView.js';
import { EditUpdateView } from '../updates/panels/editUpdateView.js';
import { EndUpdateView } from '../updates/panels/endUpdateView.js';
import { CancelWildEncounterOccurrenceView } from '../wildEncounters/panels/cancelWildEncounterOccurrenceView.js';
import { EndWildEncounterScheduleView } from '../wildEncounters/panels/endWildEncounterScheduleView.js';
import { WildEncounterScheduleView } from '../wildEncounters/panels/wildEncounterScheduleView.js';

export class ConsoleOperationPanelsBootstrapHelper {
   static PANEL_CREATORS = {
   animals: [
      OffDisplayView.createOffDisplayPanel,
      OnDisplayView.createOnDisplayPanel,
      VisibilityScheduleView.createVisibilitySchedulePanel,
      RemoveVisibilityScheduleView.createRemoveVisibilitySchedulePanel,
      ViewingAlertView.createViewingAlertPanel,
      RemoveViewingAlertView.createRemoveViewingAlertPanel,
   ],
   exhibits: [
      ExhibitClosedView.createExhibitClosedPanel,
      ExhibitOpenView.createExhibitOpenPanel,
   ],
   restaurants: [
      RestaurantClosedView.createRestaurantClosedPanel,
      RestaurantClosureOverrideView.createRestaurantClosureOverridePanel,
      RestaurantOpeningScheduleView.createRestaurantOpeningSchedulePanel,
   ],
   restrooms: [
      RestroomClosedView.createRestroomClosedPanel,
      RestroomOpenView.createRestroomOpenPanel,
      RestroomAlertView.createRestroomAlertPanel,
      RemoveRestroomAlertView.createRemoveRestroomAlertPanel,
   ],
   giftShops: [
      GiftShopClosedView.createGiftShopClosedPanel,
      GiftShopClosureOverrideView.createGiftShopClosureOverridePanel,
      GiftShopOpeningScheduleView.createGiftShopOpeningSchedulePanel,
   ],
   attractions: [
      AttractionClosedView.createAttractionClosedPanel,
      AttractionClosureOverrideView.createAttractionClosureOverridePanel,
      AttractionOpeningScheduleView.createAttractionOpeningSchedulePanel,
      AttractionHoursScheduleView.createAttractionHoursSchedulePanel,
   ],
   transportation: [
      TransportationStationClosedView.createTransportationStationClosedPanel,
      TransportationStationOpenView.createTransportationStationOpenPanel,
      TransportationRouteView.createTransportationRoutePanel,
   ],
   guardiansTalks: [
      GuardiansTalkScheduleView.createGuardiansTalkSchedulePanel,
      EndGuardiansTalkScheduleView.createEndGuardiansTalkSchedulePanel,
      AddGuardiansTalkOccurrenceView.createAddGuardiansTalkOccurrencePanel,
      CancelGuardiansTalkOccurrenceView.createCancelGuardiansTalkOccurrencePanel,
   ],
   wildEncounters: [
      WildEncounterScheduleView.createWildEncounterSchedulePanel,
      EndWildEncounterScheduleView.createEndWildEncounterSchedulePanel,
      CancelWildEncounterOccurrenceView.createCancelWildEncounterOccurrencePanel,
   ],
   drinkingFountains: [
      DrinkingFountainsClosedView.createDrinkingFountainsClosedPanel,
      DrinkingFountainsOpenView.createDrinkingFountainsOpenPanel,
   ],
   events: [
      CreateEventView.createCreateEventPanel,
   ],
   updates: [
      CreateUpdateView.createCreateUpdatePanel,
      EndUpdateView.createEndUpdatePanel,
      EditUpdateView.createEditUpdatePanel,
   ],
};

   static getPanelCreators() {
      return Object.values(ConsoleOperationPanelsBootstrapHelper.PANEL_CREATORS).flat();
   }

   static createConsoleOperationPanelsFragment(doc = document) {
      const fragment = doc.createDocumentFragment();

      ConsoleOperationPanelsBootstrapHelper.getPanelCreators().forEach((createPanel) => {
         const panelEl = createPanel();
         fragment.appendChild(
            panelEl.ownerDocument === doc
               ? panelEl
               : doc.importNode(panelEl, true)
         );
      });

      return fragment;
   }
}
