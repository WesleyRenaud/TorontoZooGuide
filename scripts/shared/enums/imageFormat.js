import imageFormatValues from '../../../shared/enums/imageFormat.json' with { type: 'json' };

export class ImageFormat {
   static {
      Object.assign(ImageFormat, imageFormatValues);
      ImageFormat.ACCEPT = Object.values(imageFormatValues)
         .map(format => format.mime)
         .join(',');
   }
}
