export class AnimalSpeciesAutocompleteHelper {
   static debounce(fn, delay = 200) {
      let timer = null;

      return (...args) => {
         clearTimeout(timer);
         timer = setTimeout(() => fn(...args), delay);
      };
   }
}
