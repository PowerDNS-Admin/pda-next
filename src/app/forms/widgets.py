from django.forms.widgets import (
    CheckboxInput as BaseCheckboxInput,
    CheckboxSelectMultiple as BaseCheckboxSelectMultiple,
    EmailInput as BaseEmailInput,
    FileInput as BaseFileInput,
    HiddenInput as BaseHiddenInput,
    Input as BaseInput,
    MultipleHiddenInput as BaseMultipleHiddenInput,
    MultiWidget as BaseMultiWidget,
    NumberInput as BaseNumberInput,
    PasswordInput as BasePasswordInput,
    RadioSelect as BaseRadioSelect,
    Select as BaseSelect,
    SelectDateWidget as BaseSelectDateWidget,
    SplitDateTimeWidget as BaseSplitDateTimeWidget,
    SplitHiddenDateTimeWidget as BaseSplitHiddenDateTimeWidget,
    TextInput as BaseTextInput,
    URLInput as BaseURLInput,
)


class Input(BaseInput):
    template_name = 'app/forms/widgets/input.jinja2'


class TextInput(BaseTextInput):
    template_name = 'app/forms/widgets/text.jinja2'


class NumberInput(BaseNumberInput):
    template_name = 'app/forms/widgets/number.jinja2'


class CheckboxInput(BaseCheckboxInput):
    template_name = 'app/forms/widgets/checkbox.jinja2'


class EmailInput(BaseEmailInput):
    template_name = 'app/forms/widgets/email.jinja2'


class URLInput(BaseURLInput):
    template_name = 'app/forms/widgets/url.jinja2'


class UsernameInput(TextInput):
    template_name = '/app/forms/widgets/username.jinja2'


class UsernameOrEmailInput(TextInput):
    template_name = '/app/forms/widgets/username_or_email.jinja2'


class PasswordInput(BasePasswordInput):
    template_name = '/app/forms/widgets/password.jinja2'


class HiddenInput(BaseHiddenInput):
    template_name = 'app/forms/widgets/hidden.jinja2'


class MultipleHiddenInput(BaseMultipleHiddenInput):
    template_name = 'app/forms/widgets/multiple_hidden.jinja2'


class FileInput(BaseFileInput):
    template_name = 'app/forms/widgets/file.jinja2'


class Select(BaseSelect):
    template_name = 'app/forms/widgets/select.jinja2'
    option_template_name = 'app/forms/widgets/select_option.jinja2'


class RadioSelect(BaseRadioSelect):
    template_name = 'app/forms/widgets/radio.jinja2'
    option_template_name = 'app/forms/widgets/radio_option.jinja2'


class CheckboxSelectMultiple(BaseCheckboxSelectMultiple):
    template_name = 'app/forms/widgets/checkbox_select.jinja2'
    option_template_name = 'app/forms/widgets/checkbox_option.jinja2'


class MultiWidget(BaseMultiWidget):
    template_name = 'app/forms/widgets/multiwidget.jinja2'


class SplitDateTimeWidget(BaseSplitDateTimeWidget):
    template_name = 'app/forms/widgets/splitdatetime.jinja2'


class SplitHiddenDateTimeWidget(BaseSplitHiddenDateTimeWidget):
    template_name = 'app/forms/widgets/splithiddendatetime.jinja2'


class SelectDateWidget(BaseSelectDateWidget):
    template_name = 'app/forms/widgets/select_date.jinja2'


class FirstNameWidget(TextInput):
    template_name = 'app/forms/widgets/first_name.jinja2'


class LastNameWidget(TextInput):
    template_name = 'app/forms/widgets/last_name.jinja2'
