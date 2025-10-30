# from django.forms import Widget
#
#
# class KeyValuewidjets(Widget):
#     template_name = "prod_add/key_value.html"
#
#     def format_value(self, value):
#         return value or {}
#
#     def value_from_datadict(self, data, files, name):
#         keys = data.getlist(f"{name}_key")
#         values = data.getlist(f"{name}_value")
#         return {k: v for k, v in zip(keys, values) if k}
#         return data.get(name)