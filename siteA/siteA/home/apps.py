import imghdr

from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"

    def ready(self):
        try:
            import pillow_avif  # noqa: F401
        except ImportError:
            return

        from willow.image import INITIAL_IMAGE_CLASSES, ImageFile
        from willow.plugins.pillow import PillowImage
        from willow.registry import registry

        class AVIFImageFile(ImageFile):
            format_name = "avif"

        def test_avif(header, file_obj):
            if len(header) < 16 or header[4:8] != b"ftyp":
                return None

            brand_bytes = header[8:32]
            for offset in range(0, len(brand_bytes) - 3, 4):
                if brand_bytes[offset:offset + 4] in {b"avif", b"avis"}:
                    return "avif"

            return None

        if not any(getattr(test, "__name__", "") == "test_avif" for test in imghdr.tests):
            imghdr.tests.append(test_avif)

        INITIAL_IMAGE_CLASSES["avif"] = AVIFImageFile
        registry.register_image_class(AVIFImageFile)
        registry.register_converter(AVIFImageFile, PillowImage, PillowImage.open)
