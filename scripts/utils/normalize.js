export function normalizeParameter(parameter) {
   return String(parameter || '')
      .normalize('NFD')                      // split accents
      .replace(/[\u0300-\u036f]/g, '')       // remove accents
      .replace(/&/g, ' and ')                // replace & with "and"
      .toLowerCase()
      .replace(/['’]/g, '')                  // remove apostrophes
      .replace(/[^a-z0-9\s-]/g, '')          // remove punctuation & symbols
      .replace(/\s+/g, '-')                  // spaces → hyphens
      .replace(/-+/g, '-')                   // collapse multiple hyphens
      .replace(/^-|-$/g, '');                // trim leading/trailing hyphens
}