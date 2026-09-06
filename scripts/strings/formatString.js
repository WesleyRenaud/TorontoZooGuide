export class FormatString {
   static formatString(template, params = {}) {
      return String(template).replace(
         /\{(\w+)\}/g,
         (match, key) => (
            Object.prototype.hasOwnProperty.call(params, key)
               ? String(params[key])
               : match
         )
      );
   }
}
