import { createOffDisplayPanel } from '../animals/panels/offDisplayPanel.js';
import { createOnDisplayPanel } from '../animals/panels/onDisplayPanel.js';
import { createRemoveViewingAlertPanel } from '../animals/panels/removeViewingAlertPanel.js';
import { createRemoveVisibilitySchedulePanel } from '../animals/panels/removeVisibilitySchedulePanel.js';
import { createViewingAlertPanel } from '../animals/panels/viewingAlertPanel.js';
import { createVisibilitySchedulePanel } from '../animals/panels/visibilitySchedulePanel.js';
import { createAttractionClosedPanel } from '../attractions/panels/attractionClosedPanel.js';
import { createAttractionClosureOverridePanel } from '../attractions/panels/attractionClosureOverridePanel.js';
import { createAttractionHoursSchedulePanel } from '../attractions/panels/attractionHoursSchedulePanel.js';
import { createAttractionOpeningSchedulePanel } from '../attractions/panels/attractionOpeningSchedulePanel.js';
import { createDrinkingFountainsClosedPanel } from '../drinkingFountains/panels/drinkingFountainsClosedPanel.js';
import { createDrinkingFountainsOpenPanel } from '../drinkingFountains/panels/drinkingFountainsOpenPanel.js';
import { createCreateEventPanel } from '../events/panels/createEventPanel.js';
import { createExhibitClosedPanel } from '../exhibits/panels/exhibitClosedPanel.js';
import { createExhibitOpenPanel } from '../exhibits/panels/exhibitOpenPanel.js';
import { createGiftShopClosedPanel } from '../giftShops/panels/giftShopClosedPanel.js';
import { createGiftShopClosureOverridePanel } from '../giftShops/panels/giftShopClosureOverridePanel.js';
import { createGiftShopOpeningSchedulePanel } from '../giftShops/panels/giftShopOpeningSchedulePanel.js';
import { createAddGuardiansTalkOccurrencePanel } from '../guardiansTalks/panels/addGuardiansTalkOccurrencePanel.js';
import { createCancelGuardiansTalkOccurrencePanel } from '../guardiansTalks/panels/cancelGuardiansTalkOccurrencePanel.js';
import { createEndGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/endGuardiansTalkSchedulePanel.js';
import { createGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/guardiansTalkSchedulePanel.js';
import { createRestaurantClosedPanel } from '../restaurants/panels/restaurantClosedPanel.js';
import { createRestaurantClosureOverridePanel } from '../restaurants/panels/restaurantClosureOverridePanel.js';
import { createRestaurantOpeningSchedulePanel } from '../restaurants/panels/restaurantOpeningSchedulePanel.js';
import { createRemoveRestroomAlertPanel } from '../restrooms/panels/removeRestroomAlertPanel.js';
import { createRestroomAlertPanel } from '../restrooms/panels/restroomAlertPanel.js';
import { createRestroomClosedPanel } from '../restrooms/panels/restroomClosedPanel.js';
import { createRestroomOpenPanel } from '../restrooms/panels/restroomOpenPanel.js';
import { createTransportationRoutePanel } from '../transportation/panels/transportationRoutePanel.js';
import { createTransportationStationClosedPanel } from '../transportation/panels/transportationStationClosedPanel.js';
import { createTransportationStationOpenPanel } from '../transportation/panels/transportationStationOpenPanel.js';
import { createCreateUpdatePanel } from '../updates/panels/createUpdatePanel.js';
import { createEditUpdatePanel } from '../updates/panels/editUpdatePanel.js';
import { createEndUpdatePanel } from '../updates/panels/endUpdatePanel.js';
import { createCancelWildEncounterOccurrencePanel } from '../wildEncounters/panels/cancelWildEncounterOccurrencePanel.js';
import { createEndWildEncounterSchedulePanel } from '../wildEncounters/panels/endWildEncounterSchedulePanel.js';
import { createWildEncounterSchedulePanel } from '../wildEncounters/panels/wildEncounterSchedulePanel.js';

const PANEL_CREATORS = {
   animals: [
      createOffDisplayPanel,
      createOnDisplayPanel,
      createVisibilitySchedulePanel,
      createRemoveVisibilitySchedulePanel,
      createViewingAlertPanel,
      createRemoveViewingAlertPanel,
   ],
   exhibits: [
      createExhibitClosedPanel,
      createExhibitOpenPanel,
   ],
   restaurants: [
      createRestaurantClosedPanel,
      createRestaurantClosureOverridePanel,
      createRestaurantOpeningSchedulePanel,
   ],
   restrooms: [
      createRestroomClosedPanel,
      createRestroomOpenPanel,
      createRestroomAlertPanel,
      createRemoveRestroomAlertPanel,
   ],
   giftShops: [
      createGiftShopClosedPanel,
      createGiftShopClosureOverridePanel,
      createGiftShopOpeningSchedulePanel,
   ],
   attractions: [
      createAttractionClosedPanel,
      createAttractionClosureOverridePanel,
      createAttractionOpeningSchedulePanel,
      createAttractionHoursSchedulePanel,
   ],
   transportation: [
      createTransportationStationClosedPanel,
      createTransportationStationOpenPanel,
      createTransportationRoutePanel,
   ],
   guardiansTalks: [
      createGuardiansTalkSchedulePanel,
      createEndGuardiansTalkSchedulePanel,
      createAddGuardiansTalkOccurrencePanel,
      createCancelGuardiansTalkOccurrencePanel,
   ],
   wildEncounters: [
      createWildEncounterSchedulePanel,
      createEndWildEncounterSchedulePanel,
      createCancelWildEncounterOccurrencePanel,
   ],
   drinkingFountains: [
      createDrinkingFountainsClosedPanel,
      createDrinkingFountainsOpenPanel,
   ],
   events: [
      createCreateEventPanel,
   ],
   updates: [
      createCreateUpdatePanel,
      createEndUpdatePanel,
      createEditUpdatePanel,
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

export function mountConsoleOperationPanels(workspaceEl) {
   if (!workspaceEl) {
      return;
   }

   const doc = workspaceEl.ownerDocument || document;
   workspaceEl.replaceChildren(createConsoleOperationPanelsFragment(doc));
}
