export class SearchResultPresentationHelper {
   static buildNamedResultPresentation(fallbackTitle, getSubtitle) {
      return {
         getTitle: (row) => row.name || fallbackTitle,
         getSubtitle,
      };
   }
}
