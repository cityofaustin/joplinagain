from django.db import models

from wagtail.core.models import Page
from wagtail.search import index
from wagtail.core.fields import RichTextField, StreamField
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.blocks import RichTextBlock, StructBlock, TextBlock, ListBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, HelpPanel, StreamFieldPanel, TabbedInterface, ObjectList
from . import forms as custom_forms

WYSIWYG_SERVICE_STEP = ['ul', 'ol', 'link', 'code']
WYSIWYG_GENERAL = ['h1', 'h2', 'h3', 'h4', 'bold', 'link', 'ul', 'ol', 'code']
SHORT_DESCRIPTION_LENGTH = 300

class HomePage(Page):
    subpage_types = ['ServicePage']

class JanisBasePage(Page):
    parent_page_types = ['HomePage']
    subpage_types = []
    search_fields = Page.search_fields + [
        index.RelatedFields('owner', [
            index.SearchField('last_name', partial_match=True),
            index.FilterField('last_name'),
        ])
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_notes = RichTextField(
        # max_length=DEFAULT_MAX_LENGTH,
        features=['ul', 'ol', 'link'],
        blank=True,
        verbose_name='Notes for authors (Not visible on the resident facing site)'
    )

    class Meta:
        abstract = True

class JanisPage(JanisBasePage):
    @cached_classmethod
    def get_edit_handler(cls):
        if hasattr(cls, 'edit_handler'):
            return cls.edit_handler.bind_to_model(cls)

        edit_handler = TabbedInterface([
            ObjectList(cls.content_panels + [
                FieldPanel('author_notes')
            ], heading='Content'),
            ObjectList(Page.promote_panels + cls.promote_panels, heading='Search Info')
        ])

        return edit_handler.bind_to_model(cls)

    class Meta:
        abstract = True

class ServicePage(JanisPage):

    # TODO: FKs
    # department = models.ForeignKey(
    #     'base.DepartmentPage',
    #     on_delete=models.PROTECT,
    #     verbose_name='Select a Department',
    #     blank=True,
    #     null=True,
    # )

    steps = StreamField(
        [
            ('basic_step', RichTextBlock(
                features=WYSIWYG_SERVICE_STEP,
                label='Basic Step'
            )),
            ('step_with_options_accordian', StructBlock(
                [
                    ('options_description', TextBlock('Describe the set of options')),
                    ('options', ListBlock(
                        StructBlock([
                            ('option_name', TextBlock(
                                label='Option name. (When clicked, this name will expand the content for this option'
                            )),
                            ('option_description', RichTextBlock(
                                features=WYSIWYG_SERVICE_STEP,
                                label='Option Content',
                            )),
                        ]),
                    )),
                ],
                label="Step With Options"
            )),
        ],
        verbose_name='Write out the steps a resident needs to take to use the service',
        # this gets called in the help panel
        help_text='A step may have a basic text step or an options accordian which reveals two or more options',
        blank=True
    )

    # TODO: custom blocks
    # dynamic_content = StreamField(
    #     [
    #         ('map_block', custom_blocks.SnippetChooserBlockWithAPIGoodness('base.Map', icon='site')),
    #         ('what_do_i_do_with_block', custom_blocks.WhatDoIDoWithBlock()),
    #         ('collection_schedule_block', custom_blocks.CollectionScheduleBlock()),
    #         ('recollect_block', custom_blocks.RecollectBlock()),
    #     ],
    #     verbose_name='Add any maps or apps that will help the resident use the service',
    #     blank=True
    # )
    additional_content = RichTextField(
        features=WYSIWYG_GENERAL,
        verbose_name='Write any additional content describing the service',
        help_text='Section header: What else do I need to know?',
        blank=True
    )

    # TODO: custom forms
    base_form_class = custom_forms.ServicePageForm

    short_description = models.TextField(
        max_length=SHORT_DESCRIPTION_LENGTH,
        blank=True,
        verbose_name='Write a description of this service'
    )

    content_panels = [
        FieldPanel('title'),
        FieldPanel('short_description'),
        # TODO: FKs
        # InlinePanel('topics', label='Topics'),
        # FieldPanel('department'),
        MultiFieldPanel(
        [
            HelpPanel(steps.help_text, classname="coa-helpPanel"),
            StreamFieldPanel('steps')
        ],
        heading=steps.verbose_name,
        classname='coa-multiField-nopadding'
        ),
        # TODO: custom blocks
        # StreamFieldPanel('dynamic_content'),
        MultiFieldPanel(
        [
            HelpPanel(additional_content.help_text, classname="coa-helpPanel"),
            FieldPanel('additional_content')
        ],
        heading=additional_content.verbose_name,
        classname='coa-multiField-nopadding'
        ),
        # TODO: FKs
        # InlinePanel('contacts', label='Contacts'),
    ]