from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page

from modelcluster.fields import ParentalKey


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock()
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)


@register_setting
class FooterBarSettings(BaseSiteSetting):
    brand_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    brand_image_alt = models.CharField(max_length=255, blank=True)
    brand_link_url = models.URLField(blank=True)
    instagram_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    instagram_url = models.URLField(blank=True)
    maps_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    maps_url = models.URLField(blank=True)

    panels = [
        FieldPanel("brand_image"),
        FieldPanel("brand_image_alt"),
        FieldPanel("brand_link_url"),
        FieldPanel("instagram_image"),
        FieldPanel("instagram_url"),
        FieldPanel("maps_image"),
        FieldPanel("maps_url"),
    ]


@register_setting
class SharedNavigationSettings(BaseSiteSetting):
    navigation_items = StreamField(
        [
            (
                "item",
                blocks.StructBlock(
                    [
                        ("page", blocks.PageChooserBlock()),
                        ("label", blocks.CharBlock(required=False)),
                    ]
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )

    panels = [
        FieldPanel("navigation_items"),
    ]


class PageHeroBlock(blocks.StructBlock):
    kicker = blocks.CharBlock(required=False, default="Subsite")
    title = blocks.CharBlock(required=False)
    intro = blocks.TextBlock(required=False)

    class Meta:
        template = "home/blocks/page_hero.html"
        icon = "title"
        label = "Page hero"


class LandingCardBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=False, default="Chandra Kumala")
    title = blocks.CharBlock()
    text = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    image_portrait = ImageChooserBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False)

    class Meta:
        icon = "image"
        label = "Landing card"


class LandingSectionBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        LandingCardBlock(),
        min_num=1,
        max_num=3,
        label="Cards",
    )
    overview_eyebrow = blocks.CharBlock(required=False, default="Overview")
    overview_title = blocks.CharBlock(
        required=False,
        default="Discover the three learning pathways in one place.",
    )
    overview_text = blocks.TextBlock(
        required=False,
        default=(
            "Move from early years through upper levels with a homepage that keeps "
            "each subsite visible while still leaving room for supporting content, "
            "updates, and highlights below."
        ),
    )
    highlight_one_title = blocks.CharBlock(required=False, default="Primary")
    highlight_one_text = blocks.TextBlock(
        required=False,
        default=(
            "Hands-on classroom moments, practical learning, and a welcoming first "
            "step into school life."
        ),
    )
    highlight_two_title = blocks.CharBlock(required=False, default="Secondary")
    highlight_two_text = blocks.TextBlock(
        required=False,
        default=(
            "Independent thinking, performance, and wider academic exploration "
            "across subjects and activities."
        ),
    )

    class Meta:
        template = "home/blocks/landing_section.html"
        icon = "placeholder"
        label = "Landing section"


class PopupAnnouncementBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, default="Announcement")
    title = blocks.CharBlock()
    text = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    button_text = blocks.CharBlock(required=False)
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)

    class Meta:
        template = "home/blocks/popup_announcement.html"
        icon = "warning"
        label = "Popup announcement"


class HomePage(Page):
    max_count = 1
    subpage_types = ["home.SubsitePage", "home.AdmissionsPage"]
    body = StreamField(
        [
            ("landing_section", LandingSectionBlock()),
            ("popup_announcement", PopupAnnouncementBlock()),
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.TextBlock()),
            ("rich_text", blocks.RichTextBlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ("boolean", blocks.BooleanBlock(required=False)),
            ("integer", blocks.IntegerBlock()),
            ("decimal", blocks.DecimalBlock()),
            ("float", blocks.FloatBlock()),
            (
                "choice",
                blocks.ChoiceBlock(
                    choices=[
                        ("primary", "Primary"),
                        ("secondary", "Secondary"),
                        ("tertiary", "Tertiary"),
                    ]
                ),
            ),
            ("date", blocks.DateBlock()),
            ("time", blocks.TimeBlock()),
            ("datetime", blocks.DateTimeBlock()),
            ("email", blocks.EmailBlock()),
            ("url", blocks.URLBlock()),
            ("page", blocks.PageChooserBlock()),
            ("image", ImageChooserBlock()),
            ("document", DocumentChooserBlock()),
            ("embed", EmbedBlock()),
            ("html", blocks.RawHTMLBlock()),
            ("list", blocks.ListBlock(blocks.CharBlock(label="Item"))),
            ("call_to_action", CallToActionBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["landing_section_present"] = any(
            block.block_type == "landing_section" for block in self.body
        )
        context["subsite_cards"] = (
            self.get_children()
            .live()
            .public()
            .specific()[:3]
        )
        return context


class SubsitePage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.SectionPage"]

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = models.TextField(blank=True)
    hero_content = StreamField(
        [
            ("page_hero", PageHeroBlock()),
        ],
        use_json_field=True,
        blank=True,
        max_num=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("intro"),
        FieldPanel("hero_content"),
    ]

    def get_navigation_items(self, request):
        nav_items = [
            {"page": item, "label": item.navigation_title}
            for item in self.get_children().live().public().specific()
        ]
        shared_nav_settings = SharedNavigationSettings.for_request(request)
        for shared_item in shared_nav_settings.navigation_items:
            shared_page = shared_item.value["page"].specific
            if shared_page.live and all(item["page"].pk != shared_page.pk for item in nav_items):
                nav_items.append(
                    {
                        "page": shared_page,
                        "label": shared_item.value["label"] or shared_page.title,
                    }
                )

        return nav_items

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["section_pages"] = self.get_children().live().public().specific()
        context["nav_pages"] = self.get_navigation_items(request)
        return context


class SectionPage(Page):
    parent_page_types = ["home.SubsitePage"]
    subpage_types = []

    nav_label = models.CharField(max_length=80, blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = models.TextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("nav_label"),
        FieldPanel("hero_image"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        subsite_root = self.get_parent().specific
        context["subsite_root"] = subsite_root
        context["home_page"] = subsite_root.get_parent().specific
        context["nav_pages"] = subsite_root.get_navigation_items(request)
        context["section_theme"] = subsite_root.slug
        return context

    @property
    def navigation_title(self):
        return self.nav_label or self.title


class AdmissionsPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        InlinePanel("sections", label="Admissions sections"),
    ]

    def get_shared_navigation_items(self, request):
        shared_nav_settings = SharedNavigationSettings.for_request(request)
        nav_items = []

        for shared_item in shared_nav_settings.navigation_items:
            shared_page = shared_item.value["page"].specific
            if shared_page.live:
                nav_items.append(
                    {
                        "page": shared_page,
                        "label": shared_item.value["label"] or shared_page.title,
                    }
                )

        return nav_items

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["subsite_root"] = self
        context["nav_pages"] = self.get_shared_navigation_items(request)
        context["admissions_sections"] = self.sections.all()
        return context


class AdmissionsSection(Orderable):
    page = ParentalKey(
        "home.AdmissionsPage",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    nav_label = models.CharField(max_length=80)
    heading = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    button_text = models.CharField(max_length=80, blank=True)
    button_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    button_url = models.URLField(blank=True)

    panels = [
        FieldPanel("nav_label"),
        FieldPanel("heading"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("document"),
        FieldPanel("button_text"),
        FieldPanel("button_page"),
        FieldPanel("button_url"),
    ]
