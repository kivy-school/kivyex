import asynckivy
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior

from kivymd.app import MDApp
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon

KV = '''
<ExpansionPanelItem>:

    MDExpansionPanelHeader:

        MDListItem:
            theme_bg_color: "Custom"
            md_bg_color: self.theme_cls.surfaceContainerLowColor
            ripple_effect: False

            MDListItemSupportingText:
                text: "Supporting text"

            TrailingPressedIconButton:
                id: chevron
                icon: "chevron-right"
                on_release: app.tap_expansion_chevron(root, chevron)

    MDExpansionPanelContent:
        orientation: "vertical"
        padding: "12dp", 0, "12dp", "12dp"
        md_bg_color: self.theme_cls.surfaceContainerLowestColor

        MDLabel:
            text: "Channel information"
            adaptive_height: True
            padding: "10dp"           #### Change padding

        MDListItem:
            theme_bg_color: "Custom"
            md_bg_color: self.theme_cls.surfaceContainerLowestColor

            MDListItemLeadingIcon:
                icon: "email"

            MDListItemHeadlineText:
                text: "Email"

            MDListItemSupportingText:
                text: "kivydevelopment@gmail.com"

        MDListItem:
            theme_bg_color: "Custom"
            md_bg_color: self.theme_cls.surfaceContainerLowestColor

            MDListItemLeadingIcon:
                icon: "instagram"

            MDListItemHeadlineText:
                text: "Instagram"

            MDListItemSupportingText:
                text: "Account"

            MDListItemTertiaryText:
                text: "www.instagram.com/KivyMD"


MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    ScrollView:
        size_hint_x: .5
        pos_hint: {"center_x": .5, "center_y": .5}

        MDList:
            id: container
'''


class ExpansionPanelItem(MDExpansionPanel):
    ...


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


class Example(MDApp):
    def on_start(self):
        async def set_panel_list():
            for i in range(12):
                await asynckivy.sleep(0)
                self.root.ids.container.add_widget(ExpansionPanelItem())

        asynckivy.start(set_panel_list())

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def tap_expansion_chevron(
        self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton
    ):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not panel.is_open
            else [0, 0, 0, 0],
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)

from kivy.core.window import Window
Window.always_on_top = True
Example().run()