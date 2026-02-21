export function normalizeParameter(parameter) {
   return String(parameter || '')
      .normalize('NFD')                    // split letters + accents
      .replace(/[\u0300-\u036f]/g, '')     // remove accent marks
      .toLowerCase()
      .replaceAll(' ', '-')
      .replaceAll("'", '');
}