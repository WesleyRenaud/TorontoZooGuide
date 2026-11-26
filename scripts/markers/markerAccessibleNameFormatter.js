import { GuardiansTalkSelectorModel } from '../itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { MarkerHoverFormatter } from './markerHoverFormatter.js';
import { MarkerHoverTextFormatter } from './markerHoverTextFormatter.js';
import { ItemType } from '../shared/enums/itemType.js';
import { Strings } from '../strings.js';

export class MarkerAccessibleNameFormatter {
   static TITLE_FIELD_BY_TYPE = Object.freeze({
      [ItemType.ANIMAL]: 'species',
      [ItemType.PAVILION]: 'name',
      [ItemType.RESTAURANT]: 'name',
      [ItemType.RESTROOM]: 'title',
      [ItemType.GIFT_SHOP]: 'name',
      [ItemType.ATTRACTION]: 'name',
      [ItemType.TRANSPORTATION]: 'name',
      [ItemType.TRANSPORTATION_STATION]: 'name',
      [ItemType.GUEST_SERVICE]: 'service_type',
      [ItemType.EVENT_SITE]: 'name',
   });

   static FIXED_TITLE_BY_TYPE = Object.freeze({
      [ItemType.DRINKING_FOUNTAIN]: Strings.map.hover.drinkingFountain,
      [ItemType.DEFIBRILLATOR]: Strings.map.hover.defibrillator,
      [ItemType.EMERGENCY_INTERCOM]: Strings.map.hover.emergencyIntercom,
      [ItemType.PICNIC_SITE]: Strings.map.hover.picnicSite,
   });

   static FALLBACK_BY_TYPE = Object.freeze({
      [ItemType.ANIMAL]: Strings.entityLabels.animal,
      [ItemType.PAVILION]: Strings.entityLabels.pavilion,
      [ItemType.RESTAURANT]: Strings.entityLabels.restaurant,
      [ItemType.RESTROOM]: Strings.entityLabels.restroom,
      [ItemType.GIFT_SHOP]: Strings.entityLabels.giftShop,
      [ItemType.ATTRACTION]: Strings.entityLabels.attraction,
      [ItemType.TRANSPORTATION]: Strings.entityLabels.attraction,
      [ItemType.TRANSPORTATION_STATION]: Strings.entityLabels.transportationStation,
      [ItemType.GUEST_SERVICE]: Strings.map.hover.guestService,
      [ItemType.EVENT_SITE]: Strings.map.hover.eventSite,
   });

   static buildAccessibleName(items) {
      if (!Array.isArray(items) || items.length === 0) {
         return '';
      }

      if (items.length === 1) {
         return MarkerHoverFormatter.buildHoverText(items);
      }

      const type = String(items[0]?.type || '');

      if (MarkerHoverFormatter.HIDDEN_HOVER_TYPES.has(type)) {
         return '';
      }

      const firstName = MarkerAccessibleNameFormatter.getFirstItemName(items[0]);
      const noun = MarkerAccessibleNameFormatter.getGroupNoun(type);

      if (!firstName || !noun) {
         return MarkerHoverFormatter.buildHoverText(items);
      }

      const moreCount = items.length - 1;

      return Strings.map.markerAriaGroup(items.length, noun, firstName, moreCount);
   }

   static getGroupNoun(type) {
      if (type === ItemType.RESTAURANT) {
         return Strings.entityLabels.restaurants;
      }

      if (type === ItemType.RESTROOM) {
         return Strings.entityLabels.restrooms;
      }

      if (type === ItemType.GIFT_SHOP) {
         return Strings.entityLabels.giftShops;
      }

      if (type === ItemType.ATTRACTION || type === ItemType.TRANSPORTATION) {
         return Strings.entityLabels.attractions;
      }

      return Strings.map.markerAriaNouns[type] || '';
   }

   static getFirstItemName(item) {
      const type = String(item?.type || '');

      if (type === ItemType.GUARDIANS_TALK) {
         return MarkerAccessibleNameFormatter.getGuardiansTalkName(item);
      }

      if (type === ItemType.WILD_ENCOUNTER) {
         return MarkerAccessibleNameFormatter.getWildEncounterName(item);
      }

      const fixedTitle = MarkerAccessibleNameFormatter.FIXED_TITLE_BY_TYPE[type];

      if (fixedTitle) {
         return fixedTitle;
      }

      const field = MarkerAccessibleNameFormatter.TITLE_FIELD_BY_TYPE[type];

      if (!field) {
         return '';
      }

      const fallback = MarkerAccessibleNameFormatter.getTitleFallback(type);

      return MarkerHoverTextFormatter.readItemText(item, field, fallback);
   }

   static getGuardiansTalkName(item) {
      const name = GuardiansTalkSelectorModel.getGuardiansTalkDisplayName(item);

      if (name) {
         return name;
      }

      return Strings.entityLabels.guardiansTalk;
   }

   static getWildEncounterName(item) {
      const name = item?.name;

      if (name) {
         return name;
      }

      return Strings.map.hover.wildEncounterMeetingSpot;
   }

   static getTitleFallback(type) {
      return MarkerAccessibleNameFormatter.FALLBACK_BY_TYPE[type];
   }
}
