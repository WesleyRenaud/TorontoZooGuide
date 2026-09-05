export class NamedItems {
   static getOptionItemName(item) {
      return typeof item === 'string'
         ? item
         : item.name ?? '';
   }

   static sortNamedOptions(items = []) {
      return items
         .slice()
         .sort((a, b) => String(NamedItems.getOptionItemName(a))
            .localeCompare(String(NamedItems.getOptionItemName(b))));
   }
}
