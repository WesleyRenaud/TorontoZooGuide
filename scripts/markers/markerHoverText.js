import { MarkerHoverTextFormatter } from './markerHoverTextFormatter.js';
import { Strings } from '../strings.js';

const HIDDEN_HOVER_TYPES = new Set([
   'transportationRouteMarker',
]);

const HOVER_FORMATTERS = Object.freeze({
   animal: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'species', Strings.entityLabels.animal)
   ),
   pavilion: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.pavilion)
   ),
   restaurant: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.restaurant)
   ),
   restroom: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'title', Strings.entityLabels.restroom)
   ),
   giftShop: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.giftShop)
   ),
   attraction: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.attraction)
   ),
   transportation: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.attraction)
   ),
   transportationStation: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.entityLabels.transportationStation)
   ),
   guardiansTalk: MarkerHoverTextFormatter.formatGuardiansTalkHoverText,
   wildEncounter: MarkerHoverTextFormatter.formatWildEncounterHoverText,
   drinkingFountain: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      () => Strings.map.hover.drinkingFountain
   ),
   defibrillator: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      () => Strings.map.hover.defibrillator
   ),
   emergencyIntercom: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      () => Strings.map.hover.emergencyIntercom
   ),
   guestService: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'service_type', Strings.map.hover.guestService)
   ),
   picnicSite: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      () => Strings.map.hover.picnicSite
   ),
   eventSite: (items) => MarkerHoverTextFormatter.formatCountedHoverText(
      items,
      (item) => MarkerHoverTextFormatter.readItemText(item, 'name', Strings.map.hover.eventSite)
   ),
});

export class MarkerHoverText {
   static buildHoverText(itemsAtPoint) {
      if (!itemsAtPoint || itemsAtPoint.length === 0) {
         return '';
      }

      const type = String(itemsAtPoint[0].type || '');
      const formatter = HOVER_FORMATTERS[type];

      if (HIDDEN_HOVER_TYPES.has(type) || !formatter) {
         return '';
      }

      return formatter(itemsAtPoint);
   }
}
