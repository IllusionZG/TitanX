from __future__ import unicode_literals
from .actions import get_action
from abc import ABCMeta
from future.utils import with_metaclass
from .base import Base

class Flex(with_metaclass(ABCMeta, Base)):
    def __init__(self,alt_text=None, contents=None, **kwargs):
        super(Flex, self).__init__(**kwargs)

        self.type = 'flex'
        self.alt_text = alt_text if alt_text else 'Send a Flex Message'
        self.contents = contents
        self.contents = self.DevLJsonDictTypes(
            contents, {
                'bubble': Bubble,
                'carousel': Carousel
            }
        )

class FlexContainer(with_metaclass(ABCMeta, Base)):

    def __init__(self, **kwargs):
        super(FlexContainer, self).__init__(**kwargs)
        self.type = None

class Bubble(FlexContainer):

    def __init__(self, direction=None, header=None, hero=None, body=None, footer=None, styles=None,
                 **kwargs):

        super(Bubble, self).__init__(**kwargs)

        self.type = 'bubble'
        self.direction = direction
        self.header = self.get_or_new_from_json_dict(header, Box)
        self.hero = self.get_or_new_from_json_dict(hero, Image)
        self.body = self.get_or_new_from_json_dict(body, Box)
        self.footer = self.get_or_new_from_json_dict(footer, Box)
        self.styles = self.get_or_new_from_json_dict(styles, BubbleStyle)


class BubbleStyle(with_metaclass(ABCMeta, Base)):

    def __init__(self, header=None, hero=None, body=None, footer=None, **kwargs):

        super(BubbleStyle, self).__init__(**kwargs)

        self.header = self.get_or_new_from_json_dict(header, BlockStyle)
        self.hero = self.get_or_new_from_json_dict(hero, BlockStyle)
        self.body = self.get_or_new_from_json_dict(body, BlockStyle)
        self.footer = self.get_or_new_from_json_dict(footer, BlockStyle)


class BlockStyle(with_metaclass(ABCMeta, Base)):


    def __init__(self, background_color=None, separator=None, separator_color=None, **kwargs):

        super(BlockStyle, self).__init__(**kwargs)
        self.background_color = background_color
        self.separator = separator
        self.separator_color = separator_color


class Carousel(FlexContainer):

    def __init__(self, contents=None, **kwargs):
        super(Carousel, self).__init__(**kwargs)

        self.type = 'carousel'

        new_contents = []
        if contents:
            for it in contents:
                new_contents.append(self.get_or_new_from_json_dict(
                    it, Bubble
                ))
        self.contents = new_contents


class FlexComponent(with_metaclass(ABCMeta, Base)):

    def __init__(self, **kwargs):
        """__init__ method.
        :param kwargs:
        """
        super(FlexComponent, self).__init__(**kwargs)

        self.type = None


class Box(FlexComponent):

    def __init__(self, layout=None, contents=None, flex=None, spacing=None, margin=None, **kwargs):

        super(Box, self).__init__(**kwargs)
        self.type = 'box'
        self.layout = layout
        self.flex = flex
        self.spacing = spacing
        self.margin = margin

        new_contents = []
        if contents:
            for it in contents:
                new_contents.append(self.DevLJsonDictTypes(
                    it, {
                        'box': Box,
                        'button': Button,
                        'filler': Filler,
                        'icon': Icon,
                        'image': Image,
                        'separator': Separator,
                        'spacer': Spacer,
                        'text': Text
                    }
                ))
        self.contents = new_contents


class Button(FlexComponent):


    def __init__(self, action=None, flex=None, margin=None, height=None, style=None, color=None,
                 gravity=None, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.type = 'button'
        self.action = get_action(action)
        self.flex = flex
        self.margin = margin
        self.height = height
        self.style = style
        self.color = color
        self.gravity = gravity


class Filler(FlexComponent):

    def __init__(self, **kwargs):
        """__init__ method.
        :param kwargs:
        """
        super(Filler, self).__init__(**kwargs)
        self.type = 'filler'


class Icon(FlexComponent):

    def __init__(self, url=None, margin=None, size=None, aspect_ratio=None, **kwargs):
        super(Icon, self).__init__(**kwargs)
        self.type = 'icon'
        self.url = url
        self.margin = margin
        self.size = size
        self.aspect_ratio = aspect_ratio


class Image(FlexComponent):

    def __init__(self, url=None, flex=None, margin=None, align=None, gravity=None, size=None,
                 aspect_ratio=None, aspect_mode=None, background_color=None, action=None,
                 **kwargs):

        super(Image, self).__init__(**kwargs)
        self.type = 'image'
        self.url = url
        self.flex = flex
        self.margin = margin
        self.align = align
        self.gravity = gravity
        self.size = size
        self.aspect_ratio = aspect_ratio
        self.aspect_mode = aspect_mode
        self.background_color = background_color
        self.action = get_action(action)


class Separator(FlexComponent):

    def __init__(self, margin=None, color=None, **kwargs):
        super(Separator, self).__init__(**kwargs)
        self.type = 'separator'
        self.margin = margin
        self.color = color


class Spacer(FlexComponent):

    def __init__(self, size=None, **kwargs):
        """__init__ method.
        :param str size: Size of the space
        :param kwargs:
        """
        super(Spacer, self).__init__(**kwargs)
        self.type = 'spacer'
        self.size = size


class Text(FlexComponent):
    """Text.
    https://developers.line.me/en/docs/messaging-api/reference/#text-component
    This component draws text. You can format the text.
    """

    def __init__(self, text=None, flex=None, margin=None, size=None, align=None, gravity=None,
                 wrap=None, weight=None,
                 color=None, action=None, **kwargs):
        r"""__init__ method.
        :param str text: Text
        :param float flex: The ratio of the width or height of this component within the parent box
        :param str margin: Minimum space between this component
            and the previous component in the parent box
        :param str size: Font size
        :param str align: Horizontal alignment style
        :param str gravity: Vertical alignment style
        :param bool wrap: rue to wrap text. The default value is False.
            If set to True, you can use a new line character (\n) to begin on a new line.
        :param str weight: Font weight
        :param str color: Font color
        :param action: Action performed when this image is tapped
        :type action: list[T <= :py:class:`linebot.models.actions.Action`]
        :param kwargs:
        """
        super(Text, self).__init__(**kwargs)
        self.type = 'text'
        self.text = text
        self.flex = flex
        self.margin = margin
        self.size = size
        self.align = align
        self.gravity = gravity
        self.wrap = wrap
        self.weight = weight
        self.color = color
        self.action = get_action(action)