import { createOffDisplayPanel } from '../animals/panels/offDisplayPanel.js';
import { createOnDisplayPanel } from '../animals/panels/onDisplayPanel.js';
import { createRemoveViewingAlertPanel } from '../animals/panels/removeViewingAlertPanel.js';
import { createRemoveVisibilitySchedulePanel } from '../animals/panels/removeVisibilitySchedulePanel.js';
import { createViewingAlertPanel } from '../animals/panels/viewingAlertPanel.js';
import { createVisibilitySchedulePanel } from '../animals/panels/visibilitySchedulePanel.js';
import { createAttractionClosedPanel } from '../attractions/panels/attractionClosedPanel.js';
import { createAttractionOpenPanel } from '../attractions/panels/attractionOpenPanel.js';
import { createDrinkingFountainsClosedPanel } from '../drinkingFountains/panels/drinkingFountainsClosedPanel.js';
import { createDrinkingFountainsOpenPanel } from '../drinkingFountains/panels/drinkingFountainsOpenPanel.js';
import { createExhibitClosedPanel } from '../exhibits/panels/exhibitClosedPanel.js';
import { createExhibitOpenPanel } from '../exhibits/panels/exhibitOpenPanel.js';
import { createGiftShopClosedPanel } from '../giftShops/panels/giftShopClosedPanel.js';
import { createGiftShopOpenPanel } from '../giftShops/panels/giftShopOpenPanel.js';
import { createCancelGuardiansTalkOccurrencePanel } from '../guardiansTalks/panels/cancelGuardiansTalkOccurrencePanel.js';
import { createEndGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/endGuardiansTalkSchedulePanel.js';
import { createGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/guardiansTalkSchedulePanel.js';
import { createRestaurantClosedPanel } from '../restaurants/panels/restaurantClosedPanel.js';
import { createRestaurantOpenPanel } from '../restaurants/panels/restaurantOpenPanel.js';
import { createRemoveRestroomAlertPanel } from '../restrooms/panels/removeRestroomAlertPanel.js';
import { createRestroomAlertPanel } from '../restrooms/panels/restroomAlertPanel.js';
import { createRestroomClosedPanel } from '../restrooms/panels/restroomClosedPanel.js';
import { createRestroomOpenPanel } from '../restrooms/panels/restroomOpenPanel.js';
import { createCreateUpdatePanel } from '../updates/panels/createUpdatePanel.js';
import { createEditUpdatePanel } from '../updates/panels/editUpdatePanel.js';
import { createEndUpdatePanel } from '../updates/panels/endUpdatePanel.js';
import { createCancelWildEncounterOccurrencePanel } from '../wildEncounters/panels/cancelWildEncounterOccurrencePanel.js';
import { createEndWildEncounterSchedulePanel } from '../wildEncounters/panels/endWildEncounterSchedulePanel.js';
import { createWildEncounterSchedulePanel } from '../wildEncounters/panels/wildEncounterSchedulePanel.js';
import { createZoomobileRoutePanel } from '../zoomobile/panels/zoomobileRoutePanel.js';
import { createZoomobileStationClosedPanel } from '../zoomobile/panels/zoomobileStationClosedPanel.js';
import { createZoomobileStationOpenPanel } from '../zoomobile/panels/zoomobileStationOpenPanel.js';

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
      createRestaurantOpenPanel,
   ],
   restrooms: [
      createRestroomClosedPanel,
      createRestroomOpenPanel,
      createRestroomAlertPanel,
      createRemoveRestroomAlertPanel,
   ],
   giftShops: [
      createGiftShopClosedPanel,
      createGiftShopOpenPanel,
   ],
   attractions: [
      createAttractionClosedPanel,
      createAttractionOpenPanel,
   ],
   zoomobile: [
      createZoomobileStationClosedPanel,
      createZoomobileStationOpenPanel,
      createZoomobileRoutePanel,
   ],
   guardiansTalks: [
      createGuardiansTalkSchedulePanel,
      createEndGuardiansTalkSchedulePanel,
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
