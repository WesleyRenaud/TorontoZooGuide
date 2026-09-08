import { InlineZooMapLoader } from './inlineZooMapLoader.js';

export class LoadInlineZooMapLoader {
   static async loadInlineZooMap() {
      const mount = InlineZooMapLoader.getZooMapMount();

      if (!mount) {
         return null;
      }

      const existingSvg = InlineZooMapLoader.getMountedSvg(mount);

      if (existingSvg) {
         return InlineZooMapLoader.configureInlineSvg(existingSvg);
      }

      const svg = await InlineZooMapLoader.mountInlineSvg(mount);

      if (!svg) {
         return null;
      }

      return InlineZooMapLoader.configureInlineSvg(svg);
   }
}
