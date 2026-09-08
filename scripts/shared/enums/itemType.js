import itemTypeValues from '../../../shared/enums/itemType.json' with { type: 'json' };

export class ItemType {
   static {
      Object.assign(ItemType, itemTypeValues);
   }
}
