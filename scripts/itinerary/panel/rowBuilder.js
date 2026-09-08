import { ItemView } from './components/itemView.js';
import { RowBuildersHelper } from './rowBuildersHelper.js';
import { RowPresenter } from './rowPresenter.js';
import { SpeciesExhibitKey } from '../speciesExhibitKey.js';

export class RowBuilder {
   static buildUniqueAnimals(animals = []) {
      return SpeciesExhibitKey.buildUniqueSpeciesExhibitEntries(animals, {
         buildKey: SpeciesExhibitKey.buildAnimalViewingSpotKey,
         mergeAnimals: (existing, animal) => ({
            ...existing,
            likelihood: RowBuildersHelper.maxStoredLikelihood(existing.likelihood, animal.likelihood),
            old_likelihood: RowBuildersHelper.maxStoredLikelihood(
               existing.old_likelihood,
               animal.old_likelihood
            ),
            likelihoodBefore: RowBuildersHelper.maxStoredLikelihood(
               existing.likelihoodBefore,
               animal.likelihoodBefore
            ),
            likelihoodAfter: RowBuildersHelper.maxStoredLikelihood(
               existing.likelihoodAfter,
               animal.likelihoodAfter
            ),
         }),
         requireExhibit: false,
      }).map(({ item }) => item);
   }

   static buildRows(
      items = [],
      {
         normalizeItem,
         prepareItems = (normalizedItems) => normalizedItems,
         buildRowProps,
      } = {}
   ) {
      const preparedItems = prepareItems(
         RowBuildersHelper.normalizeItems(items, normalizeItem)
      );

      return preparedItems.map((item) => ItemView.makeItemRow(buildRowProps(item)));
   }

   static buildNamedRows(
      items = [],
      {
         normalizeItem,
         prepareItems = (normalizedItems) => normalizedItems,
         defaultName,
         imageDirectory,
         getName,
         getImageName = getName,
         getNameSuffix = () => '',
         getMetaLines = () => [],
         getAlertLine = () => '',
         getLink = () => null,
         extendRowProps = null,
      } = {}
   ) {
      return RowBuilder.buildRows(items, {
         normalizeItem,
         prepareItems,
         buildRowProps: (item) => {
            const name = getName(item) || defaultName;
            const imageName = getImageName(item) || name;

            return {
               name,
               nameSuffix: getNameSuffix(item),
               imageSrc: RowPresenter.buildImageSrc(imageDirectory, imageName),
               metaLines: RowPresenter.buildMetaLines(getMetaLines(item)),
               alertLine: getAlertLine(item),
               ...RowPresenter.buildLinkRowProps(getLink(item)),
               ...(typeof extendRowProps === 'function' ? extendRowProps(item) : {}),
            };
         },
      });
   }
}
