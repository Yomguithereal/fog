from fog.cli.reporting.html import print_html_report
from fog.cli.reporting.toml import print_toml_report

RENDERERS = {
    'html': print_html_report,
    'toml': print_toml_report
}
