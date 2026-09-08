import { MarkerHoverTextFormatter } from './markerHoverTextFormatter.js';
import { ItemType } from '../shared/enums/itemType.js';
import { Strings } from '../strings.js';

export class MarkerHoverFormatter {
   static HIDDEN_HOVER_TYPES = new Set([
      ItemType.TRANSPORTATION_ROUTE_MARKER,
   ]);

   static HOVER_FORMATTERS = Object.freeze({
      [ItemType.ANIMAL]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'species', Strings.entityLabels.animal)
      ),
      [ItemType.PAVILION]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.pavilion)
      ),
      [ItemType.RESTAURANT]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.restaurant)
      ),
      [ItemType.RESTROOM]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'title', Strings.entityLabels.restroom)
      ),
      [ItemType.GIFT_SHOP]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.giftShop)
      ),
      [ItemType.ATTRACTION]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.attraction)
      ),
      [ItemType.TRANSPORTATION]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.attraction)
      ),
      [ItemType.TRANSPORTATION_STATION]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.transportationStation)
      ),
      [ItemType.GUARDIANS_TALK]: MarkerHoverTextFormatter.formatGuardiansTalkHoverText,
      [ItemType.WILD_ENCOUNTER]: MarkerHoverTextFormatter.formatWildEncounterHoverText,
      [ItemType.DRINKING_FOUNTAIN]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         () => Strings.map.hover.drinkingFountain
      ),
      [ItemType.DEFIBRILLATOR]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         () => Strings.map.hover.defibrillator
      ),
      [ItemType.EMERGENCY_INTERCOM]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         () => Strings.map.hover.emergencyIntercom
      ),
      [ItemType.GUEST_SERVICE]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'service_type', Strings.map.hover.guestService)
      ),
      [ItemType.PICNIC_SITE]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         () => Strings.map.hover.picnicSite
      ),
      [ItemType.EVENT_SITE]: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
         items,
         (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.map.hover.eventSite)
      ),
   });

   static buildHoverText(itemsAtPoint) {
      if (!itemsAtPoint || itemsAtPoint.length === 0) {
         return '';
      }

      const type = String(itemsAtPoint[0].type || '');
      const formatter = MarkerHoverFormatter.HOVER_FORMATTERS[type];

      if (MarkerHoverFormatter.HIDDEN_HOVER_TYPES.has(type) || !formatter) {
         return '';
      }

      return formatter(itemsAtPoint);
   }
}
