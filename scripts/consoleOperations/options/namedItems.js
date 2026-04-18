export function getOptionItemName(item) {
   return typeof item === 'string'
      ? item
      : item.name ?? item.NAME ?? '';
}

export function sortNamedOptions(items = []) {
   return items
      .slice()
      .sort((a, b) => String(getOptionItemName(a)).localeCompare(String(getOptionItemName(b))));
}
