export function normalizeParameter(parameter) {
   return String(parameter || '')
      .toLowerCase()
      .replaceAll(' ', '-')
      .replaceAll("'", '');
}