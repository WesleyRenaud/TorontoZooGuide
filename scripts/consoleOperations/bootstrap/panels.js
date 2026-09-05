import { OffDisplayPanel } from '../animals/panels/offDisplayPanel.js';
import { OnDisplayPanel } from '../animals/panels/onDisplayPanel.js';
import { RemoveViewingAlertPanel } from '../animals/panels/removeViewingAlertPanel.js';
import { RemoveVisibilitySchedulePanel } from '../animals/panels/removeVisibilitySchedulePanel.js';
import { ViewingAlertPanel } from '../animals/panels/viewingAlertPanel.js';
import { VisibilitySchedulePanel } from '../animals/panels/visibilitySchedulePanel.js';
import { AttractionClosedPanel } from '../attractions/panels/attractionClosedPanel.js';
import { AttractionClosureOverridePanel } from '../attractions/panels/attractionClosureOverridePanel.js';
import { AttractionHoursSchedulePanel } from '../attractions/panels/attractionHoursSchedulePanel.js';
import { AttractionOpeningSchedulePanel } from '../attractions/panels/attractionOpeningSchedulePanel.js';
import { DrinkingFountainsClosedPanel } from '../drinkingFountains/panels/drinkingFountainsClosedPanel.js';
import { DrinkingFountainsOpenPanel } from '../drinkingFountains/panels/drinkingFountainsOpenPanel.js';
import { CreateEventPanel } from '../events/panels/createEventPanel.js';
import { ExhibitClosedPanel } from '../exhibits/panels/exhibitClosedPanel.js';
import { ExhibitOpenPanel } from '../exhibits/panels/exhibitOpenPanel.js';
import { GiftShopClosedPanel } from '../giftShops/panels/giftShopClosedPanel.js';
import { GiftShopClosureOverridePanel } from '../giftShops/panels/giftShopClosureOverridePanel.js';
import { GiftShopOpeningSchedulePanel } from '../giftShops/panels/giftShopOpeningSchedulePanel.js';
import { AddGuardiansTalkOccurrencePanel } from '../guardiansTalks/panels/addGuardiansTalkOccurrencePanel.js';
import { CancelGuardiansTalkOccurrencePanel } from '../guardiansTalks/panels/cancelGuardiansTalkOccurrencePanel.js';
import { EndGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/endGuardiansTalkSchedulePanel.js';
import { GuardiansTalkSchedulePanel } from '../guardiansTalks/panels/guardiansTalkSchedulePanel.js';
import { RestaurantClosedPanel } from '../restaurants/panels/restaurantClosedPanel.js';
import { RestaurantClosureOverridePanel } from '../restaurants/panels/restaurantClosureOverridePanel.js';
import { RestaurantOpeningSchedulePanel } from '../restaurants/panels/restaurantOpeningSchedulePanel.js';
import { RemoveRestroomAlertPanel } from '../restrooms/panels/removeRestroomAlertPanel.js';
import { RestroomAlertPanel } from '../restrooms/panels/restroomAlertPanel.js';
import { RestroomClosedPanel } from '../restrooms/panels/restroomClosedPanel.js';
import { RestroomOpenPanel } from '../restrooms/panels/restroomOpenPanel.js';
import { TransportationRoutePanel } from '../transportation/panels/transportationRoutePanel.js';
import { TransportationStationClosedPanel } from '../transportation/panels/transportationStationClosedPanel.js';
import { TransportationStationOpenPanel } from '../transportation/panels/transportationStationOpenPanel.js';
import { CreateUpdatePanel } from '../updates/panels/createUpdatePanel.js';
import { EditUpdatePanel } from '../updates/panels/editUpdatePanel.js';
import { EndUpdatePanel } from '../updates/panels/endUpdatePanel.js';
import { CancelWildEncounterOccurrencePanel } from '../wildEncounters/panels/cancelWildEncounterOccurrencePanel.js';
import { EndWildEncounterSchedulePanel } from '../wildEncounters/panels/endWildEncounterSchedulePanel.js';
import { WildEncounterSchedulePanel } from '../wildEncounters/panels/wildEncounterSchedulePanel.js';

const PANEL_CREATORS = {
   animals: [
      OffDisplayPanel.createOffDisplayPanel,
      OnDisplayPanel.createOnDisplayPanel,
      VisibilitySchedulePanel.createVisibilitySchedulePanel,
      RemoveVisibilitySchedulePanel.createRemoveVisibilitySchedulePanel,
      ViewingAlertPanel.createViewingAlertPanel,
      RemoveViewingAlertPanel.createRemoveViewingAlertPanel,
   ],
   exhibits: [
      ExhibitClosedPanel.createExhibitClosedPanel,
      ExhibitOpenPanel.createExhibitOpenPanel,
   ],
   restaurants: [
      RestaurantClosedPanel.createRestaurantClosedPanel,
      RestaurantClosureOverridePanel.createRestaurantClosureOverridePanel,
      RestaurantOpeningSchedulePanel.createRestaurantOpeningSchedulePanel,
   ],
   restrooms: [
      RestroomClosedPanel.createRestroomClosedPanel,
      RestroomOpenPanel.createRestroomOpenPanel,
      RestroomAlertPanel.createRestroomAlertPanel,
      RemoveRestroomAlertPanel.createRemoveRestroomAlertPanel,
   ],
   giftShops: [
      GiftShopClosedPanel.createGiftShopClosedPanel,
      GiftShopClosureOverridePanel.createGiftShopClosureOverridePanel,
      GiftShopOpeningSchedulePanel.createGiftShopOpeningSchedulePanel,
   ],
   attractions: [
      AttractionClosedPanel.createAttractionClosedPanel,
      AttractionClosureOverridePanel.createAttractionClosureOverridePanel,
      AttractionOpeningSchedulePanel.createAttractionOpeningSchedulePanel,
      AttractionHoursSchedulePanel.createAttractionHoursSchedulePanel,
   ],
   transportation: [
      TransportationStationClosedPanel.createTransportationStationClosedPanel,
      TransportationStationOpenPanel.createTransportationStationOpenPanel,
      TransportationRoutePanel.createTransportationRoutePanel,
   ],
   guardiansTalks: [
      GuardiansTalkSchedulePanel.createGuardiansTalkSchedulePanel,
      EndGuardiansTalkSchedulePanel.createEndGuardiansTalkSchedulePanel,
      AddGuardiansTalkOccurrencePanel.createAddGuardiansTalkOccurrencePanel,
      CancelGuardiansTalkOccurrencePanel.createCancelGuardiansTalkOccurrencePanel,
   ],
   wildEncounters: [
      WildEncounterSchedulePanel.createWildEncounterSchedulePanel,
      EndWildEncounterSchedulePanel.createEndWildEncounterSchedulePanel,
      CancelWildEncounterOccurrencePanel.createCancelWildEncounterOccurrencePanel,
   ],
   drinkingFountains: [
      DrinkingFountainsClosedPanel.createDrinkingFountainsClosedPanel,
      DrinkingFountainsOpenPanel.createDrinkingFountainsOpenPanel,
   ],
   events: [
      CreateEventPanel.createCreateEventPanel,
   ],
   updates: [
      CreateUpdatePanel.createCreateUpdatePanel,
      EndUpdatePanel.createEndUpdatePanel,
      EditUpdatePanel.createEditUpdatePanel,
   ],
};

function getPanelCreators() {
   return Object.values(PANEL_CREATORS).flat();
}

function createConsoleOperationPanelsFragment(doc = document) {
   const fragment = doc.createDocumentFragment();

   getPanelCreators().forEach((createPanel) => {
      const panelEl = createPanel();
      fragment.appendChild(
         panelEl.ownerDocument === doc
            ? panelEl
            : doc.importNode(panelEl, true)
      );
   });

   return fragment;
}

export class Panels {
   static mountConsoleOperationPanels(workspaceEl) {
      if (!workspaceEl) {
         return;
      }

      const doc = workspaceEl.ownerDocument || document;
      workspaceEl.replaceChildren(createConsoleOperationPanelsFragment(doc));
   }
}
